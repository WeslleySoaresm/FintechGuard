
/* =========================================================
   FINTECHGUARD - DASHBOARD
   Arquivo: static/js/dashboard.js
   ========================================================= */

"use strict";

let allTickets = [];
let filteredTickets = [];
let ticketModal = null;
let selectedTicketId = null;

let currentPage = 1;
let pageSize = 20;

/* =========================================================
   AUTENTICAÇÃO
   ========================================================= */

function getToken() {
    return localStorage.getItem("access_token");
}

function redirectToLogin() {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
}

function getAuthHeaders() {
    const token = getToken();

    if (!token) {
        redirectToLogin();
        return {};
    }

    return {
        Authorization: `Bearer ${token}`
    };
}

/* =========================================================
   ERROS
   ========================================================= */

function showError(message) {
    const errorElement = document.getElementById("errorMessage");

    if (!errorElement) {
        console.error(message);
        return;
    }

    errorElement.textContent = message;
    errorElement.style.display = "block";
}

function hideError() {
    const errorElement = document.getElementById("errorMessage");

    if (!errorElement) {
        return;
    }

    errorElement.textContent = "";
    errorElement.style.display = "none";
}

/* =========================================================
   BUSCAR TICKETS
   ========================================================= */

async function fetchTickets() {
    hideError();

    const tableBody = document.getElementById("ticketsTableBody");

    if (!tableBody) {
        console.error("Elemento #ticketsTableBody não encontrado.");
        return;
    }

    tableBody.innerHTML = "";

    const loadingRow = document.createElement("tr");
    const loadingCell = document.createElement("td");

    loadingCell.colSpan = 8;
    loadingCell.className = "loading";
    loadingCell.textContent = "Carregando tickets...";

    loadingRow.appendChild(loadingCell);
    tableBody.appendChild(loadingRow);

    try {
        const token = getToken();

        if (!token) {
            redirectToLogin();
            return;
        }

        const response = await fetch("/tickets?limit=10000", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            redirectToLogin();
            return;
        }

        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}`);
        }

        const data = await response.json();

        allTickets = Array.isArray(data) ? data : [];

        updateDashboard();
        populateCategoryFilter();
        applyFilters();

    } catch (error) {
        console.error("Erro ao carregar tickets:", error);

        allTickets = [];
        filteredTickets = [];

        updateDashboard();
        renderCurrentPage();

        showError(
            "Erro ao carregar os tickets. Verifique se a API está funcionando."
        );
    }
}

/* =========================================================
   ATUALIZAR INDICADORES
   ========================================================= */

function updateDashboard() {
    const total = allTickets.length;

    const open = allTickets.filter(ticket =>
        String(ticket.ticket_status || "").toLowerCase() === "open"
    ).length;

    const highPriority = allTickets.filter(ticket =>
        String(ticket.ticket_priority || "").toLowerCase() === "high"
    ).length;

    const ratings = allTickets
        .map(ticket => ticket.customer_satisfaction_rating)
        .filter(value =>
            value !== null &&
            value !== undefined &&
            value !== "" &&
            Number.isFinite(Number(value))
        )
        .map(Number);

    let average = "-";

    if (ratings.length > 0) {
        const sum = ratings.reduce((totalValue, value) => {
            return totalValue + value;
        }, 0);

        average = (sum / ratings.length).toFixed(2);
    }

    const totalElement = document.getElementById("totalTickets");
    const openElement = document.getElementById("openTickets");
    const highElement = document.getElementById("highPriorityTickets");
    const averageElement = document.getElementById("averageRating");

    if (totalElement) {
        totalElement.textContent = total;
    }

    if (openElement) {
        openElement.textContent = open;
    }

    if (highElement) {
        highElement.textContent = highPriority;
    }

    if (averageElement) {
        averageElement.textContent = average;
    }
}

/* =========================================================
   FILTRO DE CATEGORIAS
   ========================================================= */

function populateCategoryFilter() {
    const select = document.getElementById("filterCategory");

    if (!select) {
        return;
    }

    const selectedValue = select.value;

    const categories = [
        ...new Set(
            allTickets
                .map(ticket => ticket.ticket_type)
                .filter(Boolean)
        )
    ].sort((a, b) => String(a).localeCompare(String(b), "pt-BR"));

    select.innerHTML = "";

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Todas as Categorias";

    select.appendChild(defaultOption);

    categories.forEach(category => {
        const option = document.createElement("option");

        option.value = category;
        option.textContent = category;

        select.appendChild(option);
    });

    if (categories.includes(selectedValue)) {
        select.value = selectedValue;
    }
}

/* =========================================================
   APLICAR FILTROS
   ========================================================= */

function applyFilters() {
    const searchElement = document.getElementById("filterSearch");
    const categoryElement = document.getElementById("filterCategory");
    const priorityElement = document.getElementById("filterPriority");
    const statusElement = document.getElementById("filterStatus");
    const pageSizeElement = document.getElementById("pageSize");

    const search = searchElement
        ? searchElement.value.trim().toLowerCase()
        : "";

    const category = categoryElement ? categoryElement.value : "";
    const priority = priorityElement ? priorityElement.value : "";
    const status = statusElement ? statusElement.value : "";

    if (pageSizeElement) {
        const requestedSize = Number(pageSizeElement.value);

        if (
            Number.isInteger(requestedSize) &&
            requestedSize > 0
        ) {
            pageSize = requestedSize;
        }
    }

    filteredTickets = allTickets.filter(ticket => {
        const id = String(ticket.id ?? "").toLowerCase();
        const name = String(ticket.customer_name ?? "").toLowerCase();
        const email = String(ticket.customer_email ?? "").toLowerCase();

        const matchesSearch =
            !search ||
            id.includes(search) ||
            name.includes(search) ||
            email.includes(search);

        const matchesCategory =
            !category || ticket.ticket_type === category;

        const matchesPriority =
            !priority || ticket.ticket_priority === priority;

        const matchesStatus =
            !status || ticket.ticket_status === status;

        return (
            matchesSearch &&
            matchesCategory &&
            matchesPriority &&
            matchesStatus
        );
    });

    // Quando os filtros mudam, volta para a primeira página.
    currentPage = 1;

    renderCurrentPage();
}

/* =========================================================
   PAGINAÇÃO
   ========================================================= */

function renderCurrentPage() {
    const total = filteredTickets.length;
    const totalPages = Math.max(
        1,
        Math.ceil(total / pageSize)
    );

    currentPage = Math.min(
        Math.max(1, currentPage),
        totalPages
    );

    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = Math.min(startIndex + pageSize, total);

    const ticketsToRender = filteredTickets.slice(
        startIndex,
        endIndex
    );

    renderTickets(ticketsToRender);

    updatePaginationControls(
        total,
        totalPages,
        startIndex,
        endIndex
    );
}

function updatePaginationControls(
    total,
    totalPages,
    startIndex,
    endIndex
) {
    const info = document.getElementById("paginationInfo");
    const pageLabel = document.getElementById("currentPage");
    const previousButton = document.getElementById("prevPageButton");
    const nextButton = document.getElementById("nextPageButton");

    if (info) {
        info.textContent = total === 0
            ? "Nenhum registro encontrado"
            : `Mostrando ${startIndex + 1}–${endIndex} de ${total} tickets`;
    }

    if (pageLabel) {
        pageLabel.textContent = `Página ${currentPage} de ${totalPages}`;
    }

    if (previousButton) {
        previousButton.disabled = currentPage <= 1 || total === 0;
    }

    if (nextButton) {
        nextButton.disabled =
            currentPage >= totalPages || total === 0;
    }
}

function goToPage(page) {
    const totalPages = Math.max(
        1,
        Math.ceil(filteredTickets.length / pageSize)
    );

    if (
        !Number.isInteger(page) ||
        page < 1 ||
        page > totalPages
    ) {
        return;
    }

    currentPage = page;
    renderCurrentPage();
}

/* =========================================================
   CRIAR CÉLULA SEGURA
   ========================================================= */

function createCell(value) {
    const cell = document.createElement("td");

    if (value === null || value === undefined || value === "") {
        cell.textContent = "-";
    } else {
        cell.textContent = String(value);
    }

    return cell;
}

/* =========================================================
   CRIAR BADGES
   ========================================================= */

function createBadge(text, className) {
    const badge = document.createElement("span");

    badge.className = `badge ${className}`;
    badge.textContent = text || "-";

    return badge;
}

function getStatusClass(status) {
    const normalized = String(status || "").toLowerCase();

    if (normalized === "open") {
        return "status-open";
    }

    if (normalized === "closed") {
        return "status-closed";
    }

    if (normalized === "pending") {
        return "status-pending";
    }

    return "";
}

function getPriorityClass(priority) {
    const normalized = String(priority || "").toLowerCase();

    if (normalized === "high") {
        return "priority-high";
    }

    if (normalized === "medium") {
        return "priority-medium";
    }

    if (normalized === "low") {
        return "priority-low";
    }

    return "";
}

/* =========================================================
   RENDERIZAR TICKETS
   ========================================================= */

function renderTickets(tickets) {
    const tableBody = document.getElementById("ticketsTableBody");

    if (!tableBody) {
        console.error("Elemento #ticketsTableBody não encontrado.");
        return;
    }

    tableBody.innerHTML = "";

    if (!Array.isArray(tickets) || tickets.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 8;
        cell.className = "empty";
        cell.textContent = "Nenhum ticket encontrado.";

        row.appendChild(cell);
        tableBody.appendChild(row);

        return;
    }

    tickets.forEach(ticket => {
        const row = document.createElement("tr");

        row.appendChild(createCell(`#${ticket.id}`));
        row.appendChild(createCell(ticket.customer_name));
        row.appendChild(createCell(ticket.ticket_subject));
        row.appendChild(createCell(ticket.ticket_type));

        const statusCell = document.createElement("td");

        statusCell.appendChild(
            createBadge(
                ticket.ticket_status,
                getStatusClass(ticket.ticket_status)
            )
        );

        row.appendChild(statusCell);

        const priorityCell = document.createElement("td");

        priorityCell.appendChild(
            createBadge(
                ticket.ticket_priority,
                getPriorityClass(ticket.ticket_priority)
            )
        );

        row.appendChild(priorityCell);

        const ratingCell = document.createElement("td");

        if (
            ticket.customer_satisfaction_rating !== null &&
            ticket.customer_satisfaction_rating !== undefined &&
            ticket.customer_satisfaction_rating !== ""
        ) {
            ratingCell.textContent =
                `⭐ ${ticket.customer_satisfaction_rating}`;
        } else {
            ratingCell.textContent = "-";
        }

        row.appendChild(ratingCell);

        /* AÇÕES: botão de exclusão */

        const actionsCell = document.createElement("td");
        const deleteButton = document.createElement("button");

        deleteButton.type = "button";
        deleteButton.className =
            "button button-danger delete-ticket-button";

        deleteButton.textContent = "Excluir";

        deleteButton.setAttribute(
            "aria-label",
            `Excluir ticket ${ticket.id}`
        );

        deleteButton.addEventListener("click", async event => {
            event.preventDefault();
            event.stopPropagation();

            await deleteTicket(ticket.id, deleteButton);
        });

        actionsCell.appendChild(deleteButton);
        row.appendChild(actionsCell);

        /* A linha abre os detalhes, mas o botão não. */

        row.addEventListener("click", () => {
            openTicketDetails(ticket);
        });

        tableBody.appendChild(row);
    });
}

/* =========================================================
   EXCLUIR TICKET
   ========================================================= */

async function deleteTicket(ticketId, button = null) {
    const id = Number(ticketId);

    if (!Number.isInteger(id) || id <= 0) {
        showError("ID do ticket inválido.");
        console.error("ID inválido recebido:", ticketId);
        return;
    }

    const confirmed = window.confirm(
        `Tem certeza de que deseja excluir o ticket #${id}?\n\n` +
        "Essa ação não poderá ser desfeita."
    );

    if (!confirmed) {
        return;
    }

    hideError();

    const originalButtonText = button
        ? button.textContent
        : null;

    const modalDeleteButton = document.getElementById(
        "deleteTicketButton"
    );

    const originalModalButtonText = modalDeleteButton
        ? modalDeleteButton.textContent
        : null;

    if (button) {
        button.disabled = true;
        button.textContent = "Excluindo...";
    }

    if (modalDeleteButton) {
        modalDeleteButton.disabled = true;
        modalDeleteButton.textContent = "Excluindo...";
    }

    try {
        const token = getToken();

        if (!token) {
            redirectToLogin();
            return;
        }

        const response = await fetch(
            `/tickets/${encodeURIComponent(id)}`,
            {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (response.status === 401) {
            redirectToLogin();
            return;
        }

        if (response.status === 404) {
            closeTicketDetails();

            showError(
                "Ticket não encontrado ou você não tem permissão para excluí-lo."
            );

            await fetchTickets();
            return;
        }

        if (!response.ok) {
            let detail = "";

            try {
                const body = await response.json();

                if (body.detail) {
                    detail = typeof body.detail === "string"
                        ? body.detail
                        : JSON.stringify(body.detail);
                }
            } catch {
                // A resposta pode não conter JSON.
            }

            throw new Error(
                `Erro HTTP ${response.status}` +
                (detail ? `: ${detail}` : "")
            );
        }

        selectedTicketId = null;
        closeTicketDetails();

        await fetchTickets();

    } catch (error) {
        console.error("Erro ao excluir ticket:", error);

        showError(
            error.message ||
            "Não foi possível excluir o ticket. Verifique a conexão com a API."
        );

    } finally {
        if (button) {
            button.disabled = false;
            button.textContent = originalButtonText || "Excluir";
        }

        if (modalDeleteButton) {
            modalDeleteButton.disabled = false;

            modalDeleteButton.textContent =
                originalModalButtonText || "Excluir Ticket";
        }
    }
}

/* =========================================================
   MODAL DE NOVO TICKET
   ========================================================= */

function closeModal() {
    if (!ticketModal) {
        return;
    }

    ticketModal.style.display = "none";

    const form = document.getElementById("ticketForm");

    if (form) {
        form.reset();
    }
}

/* =========================================================
   CRIAR TICKET
   ========================================================= */

async function createTicket(event) {
    event.preventDefault();
    hideError();

    const saveButton = document.getElementById("saveTicketButton");

    const getValue = id => {
        const element = document.getElementById(id);
        return element ? element.value.trim() : "";
    };

    const purchaseDate = getValue("date_of_purchase");
    const ageValue = getValue("customer_age");
    const ratingValue = getValue("customer_satisfaction_rating");

    const payload = {
        customer_name: getValue("customer_name"),
        customer_email: getValue("customer_email"),

        customer_age: ageValue ? Number(ageValue) : null,

        customer_gender:
            getValue("customer_gender") || null,

        product_purchased:
            getValue("product_purchased") || null,

        date_of_purchase: purchaseDate
            ? `${purchaseDate}T00:00:00`
            : null,

        ticket_type:
            getValue("ticket_type") || null,

        ticket_subject:
            getValue("ticket_subject"),

        ticket_description:
            getValue("ticket_description") || null,

        ticket_status:
            getValue("ticket_status") || "Open",

        ticket_priority:
            getValue("ticket_priority") || null,

        ticket_channel:
            getValue("ticket_channel") || null,

        first_response_time: null,
        time_to_resolution: null,
        resolution: null,

        customer_satisfaction_rating:
            ratingValue ? Number(ratingValue) : null
    };

    if (
        !payload.customer_name ||
        !payload.customer_email ||
        !payload.ticket_subject
    ) {
        showError("Nome, e-mail e assunto são obrigatórios.");
        return;
    }

    if (saveButton) {
        saveButton.disabled = true;
        saveButton.textContent = "Salvando...";
    }

    try {
        const token = getToken();

        if (!token) {
            redirectToLogin();
            return;
        }

        const response = await fetch("/tickets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        if (response.status === 401) {
            redirectToLogin();
            return;
        }

        let data = {};

        try {
            data = await response.json();
        } catch {
            data = {};
        }

        if (!response.ok) {
            let errorText = "Não foi possível criar o ticket.";

            if (data.detail) {
                if (Array.isArray(data.detail)) {
                    errorText = data.detail
                        .map(error => error.msg || "Campo inválido")
                        .join("; ");
                } else {
                    errorText = String(data.detail);
                }
            }

            showError(errorText);
            return;
        }

        closeModal();
        await fetchTickets();

    } catch (error) {
        console.error("Erro ao criar ticket:", error);
        showError("Erro de conexão com a API.");

    } finally {
        if (saveButton) {
            saveButton.disabled = false;
            saveButton.textContent = "Salvar Ticket";
        }
    }
}

/* =========================================================
   FORMATAÇÃO DOS DETALHES
   ========================================================= */

function formatValue(value) {
    if (value === null || value === undefined || value === "") {
        return "Não informado";
    }

    return String(value);
}

function formatDate(value) {
    if (!value) {
        return "Não informado";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return formatValue(value);
    }

    return date.toLocaleString("pt-BR");
}

function formatRating(value) {
    if (value === null || value === undefined || value === "") {
        return "Não avaliado";
    }

    return `${value} ⭐`;
}

/* =========================================================
   ABRIR DETALHES
   ========================================================= */

function openTicketDetails(ticket) {
    selectedTicketId = ticket.id;

    const ticketId = document.getElementById("detailsTicketId");
    const ticketSubject = document.getElementById("detailsTicketSubject");
    const statusElement = document.getElementById("detailsTicketStatus");
    const priorityElement = document.getElementById("detailsTicketPriority");

    if (ticketId) {
        ticketId.textContent = formatValue(ticket.id);
    }

    if (ticketSubject) {
        ticketSubject.textContent = formatValue(ticket.ticket_subject);
    }

    if (statusElement) {
        statusElement.textContent = formatValue(ticket.ticket_status);
        statusElement.className =
            `badge ${getStatusClass(ticket.ticket_status)}`;
    }

    if (priorityElement) {
        priorityElement.textContent = formatValue(ticket.ticket_priority);
        priorityElement.className =
            `badge ${getPriorityClass(ticket.ticket_priority)}`;
    }

    setDetailText(
        "detailsTicketRating",
        formatRating(ticket.customer_satisfaction_rating)
    );

    setDetailText("detailsCustomerName", formatValue(ticket.customer_name));
    setDetailText("detailsCustomerEmail", formatValue(ticket.customer_email));
    setDetailText("detailsCustomerAge", formatValue(ticket.customer_age));
    setDetailText("detailsCustomerGender", formatValue(ticket.customer_gender));
    setDetailText("detailsProduct", formatValue(ticket.product_purchased));
    setDetailText("detailsTicketType", formatValue(ticket.ticket_type));
    setDetailText("detailsTicketChannel", formatValue(ticket.ticket_channel));
    setDetailText("detailsPurchaseDate", formatDate(ticket.date_of_purchase));
    setDetailText("detailsSubject", formatValue(ticket.ticket_subject));
    setDetailText("detailsDescription", formatValue(ticket.ticket_description));
    setDetailText("detailsFirstResponse", formatDate(ticket.first_response_time));
    setDetailText("detailsResolutionTime", formatDate(ticket.time_to_resolution));
    setDetailText("detailsResolution", formatValue(ticket.resolution));
    setDetailText("detailsUserId", formatValue(ticket.user_id));
    setDetailText("detailsCreatedAt", formatDate(ticket.created_at));

    const modal = document.getElementById("ticketDetailsModal");

    if (modal) {
        modal.style.display = "block";
    }
}

/* =========================================================
   PREENCHER CAMPOS DOS DETALHES
   ========================================================= */

function setDetailText(elementId, value) {
    const element = document.getElementById(elementId);

    if (!element) {
        return;
    }

    element.textContent = value;
}

/* =========================================================
   FECHAR DETALHES
   ========================================================= */

function closeTicketDetails() {
    const modal = document.getElementById("ticketDetailsModal");

    if (modal) {
        modal.style.display = "none";
    }

    selectedTicketId = null;
}

/* =========================================================
   INICIALIZAÇÃO
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {
    const token = getToken();

    if (!token) {
        redirectToLogin();
        return;
    }

    /* Novo ticket */

    ticketModal = document.getElementById("ticketModal");

    const newTicketButton = document.getElementById("newTicketButton");

    if (newTicketButton && ticketModal) {
        newTicketButton.addEventListener("click", function () {
            ticketModal.style.display = "block";
        });
    }

    const closeModalButton = document.getElementById("closeModalButton");

    if (closeModalButton) {
        closeModalButton.addEventListener("click", closeModal);
    }

    const cancelModalButton = document.getElementById("cancelModalButton");

    if (cancelModalButton) {
        cancelModalButton.addEventListener("click", closeModal);
    }

    const ticketForm = document.getElementById("ticketForm");

    if (ticketForm) {
        ticketForm.addEventListener("submit", createTicket);
    }

    /* Modal de detalhes */

    const ticketDetailsModal = document.getElementById("ticketDetailsModal");

    const closeTicketDetailsButton = document.getElementById(
        "closeTicketDetailsButton"
    );

    const closeTicketDetailsX = document.getElementById(
        "closeTicketDetails"
    );

    const deleteModalButton = document.getElementById("deleteTicketButton");

    if (deleteModalButton) {
        deleteModalButton.addEventListener("click", async function (event) {
            event.preventDefault();
            event.stopPropagation();

            if (selectedTicketId !== null) {
                await deleteTicket(selectedTicketId, deleteModalButton);
            } else {
                showError("Nenhum ticket foi selecionado para exclusão.");
            }
        });
    }

    if (closeTicketDetailsButton) {
        closeTicketDetailsButton.addEventListener(
            "click",
            closeTicketDetails
        );
    }

    if (closeTicketDetailsX) {
        closeTicketDetailsX.addEventListener(
            "click",
            closeTicketDetails
        );
    }

    if (ticketDetailsModal) {
        ticketDetailsModal.addEventListener("click", function (event) {
            if (event.target === ticketDetailsModal) {
                closeTicketDetails();
            }
        });
    }

    /* Tecla Escape */

    document.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") {
            return;
        }

        closeTicketDetails();

        if (ticketModal && ticketModal.style.display === "block") {
            closeModal();
        }
    });

    /* Filtros */

    const filterSearch = document.getElementById("filterSearch");
    const filterCategory = document.getElementById("filterCategory");
    const filterPriority = document.getElementById("filterPriority");
    const filterStatus = document.getElementById("filterStatus");

    if (filterSearch) {
        filterSearch.addEventListener("input", applyFilters);
    }

    if (filterCategory) {
        filterCategory.addEventListener("change", applyFilters);
    }

    if (filterPriority) {
        filterPriority.addEventListener("change", applyFilters);
    }

    if (filterStatus) {
        filterStatus.addEventListener("change", applyFilters);
    }

    /* Controles da paginação */

    const pageSizeElement = document.getElementById("pageSize");
    const previousPageButton = document.getElementById("prevPageButton");
    const nextPageButton = document.getElementById("nextPageButton");

    if (pageSizeElement) {
        pageSizeElement.addEventListener("change", applyFilters);
    }

    if (previousPageButton) {
        previousPageButton.addEventListener("click", function () {
            goToPage(currentPage - 1);
        });
    }

    if (nextPageButton) {
        nextPageButton.addEventListener("click", function () {
            goToPage(currentPage + 1);
        });
    }

    /* Logout */

    const logoutButton = document.getElementById("logoutButton");

    if (logoutButton) {
        logoutButton.addEventListener("click", function () {
            localStorage.removeItem("access_token");
            window.location.href = "/login";
        });
    }

    /* Fechar modal de criação ao clicar fora */

    if (ticketModal) {
        ticketModal.addEventListener("click", function (event) {
            if (event.target === ticketModal) {
                closeModal();
            }
        });
    }

    /* Carregar dados */

    fetchTickets();
});
