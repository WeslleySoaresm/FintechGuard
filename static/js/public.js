
"use strict";

document.addEventListener("DOMContentLoaded", () => {
    initializeFooterYear();
    initializeChat();
});

/**
 * Atualiza o ano do rodapé.
 */
function initializeFooterYear() {
    const yearElement = document.getElementById("current-year");

    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

/**
 * Inicializa o chat.
 */
function initializeChat() {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("chat-input");
    const messages = document.getElementById("chat-messages");
    const suggestions = document.getElementById("chat-suggestions");
    const sendButton = document.getElementById("send-button");

    if (!form || !input || !messages || !sendButton) {
        console.error("Elementos necessários para o chat não encontrados.");
        return;
    }

    let isSending = false;
    let conversationId = null;

    /*
     * Se o usuário estiver trabalhando com um ticket,
     * defina o ID real aqui ou carregue-o da aplicação.
     *
     * Não invente um ticket_id.
     */
    let ticketId = null;

    /**
     * Recupera o token de autenticação.
     *
     * IMPORTANTE:
     * Esta função precisa ser integrada ao mecanismo
     * de autenticação utilizado pelo seu projeto.
     *
     * Não coloque tokens secretos diretamente no código.
     */
    async function getAccessToken() {
        /*
         * O ideal é utilizar um cookie HttpOnly, Secure
         * e SameSite, com suporte correspondente no backend.
         *
         * Enquanto isso não estiver implementado,
         * não enviamos requisições sem autenticação.
         */
        return null;
    }

    /**
     * Adiciona uma mensagem ao histórico visual.
     */
    function addMessage(text, type) {
        const message = document.createElement("div");
        message.className = `message ${type}-message`;

        const avatar = document.createElement("div");
        avatar.className = "message-avatar";
        avatar.textContent = type === "assistant" ? "FG" : "EU";

        const content = document.createElement("div");
        content.className = "message-content";

        const author = document.createElement("span");
        author.className = "message-author";
        author.textContent = type === "assistant"
            ? "FintechGuard"
            : "Você";

        const bubble = document.createElement("div");
        bubble.className = "message-bubble";
        bubble.textContent = text;

        const time = document.createElement("span");
        time.className = "message-time";
        time.textContent = new Date().toLocaleTimeString("pt-BR", {
            hour: "2-digit",
            minute: "2-digit"
        });

        content.append(author, bubble, time);
        message.append(avatar, content);
        messages.appendChild(message);

        scrollToLatestMessage();
    }

    /**
     * Exibe informações complementares da resposta.
     */
    function addAgentMetadata(data) {
        if (!data.requires_human) {
            return;
        }

        const notice = document.createElement("div");
        notice.className = "agent-escalation-notice";

        notice.textContent =
            "Sua solicitação precisa de atendimento humano. " +
            "O encaminhamento foi identificado pelo sistema.";

        messages.appendChild(notice);
        scrollToLatestMessage();
    }

    /**
     * Mantém a conversa na última mensagem.
     */
    function scrollToLatestMessage() {
        messages.scrollTop = messages.scrollHeight;
    }

    /**
     * Mostra o indicador de digitação.
     */
    function showTyping() {
        removeTyping();

        const typing = document.createElement("div");
        typing.className = "message assistant-message";
        typing.id = "typing-indicator";

        const avatar = document.createElement("div");
        avatar.className = "message-avatar";
        avatar.textContent = "FG";

        const bubble = document.createElement("div");
        bubble.className = "message-bubble typing-indicator";
        bubble.setAttribute("aria-label", "Assistente está digitando");

        for (let index = 0; index < 3; index++) {
            bubble.appendChild(document.createElement("span"));
        }

        typing.append(avatar, bubble);
        messages.appendChild(typing);

        scrollToLatestMessage();
    }

    /**
     * Remove o indicador de digitação.
     */
    function removeTyping() {
        document.getElementById("typing-indicator")?.remove();
    }

    /**
     * Envia a mensagem ao endpoint real do agente.
     */
    async function sendToAgent(message) {
        const token = await getAccessToken();

        if (!token) {
            throw new Error(
                "Para utilizar o atendimento, é necessário entrar na sua conta."
            );
        }

        const payload = {
            message: message,
            conversation_id: conversationId,
            ticket_id: ticketId
        };

        const response = await fetch("/agent", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`
            },
            credentials: "same-origin",
            body: JSON.stringify(payload)
        });

        let data;

        try {
            data = await response.json();
        } catch {
            throw new Error(
                "O servidor retornou uma resposta inválida."
            );
        }

        if (response.status === 401) {
            throw new Error(
                "Sua sessão expirou ou não é válida. Entre novamente."
            );
        }

        if (response.status === 403) {
            throw new Error(
                "Você não possui autorização para realizar esta operação."
            );
        }

        if (!response.ok) {
            const detail = typeof data.detail === "string"
                ? data.detail
                : `Erro HTTP ${response.status}.`;

            throw new Error(detail);
        }

        /*
         * Campos definidos pelo AgentResponse.
         */
        if (
            typeof data.response !== "string" ||
            !data.response.trim()
        ) {
            console.error("Resposta recebida:", data);

            throw new Error(
                "O agente não retornou uma resposta válida."
            );
        }

        if (
            !Number.isInteger(data.conversation_id) ||
            data.conversation_id <= 0
        ) {
            throw new Error(
                "O servidor não retornou um identificador válido de conversa."
            );
        }

        conversationId = data.conversation_id;

        return data;
    }

    /**
     * Processa o envio de uma mensagem.
     */
    async function handleSendMessage(text) {
        const cleanText = text.trim();

        if (!cleanText || isSending) {
            return;
        }

        if (cleanText.length > 2000) {
            addMessage(
                "Sua mensagem ultrapassou o limite de 2.000 caracteres.",
                "assistant"
            );
            return;
        }

        addMessage(cleanText, "user");

        input.value = "";

        if (suggestions) {
            suggestions.hidden = true;
        }

        isSending = true;
        input.disabled = true;
        sendButton.disabled = true;

        showTyping();

        try {
            const result = await sendToAgent(cleanText);

            removeTyping();

            addMessage(result.response, "assistant");

            addAgentMetadata(result);

        } catch (error) {
            removeTyping();

            console.error("Erro no atendimento:", error);

            addMessage(
                error.message ||
                "Não foi possível conectar ao atendimento.",
                "assistant"
            );

        } finally {
            isSending = false;
            input.disabled = false;
            sendButton.disabled = false;
            input.focus();
        }
    }

    /**
     * Envio pelo formulário.
     */
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        handleSendMessage(input.value);
    });

    /**
     * Perguntas sugeridas.
     */
    document.querySelectorAll(".suggestion-button").forEach((button) => {
        button.addEventListener("click", () => {
            const suggestedMessage = button.dataset.message;

            if (suggestedMessage) {
                handleSendMessage(suggestedMessage);
            }
        });
    });
}
