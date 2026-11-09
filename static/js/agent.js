
document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chatForm");
    const messageInput = document.getElementById("messageInput");
    const chatMessages = document.getElementById("chatMessages");
    const sendButton = document.getElementById("sendButton");

    const analysisPanel = document.getElementById("analysisPanel");
    const analysisButton = document.getElementById("analysisButton");
    const closeAnalysisButton = document.getElementById("closeAnalysisButton");

    const newConversationButton = document.getElementById("newConversationButton");
    const historyButton = document.getElementById("historyButton");
    const historyDialog = document.getElementById("historyDialog");
    const closeHistoryButton = document.getElementById("closeHistoryButton");
    const conversationList = document.getElementById("conversationList");
    const historyStatus = document.getElementById("historyStatus");
    const loadMoreHistoryButton = document.getElementById("loadMoreHistoryButton");
    const logoutButton = document.getElementById("logoutButton");

    const ticketIdInput = document.getElementById("ticketIdInput");
    const associateTicketButton = document.getElementById("associateTicketButton");
    const ticketStatus = document.getElementById("ticketStatus");

    const riskValue = document.getElementById("riskValue");
    const intentValue = document.getElementById("intentValue");
    const humanValue = document.getElementById("humanValue");
    const priorityValue = document.getElementById("priorityValue");

    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.href = "/login";
        return;
    }

    let currentConversationId = null;
    let associatedTicketId = null;
    let sendingMessage = false;
    let historyOffset = 0;
    const historyPageSize = 50;

    function addMessage(text, sender, isError = false) {
        const message = document.createElement("div");

        message.classList.add("message", sender);

        if (isError) {
            message.classList.add("error");
        }

        const content = document.createElement("div");
        content.textContent = text;

        message.appendChild(content);
        chatMessages.appendChild(message);

        chatMessages.scrollTop = chatMessages.scrollHeight;

        return message;
    }

    function clearWelcomeMessage() {
        const welcome = chatMessages.querySelector(".welcome-message");

        if (welcome) {
            welcome.remove();
        }
    }

    function updateAnalysis(data) {
        riskValue.textContent = data.risk_level || "Não informado";
        intentValue.textContent = data.intent || "Não identificada";

        humanValue.textContent = data.requires_human
            ? "Sim"
            : "Não";

        priorityValue.textContent = data.priority || "Não definida";
    }

    function resetAnalysis() {
        riskValue.textContent = "Aguardando análise";
        intentValue.textContent = "Aguardando mensagem";
        humanValue.textContent = "Não avaliado";
        priorityValue.textContent = "Não avaliada";
    }

    function updateTicketStatus() {
        ticketStatus.textContent = associatedTicketId
            ? `Ticket associado: #${associatedTicketId}`
            : "Nenhum ticket associado";
    }

    async function loadConversationHistory(append = false) {
        historyDialog.classList.remove("hidden");
        if (!append) {
            historyOffset = 0;
            conversationList.replaceChildren();
            loadMoreHistoryButton.classList.add("hidden");
        }
        historyStatus.textContent = "Carregando conversas…";

        try {
            const response = await fetch(`/agent/conversations?limit=${historyPageSize}&offset=${historyOffset}`, {
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (response.status === 401) {
                localStorage.removeItem("access_token");
                window.location.href = "/login";
                return;
            }
            if (!response.ok) throw new Error("Não foi possível carregar o histórico.");

            const conversations = await response.json();
            if (!conversations.length && !append) {
                historyStatus.textContent = "Ainda não há conversas salvas.";
                return;
            }

            historyOffset += conversations.length;
            historyStatus.textContent = "Selecione uma conversa para abrir suas mensagens.";
            loadMoreHistoryButton.classList.toggle("hidden", conversations.length < historyPageSize);
            conversations.forEach((conversation) => {
                const item = document.createElement("button");
                item.type = "button";
                item.className = "conversation-item";
                const date = conversation.created_at
                    ? new Date(conversation.created_at).toLocaleString("pt-BR")
                    : `Conversa #${conversation.id}`;
                item.textContent = `${date}${conversation.ticket_id ? ` · Ticket #${conversation.ticket_id}` : " · Sem ticket"}`;
                item.addEventListener("click", () => openConversation(conversation.id));
                conversationList.appendChild(item);
            });
        } catch (error) {
            historyStatus.textContent = error.message || "Erro ao carregar o histórico.";
        }
    }

    async function openConversation(conversationId) {
        historyStatus.textContent = "Abrindo conversa…";
        try {
            const response = await fetch(`/agent/conversations/${conversationId}`, {
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (response.status === 401) {
                localStorage.removeItem("access_token");
                window.location.href = "/login";
                return;
            }
            if (!response.ok) throw new Error("Não foi possível abrir esta conversa.");

            const conversation = await response.json();
            currentConversationId = conversation.id;
            associatedTicketId = conversation.ticket_id;
            ticketIdInput.value = conversation.ticket_id || "";
            chatMessages.replaceChildren();
            conversation.messages.forEach((message) => {
                addMessage(message.message, message.sender_type === "CUSTOMER" ? "user" : "agent");
            });
            updateTicketStatus();
            resetAnalysis();
            historyDialog.classList.add("hidden");
            messageInput.focus();
        } catch (error) {
            historyStatus.textContent = error.message || "Erro ao abrir a conversa.";
        }
    }

    async function sendMessage(message) {
        if (sendingMessage) {
            return;
        }

        sendingMessage = true;
        sendButton.disabled = true;
        sendButton.textContent = "Enviando...";

        clearWelcomeMessage();
        addMessage(message, "user");

        const payload = {
            message: message
        };

        // Continua a conversa existente.
        if (currentConversationId !== null) {
            payload.conversation_id = currentConversationId;
        }

        // Associa o ticket, quando informado.
        if (associatedTicketId !== null) {
            payload.ticket_id = associatedTicketId;
        }

        try {
            const response = await fetch("/agent", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.status === 401) {
                localStorage.removeItem("access_token");
                window.location.href = "/login";
                return;
            }

            const data = await response.json();

            if (!response.ok) {
                const detail = data.detail || "Não foi possível processar sua mensagem.";

                throw new Error(
                    typeof detail === "string"
                        ? detail
                        : "Verifique os dados enviados."
                );
            }

            // Guarda o identificador retornado pelo backend.
            currentConversationId = data.conversation_id;

            addMessage(data.response, "agent");
            updateAnalysis(data);

        } catch (error) {
            addMessage(
                error.message || "Erro de comunicação com o servidor.",
                "agent",
                true
            );

        } finally {
            sendingMessage = false;
            sendButton.disabled = false;
            sendButton.textContent = "Enviar";
            messageInput.focus();
        }
    }

    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const message = messageInput.value.trim();

        if (!message || sendingMessage) {
            return;
        }

        messageInput.value = "";

        await sendMessage(message);
    });

    messageInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            chatForm.requestSubmit();
        }
    });

    analysisButton.addEventListener("click", () => {
        analysisPanel.classList.toggle("hidden");
    });

    closeAnalysisButton.addEventListener("click", () => {
        analysisPanel.classList.add("hidden");
    });

    newConversationButton.addEventListener("click", () => {
        if (sendingMessage) {
            return;
        }

        chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="assistant-avatar">F</div>
                <h2>Nova conversa iniciada.</h2>
                <p>Como posso ajudar você?</p>
            </div>
        `;

        // A próxima mensagem criará uma nova conversa no backend.
        currentConversationId = null;
        associatedTicketId = null;

        ticketIdInput.value = "";

        updateTicketStatus();
        resetAnalysis();
        messageInput.focus();
    });

    associateTicketButton.addEventListener("click", () => {
        const ticketId = Number(ticketIdInput.value);

        if (!Number.isInteger(ticketId) || ticketId <= 0) {
            addMessage(
                "Informe um ID de ticket válido.",
                "agent",
                true
            );
            return;
        }

        associatedTicketId = ticketId;
        updateTicketStatus();

        addMessage(
            `Ticket #${ticketId} será enviado para validação e associação pelo servidor.`,
            "agent"
        );
    });

    historyButton.addEventListener("click", () => {
        loadConversationHistory();
    });
    loadMoreHistoryButton.addEventListener("click", () => loadConversationHistory(true));

    closeHistoryButton.addEventListener("click", () => historyDialog.classList.add("hidden"));
    historyDialog.addEventListener("click", (event) => {
        if (event.target === historyDialog) historyDialog.classList.add("hidden");
    });

    logoutButton.addEventListener("click", () => {
        localStorage.removeItem("access_token");
        window.location.href = "/login";
    });

    updateTicketStatus();
});
