from datetime import datetime, timedelta
from functools import wraps
import re
import secrets
from urllib.parse import urlparse

from flask import Flask, flash, redirect, render_template, request, session, url_for
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
from database.connection import get_connection


app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(days=30)

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def _close_db(connection, cursor):
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()


def _get_connection(cursor_factory=None):
    connection = get_connection()
    if cursor_factory is None:
        cursor = connection.cursor()
    else:
        cursor = connection.cursor(cursor_factory=cursor_factory)
    return connection, cursor


def _clean_string(value):
    return (value or "").strip()


def _normalize_email(value):
    email = _clean_string(value).lower()
    if not email or not EMAIL_PATTERN.match(email):
        return ""
    return email


def _safe_redirect(default_endpoint="dashboard"):
    target = request.args.get("next")
    if target and target.startswith("/") and not target.startswith("//"):
        parsed_target = urlparse(target)
        if not parsed_target.netloc:
            return redirect(target)
    return redirect(url_for(default_endpoint))


def _load_user_by_identifier(identifier):
    connection = None
    cursor = None
    try:
        connection, cursor = _get_connection(RealDictCursor)
        cursor.execute(
            """
            SELECT
                user_id,
                username,
                email,
                full_name,
                password_hash,
                deleted_at
            FROM users
            WHERE deleted_at IS NULL
              AND (
                    LOWER(username) = LOWER(%s)
                 OR LOWER(email) = LOWER(%s)
              )
            LIMIT 1
            """,
            (identifier, identifier),
        )
        return cursor.fetchone()
    finally:
        _close_db(connection, cursor)


def _load_user_by_email(email):
    connection = None
    cursor = None
    try:
        connection, cursor = _get_connection(RealDictCursor)
        cursor.execute(
            """
            SELECT
                user_id,
                username,
                email,
                full_name,
                password_hash,
                deleted_at
            FROM users
            WHERE deleted_at IS NULL
              AND LOWER(email) = LOWER(%s)
            LIMIT 1
            """,
            (email,),
        )
        return cursor.fetchone()
    finally:
        _close_db(connection, cursor)


def _load_reset_candidate(token):
    connection = None
    cursor = None
    try:
        connection, cursor = _get_connection(RealDictCursor)
        cursor.execute(
            """
            SELECT
                pr.reset_id,
                pr.user_id,
                pr.token_hash,
                pr.expires_at,
                pr.used_at,
                u.username,
                u.email
            FROM password_resets pr
            JOIN users u
              ON u.user_id = pr.user_id
            WHERE pr.used_at IS NULL
              AND pr.expires_at > NOW()
            ORDER BY pr.created_at DESC
            """,
        )
        rows = cursor.fetchall()
        for row in rows:
            if check_password_hash(row["token_hash"], token):
                return row
        return None
    finally:
        _close_db(connection, cursor)


def _store_reset_token(user_id, token_hash, expires_at):
    connection = None
    cursor = None
    try:
        connection, cursor = _get_connection()
        cursor.execute(
            """
            UPDATE password_resets
            SET used_at = %s
            WHERE user_id = %s
              AND used_at IS NULL
            """,
            (datetime.utcnow(), user_id),
        )
        cursor.execute(
            """
            INSERT INTO password_resets (
                user_id,
                token_hash,
                expires_at
            )
            VALUES (%s, %s, %s)
            """,
            (user_id, token_hash, expires_at),
        )
        connection.commit()
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        _close_db(connection, cursor)


def _update_password(user_id, password_hash):
    connection = None
    cursor = None
    try:
        connection, cursor = _get_connection()
        cursor.execute(
            """
            UPDATE users
            SET password_hash = %s,
                updated_at = %s
            WHERE user_id = %s
            """,
            (password_hash, datetime.utcnow(), user_id),
        )
        cursor.execute(
            """
            UPDATE password_resets
            SET used_at = %s
            WHERE user_id = %s
              AND used_at IS NULL
            """,
            (datetime.utcnow(), user_id),
        )
        connection.commit()
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        _close_db(connection, cursor)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        full_name = _clean_string(request.form.get("full_name"))
        username = _clean_string(request.form.get("username"))
        email = _normalize_email(request.form.get("email"))
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        terms_accepted = request.form.get("terms") == "on"

        if not full_name or len(full_name) < 3:
            flash("Full name must be at least 3 characters long.", "danger")
            return redirect(url_for("register"))

        if not username or len(username) < 3 or len(username) > 50 or " " in username:
            flash("Username must be 3-50 characters and contain no spaces.", "danger")
            return redirect(url_for("register"))

        if not email:
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Password confirmation does not match.", "danger")
            return redirect(url_for("register"))

        if not terms_accepted:
            flash("You must agree to the terms before continuing.", "danger")
            return redirect(url_for("register"))

        connection = None
        cursor = None
        try:
            connection, cursor = _get_connection(RealDictCursor)
            cursor.execute(
                """
                SELECT 1
                FROM users
                WHERE deleted_at IS NULL
                  AND (
                        LOWER(username) = LOWER(%s)
                     OR LOWER(email) = LOWER(%s)
                  )
                LIMIT 1
                """,
                (username, email),
            )
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Username or email is already in use.", "danger")
                return redirect(url_for("register"))

            password_hash = generate_password_hash(password)
            cursor.execute(
                """
                INSERT INTO users (
                    username,
                    email,
                    password_hash,
                    full_name
                )
                VALUES (%s, %s, %s, %s)
                """,
                (username, email, password_hash, full_name),
            )
            connection.commit()
        except Exception:
            if connection is not None:
                connection.rollback()
            flash("Registration failed. Please try again.", "danger")
            return redirect(url_for("register"))
        finally:
            _close_db(connection, cursor)

        flash("Account created successfully. Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("auth/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        identifier = _clean_string(request.form.get("identifier"))
        password = request.form.get("password", "")
        remember_me = request.form.get("remember_me") == "on"

        if not identifier or not password:
            flash("Please enter your username or email and password.", "danger")
            return redirect(url_for("login"))

        user = _load_user_by_identifier(identifier)

        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid credentials.", "danger")
            return redirect(url_for("login"))

        connection = None
        cursor = None
        try:
            connection, cursor = _get_connection()
            cursor.execute(
                """
                UPDATE users
                SET last_login = %s,
                    updated_at = %s
                WHERE user_id = %s
                """,
                (datetime.utcnow(), datetime.utcnow(), user["user_id"]),
            )
            connection.commit()
        except Exception:
            if connection is not None:
                connection.rollback()
        finally:
            _close_db(connection, cursor)

        session.clear()
        session.permanent = remember_me
        session["user_id"] = user["user_id"]
        session["username"] = user["username"]
        session["email"] = user["email"]
        session["full_name"] = user["full_name"] or user["username"]
        session["remember_me"] = remember_me

        flash("Signed in successfully.", "success")
        return _safe_redirect("dashboard")

    return render_template("auth/login.html")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = _normalize_email(request.form.get("email"))

        if not email:
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("forgot_password"))

        user = _load_user_by_email(email)
        if user:
            token = secrets.token_urlsafe(32)
            token_hash = generate_password_hash(token)
            expires_at = datetime.utcnow() + timedelta(hours=1)

            try:
                _store_reset_token(user["user_id"], token_hash, expires_at)
                reset_link = url_for("reset_password", token=token, _external=False)
                app.logger.info("Password reset token for %s: %s", email, token)
                print(f"[BelajarYuk] Password reset token for {email}: {token}")
                print(f"[BelajarYuk] Reset link: {reset_link}")
            except Exception:
                flash("Unable to create password reset token. Please try again.", "danger")
                return redirect(url_for("forgot_password"))

        flash(
            "If the email exists, a reset token has been created. Check the Flask terminal for development.",
            "success",
        )
        return redirect(url_for("forgot_password"))

    return render_template("auth/forgot_password.html")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    reset_request = _load_reset_candidate(token)
    if not reset_request:
        flash("The reset token is invalid or has expired.", "danger")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
            return redirect(url_for("reset_password", token=token))

        if password != confirm_password:
            flash("Password confirmation does not match.", "danger")
            return redirect(url_for("reset_password", token=token))

        try:
            _update_password(reset_request["user_id"], generate_password_hash(password))
        except Exception:
            flash("Unable to reset password. Please try again.", "danger")
            return redirect(url_for("reset_password", token=token))

        flash("Password reset successfully. Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("auth/reset_password.html", reset_request=reset_request)


@app.route("/dashboard")
@login_required
def dashboard():
    display_name = session.get("full_name") or session.get("username") or "User"
    return render_template("dashboard/index.html", display_name=display_name)


@app.route("/home")
@login_required
def home():
    return redirect(url_for("dashboard"))


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
