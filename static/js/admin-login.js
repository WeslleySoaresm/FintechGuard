
const adminLoginForm = document.getElementById("adminLoginForm");
const loginMessage = document.getElementById("loginMessage");
const loginButton = document.getElementById("loginButton");

adminLoginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    loginMessage.hidden = true;
    loginButton.disabled = true;
    loginButton.textContent = "Verificando...";

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/admin/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "same-origin",
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Não foi possível entrar no painel."
            );
        }

        // A sessão é criada no servidor por meio de um cookie seguro.
        window.location.assign("/admin");
    } catch (error) {
        loginMessage.textContent =
            error.message || "Erro de comunicação com o servidor.";

        loginMessage.className = "message error";
        loginMessage.hidden = false;
    } finally {
        loginButton.disabled = false;
        loginButton.textContent = "Entrar no painel";
    }
});
