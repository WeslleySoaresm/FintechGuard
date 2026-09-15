const loginForm =
    document.getElementById("loginForm");


const loginButton =
    document.getElementById("loginButton");


const message =
    document.getElementById("message");


function showMessage(text, type) {

    message.textContent = text;

    message.className =
        `message ${type}`;

    message.style.display = "block";
}


function hideMessage() {

    message.textContent = "";

    message.style.display = "none";
}


loginForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        hideMessage();


        const email =
            document
                .getElementById("email")
                .value
                .trim();


        /*
         * Não usamos trim() na senha.
         *
         * Espaços podem fazer parte
         * de uma senha.
         */
        const password =
            document
                .getElementById("password")
                .value;


        if (!email || !password) {

            showMessage(
                "Preencha o e-mail e a senha.",
                "error"
            );

            return;
        }


        loginButton.disabled = true;

        loginButton.textContent =
            "Entrando...";


        try {

            const response =
                await fetch(
                    "/auth/token",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                email: email,
                                password: password
                            })
                    }
                );


            let data = {};


            try {

                data =
                    await response.json();

            } catch {

                data = {};

            }


            if (!response.ok) {

                let errorMessage =
                    "Não foi possível realizar o login.";


                if (response.status === 401) {

                    errorMessage =
                        "E-mail ou senha inválidos.";

                }


                if (response.status === 429) {

                    errorMessage =
                        "Muitas tentativas. Aguarde alguns minutos antes de tentar novamente.";

                }


                if (data.detail) {

                    errorMessage =
                        data.detail;

                }


                showMessage(
                    errorMessage,
                    "error"
                );

                return;
            }


            if (!data.access_token) {

                showMessage(
                    "O servidor não retornou um token de acesso.",
                    "error"
                );

                return;

            }


            localStorage.setItem(
                "access_token",
                data.access_token
            );


            document.cookie =
                `access_token=${encodeURIComponent(data.access_token)}; path=/; SameSite=Lax`;


            showMessage(
                "Login realizado com sucesso.",
                "success"
            );


            setTimeout(
                () => {

                    window.location.href =
                        "/dashboard";

                },
                500
            );


        } catch (error) {

            console.error(
                "Erro no login:",
                error
            );


            showMessage(
                "Não foi possível conectar ao servidor.",
                "error"
            );


        } finally {

            loginButton.disabled = false;

            loginButton.textContent =
                "Entrar";

        }

    }
);