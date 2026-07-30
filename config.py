import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'belajaryuk-dev-secret-key-129847192'
    IS_VERCEL = os.environ.get('VERCEL') == '1'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or (
        'sqlite:////tmp/belajaryuk.db' if IS_VERCEL
        else 'sqlite:///' + os.path.join(BASE_DIR, 'belajaryuk.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,   # cek koneksi masih hidup sebelum dipakai (penting untuk DB online)
        'pool_recycle': 280,     # daur ulang koneksi tiap ~280 detik, hindari "MySQL server has gone away"
    }

    # Upload configurations
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or (
        '/tmp/uploads' if IS_VERCEL else os.path.join(BASE_DIR, 'static', 'uploads')
    )
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
