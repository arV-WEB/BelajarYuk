document.addEventListener("DOMContentLoaded", () => {
    const toggleButtons = document.querySelectorAll("[data-password-toggle]");

    toggleButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const targetId = button.getAttribute("data-password-toggle");
            const target = document.getElementById(targetId);

            if (!target) {
                return;
            }

            const isPassword = target.type === "password";
            target.type = isPassword ? "text" : "password";
            button.setAttribute("aria-pressed", String(isPassword));

            const icon = button.querySelector("[data-password-icon]");
            if (icon) {
                icon.innerHTML = isPassword
                    ? '<path d="M2.25 12s3.75-6.75 9.75-6.75S21.75 12 21.75 12s-3.75 6.75-9.75 6.75S2.25 12 2.25 12Zm9.75 4.5A4.5 4.5 0 1 0 7.5 12a4.5 4.5 0 0 0 4.5 4.5Zm0-2.1A2.4 2.4 0 1 1 14.4 12a2.4 2.4 0 0 1-2.4 2.4Z"></path>'
                    : '<path d="M3 4.5 19.5 21m-4.162-4.162A9.8 9.8 0 0 1 12 18.75C6 18.75 2.25 12 2.25 12a17.65 17.65 0 0 1 3.15-4.162M9.55 6.28A9.71 9.71 0 0 1 12 5.25C18 5.25 21.75 12 21.75 12a18.09 18.09 0 0 1-2.6 3.73"></path>';
            }
        });
    });
});
