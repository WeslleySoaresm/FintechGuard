/* =========================================================
   FINTECHGUARD - DASHBOARD
   ========================================================= */

let allTickets = [];

let ticketModal = null;


/* =========================================================
   AUTENTICAÇÃO
   ========================================================= */

function getToken() {

    return localStorage.getItem(
        "access_token"
    );
}


function redirectToLogin() {

    localStorage.removeItem(
        "access_token"
    );

    window.location.href = "/login";
}


function getAuthHeaders() {

    const token = getToken();

    if (!token) {

        redirectToLogin();

        return {};
    }

    return {
        "Authorization":
            `Bearer ${token}`
    };
}


/* =========================================================
   ERROS
   ========================================================= */

function showError(message) {

    const errorElement =
        document.getElementById(
            "errorMessage"
        );

    if (!errorElement) {
        return;
    }

    errorElement.textContent =
        message;

    errorElement.style.display =
        "block";
}


function hideError() {

    const errorElement =
        document.getElementById(
            "errorMessage"
        );

    if (!errorElement) {
        return;
    }

    errorElement.textContent = "";

    errorElement.style.display =
        "none";
}


/* =========================================================
   BUSCAR TICKETS
   ========================================================= */

async function fetchTickets() {

    hideError();

    const tableBody =
        document.getElementById(
            "ticketsTableBody"
        );

    if (!tableBody) {
        return;
    }

    tableBody.innerHTML = "";


    const loadingRow =
        document.createElement("tr");


    const loadingCell =
        document.createElement("td");


    loadingCell.colSpan = 7;

    loadingCell.className =
        "loading";

    loadingCell.textContent =
        "Carregando tickets...";


    loadingRow.appendChild(
        loadingCell
    );


    tableBody.appendChild(
        loadingRow
    );


    try {

        const response =
            await fetch(
                "/tickets?limit=100",
                {
                    method: "GET",

                    headers:
                        getAuthHeaders()
                }
            );


        if (response.status === 401) {

            redirectToLogin();

            return;
        }


        if (!response.ok) {

            throw new Error(
                `Erro HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        allTickets =
            Array.isArray(data)
                ? data
                : [];


        updateDashboard();

        populateCategoryFilter();

        renderTickets(
            allTickets
        );


    } catch (error) {

        console.error(
            "Erro ao carregar tickets:",
            error
        );


        allTickets = [];

        tableBody.innerHTML = "";


        const row =
            document.createElement("tr");


        const cell =
            document.createElement("td");


        cell.colSpan = 7;

        cell.className =
            "empty";

        cell.textContent =
            "Não foi possível carregar os tickets.";


        row.appendChild(cell);

        tableBody.appendChild(row);


        showError(
            "Erro ao carregar os tickets. Verifique se a API está funcionando."
        );
    }
}


/* =========================================================
   DASHBOARD
   ========================================================= */

function updateDashboard() {

    const total =
        allTickets.length;


    const open =
        allTickets.filter(
            ticket =>
                String(
                    ticket.ticket_status || ""
                ).toLowerCase() === "open"
        ).length;


    const highPriority =
        allTickets.filter(
            ticket =>
                String(
                    ticket.ticket_priority || ""
                ).toLowerCase() === "high"
        ).length;


    const ratings =
        allTickets
            .map(
                ticket =>
                    Number(
                        ticket.customer_satisfaction_rating
                    )
            )
            .filter(
                value =>
                    Number.isFinite(value)
            );


    let average = "-";


    if (ratings.length > 0) {

        const sum =
            ratings.reduce(
                (
                    total,
                    value
                ) =>
                    total + value,
                0
            );


        average =
            (
                sum / ratings.length
            ).toFixed(2);
    }


    const totalElement =
        document.getElementById(
            "totalTickets"
        );


    const openElement =
        document.getElementById(
            "openTickets"
        );


    const highElement =
        document.getElementById(
            "highPriorityTickets"
        );


    const averageElement =
        document.getElementById(
            "averageRating"
        );


    if (totalElement) {
        totalElement.textContent =
            total;
    }


    if (openElement) {
        openElement.textContent =
            open;
    }


    if (highElement) {
        highElement.textContent =
            highPriority;
    }


    if (averageElement) {
        averageElement.textContent =
            average;
    }
}


/* =========================================================
   CATEGORIAS
   ========================================================= */

function populateCategoryFilter() {

    const select =
        document.getElementById(
            "filterCategory"
        );


    if (!select) {
        return;
    }


    const categories =
        [
            ...new Set(
                allTickets
                    .map(
                        ticket =>
                            ticket.ticket_type
                    )
                    .filter(Boolean)
            )
        ];


    select.innerHTML = "";


    const defaultOption =
        document.createElement(
            "option"
        );


    defaultOption.value = "";

    defaultOption.textContent =
        "Todas as Categorias";


    select.appendChild(
        defaultOption
    );


    categories.forEach(
        category => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                category;

            option.textContent =
                category;


            select.appendChild(
                option
            );
        }
    );
}


/* =========================================================
   FILTROS
   ========================================================= */

function applyFilters() {

    const searchElement =
        document.getElementById(
            "filterSearch"
        );


    const categoryElement =
        document.getElementById(
            "filterCategory"
        );


    const priorityElement =
        document.getElementById(
            "filterPriority"
        );


    const statusElement =
        document.getElementById(
            "filterStatus"
        );


    const search =
        searchElement
            ? searchElement.value
                .trim()
                .toLowerCase()
            : "";


    const category =
        categoryElement
            ? categoryElement.value
            : "";


    const priority =
        priorityElement
            ? priorityElement.value
            : "";


    const status =
        statusElement
            ? statusElement.value
            : "";


    const filtered =
        allTickets.filter(
            ticket => {

                const id =
                    String(
                        ticket.id ?? ""
                    ).toLowerCase();


                const name =
                    String(
                        ticket.customer_name ?? ""
                    ).toLowerCase();


                const email =
                    String(
                        ticket.customer_email ?? ""
                    ).toLowerCase();


                const matchesSearch =
                    !search ||
                    id.includes(search) ||
                    name.includes(search) ||
                    email.includes(search);


                const matchesCategory =
                    !category ||
                    ticket.ticket_type ===
                        category;


                const matchesPriority =
                    !priority ||
                    ticket.ticket_priority ===
                        priority;


                const matchesStatus =
                    !status ||
                    ticket.ticket_status ===
                        status;


                return (
                    matchesSearch &&
                    matchesCategory &&
                    matchesPriority &&
                    matchesStatus
                );
            }
        );


    renderTickets(filtered);
}


/* =========================================================
   CÉLULA SEGURA
   ========================================================= */

function createCell(text) {

    const cell =
        document.createElement("td");


    if (
        text === null ||
        text === undefined ||
        text === ""
    ) {

        cell.textContent = "-";

    } else {

        cell.textContent =
            String(text);
    }


    return cell;
}


/* =========================================================
   BADGES
   ========================================================= */

function createBadge(
    text,
    className
) {

    const badge =
        document.createElement(
            "span"
        );


    badge.className =
        `badge ${className}`;


    badge.textContent =
        text || "-";


    return badge;
}


function getStatusClass(status) {

    const normalized =
        String(
            status || ""
        ).toLowerCase();


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


function getPriorityClass(
    priority
) {

    const normalized =
        String(
            priority || ""
        ).toLowerCase();


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

function renderTickets(
    tickets
) {

    const tableBody =
        document.getElementById(
            "ticketsTableBody"
        );


    if (!tableBody) {
        return;
    }


    tableBody.innerHTML = "";


    if (!tickets.length) {

        const row =
            document.createElement("tr");


        const cell =
            document.createElement("td");


        cell.colSpan = 7;

        cell.className =
            "empty";

        cell.textContent =
            "Nenhum ticket encontrado.";


        row.appendChild(cell);

        tableBody.appendChild(row);

        return;
    }


    tickets.forEach(
        ticket => {

            const row =
                document.createElement(
                    "tr"
                );


            /*
             * Abre os detalhes
             * ao clicar na linha.
             */

            row.addEventListener(
                "click",
                () => {

                    openTicketDetails(
                        ticket
                    );
                }
            );


            /*
             * ID
             */

            row.appendChild(
                createCell(
                    `#${ticket.id}`
                )
            );


            /*
             * CLIENTE
             */

            row.appendChild(
                createCell(
                    ticket.customer_name
                )
            );


            /*
             * ASSUNTO
             */

            row.appendChild(
                createCell(
                    ticket.ticket_subject
                )
            );


            /*
             * CATEGORIA
             */

            row.appendChild(
                createCell(
                    ticket.ticket_type
                )
            );


            /*
             * STATUS
             */

            const statusCell =
                document.createElement(
                    "td"
                );


            statusCell.appendChild(
                createBadge(
                    ticket.ticket_status,
                    getStatusClass(
                        ticket.ticket_status
                    )
                )
            );


            row.appendChild(
                statusCell
            );


            /*
             * PRIORIDADE
             */

            const priorityCell =
                document.createElement(
                    "td"
                );


            priorityCell.appendChild(
                createBadge(
                    ticket.ticket_priority,
                    getPriorityClass(
                        ticket.ticket_priority
                    )
                )
            );


            row.appendChild(
                priorityCell
            );


            /*
             * AVALIAÇÃO
             */

            const ratingCell =
                document.createElement(
                    "td"
                );


            if (
                ticket.customer_satisfaction_rating !==
                    null &&
                ticket.customer_satisfaction_rating !==
                    undefined
            ) {

                ratingCell.textContent =
                    `⭐ ${ticket.customer_satisfaction_rating}`;

            } else {

                ratingCell.textContent =
                    "-";
            }


            row.appendChild(
                ratingCell
            );


            tableBody.appendChild(
                row
            );
        }
    );
}


/* =========================================================
   NOVO TICKET
   ========================================================= */

function closeModal() {

    if (!ticketModal) {
        return;
    }


    ticketModal.style.display =
        "none";


    const form =
        document.getElementById(
            "ticketForm"
        );


    if (form) {
        form.reset();
    }
}


async function createTicket(
    event
) {

    event.preventDefault();

    hideError();


    const saveButton =
        document.getElementById(
            "saveTicketButton"
        );


    const purchaseDate =
        document.getElementById(
            "date_of_purchase"
        ).value;


    const ageValue =
        document.getElementById(
            "customer_age"
        ).value;


    const ratingValue =
        document.getElementById(
            "customer_satisfaction_rating"
        ).value;


    const payload = {

        customer_name:
            document.getElementById(
                "customer_name"
            ).value.trim(),


        customer_email:
            document.getElementById(
                "customer_email"
            ).value.trim(),


        customer_age:
            ageValue
                ? Number(ageValue)
                : null,


        customer_gender:
            document.getElementById(
                "customer_gender"
            ).value || null,


        product_purchased:
            document.getElementById(
                "product_purchased"
            ).value.trim() || null,


        date_of_purchase:
            purchaseDate
                ? `${purchaseDate}T00:00:00`
                : null,


        ticket_type:
            document.getElementById(
                "ticket_type"
            ).value.trim() || null,


        ticket_subject:
            document.getElementById(
                "ticket_subject"
            ).value.trim(),


        ticket_description:
            document.getElementById(
                "ticket_description"
            ).value.trim() || null,


        ticket_status:
            document.getElementById(
                "ticket_status"
            ).value || "Open",


        ticket_priority:
            document.getElementById(
                "ticket_priority"
            ).value || null,


        ticket_channel:
            document.getElementById(
                "ticket_channel"
            ).value.trim() || null,


        first_response_time:
            null,


        time_to_resolution:
            null,


        resolution:
            null,


        customer_satisfaction_rating:
            ratingValue
                ? Number(ratingValue)
                : null
    };


    if (
        !payload.customer_name ||
        !payload.customer_email ||
        !payload.ticket_subject
    ) {

        showError(
            "Nome, e-mail e assunto são obrigatórios."
        );

        return;
    }


    if (saveButton) {

        saveButton.disabled =
            true;

        saveButton.textContent =
            "Salvando...";
    }


    try {

        const response =
            await fetch(
                "/tickets",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        ...getAuthHeaders()
                    },

                    body:
                        JSON.stringify(
                            payload
                        )
                }
            );


        if (response.status === 401) {

            redirectToLogin();

            return;
        }


        let data = {};


        try {

            data =
                await response.json();

        } catch {

            data = {};
        }


        if (!response.ok) {

            let errorText =
                "Não foi possível criar o ticket.";


            if (data.detail) {

                if (
                    Array.isArray(
                        data.detail
                    )
                ) {

                    errorText =
                        data.detail
                            .map(
                                error =>
                                    error.msg ||
                                    "Campo inválido"
                            )
                            .join("; ");

                } else {

                    errorText =
                        String(
                            data.detail
                        );
                }
            }


            showError(
                errorText
            );

            return;
        }


        closeModal();

        await fetchTickets();


    } catch (error) {

        console.error(
            "Erro ao criar ticket:",
            error
        );


        showError(
            "Erro de conexão com a API."
        );


    } finally {

        if (saveButton) {

            saveButton.disabled =
                false;

            saveButton.textContent =
                "Salvar Ticket";
        }
    }
}


/* =========================================================
   DETALHES DO TICKET
   ========================================================= */

function formatValue(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "Não informado";
    }


    return String(value);
}


function formatDate(value) {

    if (!value) {

        return "Não informado";
    }


    const date =
        new Date(value);


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return formatValue(
            value
        );
    }


    return date.toLocaleString(
        "pt-BR"
    );
}


function formatRating(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return "Não avaliado";
    }


    return `${value} ⭐`;
}


function openTicketDetails(
    ticket
) {

    const ticketId =
        document.getElementById(
            "detailsTicketId"
        );


    const ticketSubject =
        document.getElementById(
            "detailsTicketSubject"
        );


    const statusElement =
        document.getElementById(
            "detailsTicketStatus"
        );


    const priorityElement =
        document.getElementById(
            "detailsTicketPriority"
        );


    if (ticketId) {

        ticketId.textContent =
            formatValue(
                ticket.id
            );
    }


    if (ticketSubject) {

        ticketSubject.textContent =
            formatValue(
                ticket.ticket_subject
            );
    }


    if (statusElement) {

        statusElement.textContent =
            formatValue(
                ticket.ticket_status
            );


        statusElement.className =
            `badge ${getStatusClass(
                ticket.ticket_status
            )}`;
    }


    if (priorityElement) {

        priorityElement.textContent =
            formatValue(
                ticket.ticket_priority
            );


        priorityElement.className =
            `badge ${getPriorityClass(
                ticket.ticket_priority
            )}`;
    }


    setDetailText(
        "detailsTicketRating",
        formatRating(
            ticket.customer_satisfaction_rating
        )
    );


    setDetailText(
        "detailsCustomerName",
        formatValue(
            ticket.customer_name
        )
    );


    setDetailText(
        "detailsCustomerEmail",
        formatValue(
            ticket.customer_email
        )
    );


    setDetailText(
        "detailsCustomerAge",
        formatValue(
            ticket.customer_age
        )
    );


    setDetailText(
        "detailsCustomerGender",
        formatValue(
            ticket.customer_gender
        )
    );


    setDetailText(
        "detailsProduct",
        formatValue(
            ticket.product_purchased
        )
    );


    setDetailText(
        "detailsTicketType",
        formatValue(
            ticket.ticket_type
        )
    );


    setDetailText(
        "detailsTicketChannel",
        formatValue(
            ticket.ticket_channel
        )
    );


    setDetailText(
        "detailsPurchaseDate",
        formatDate(
            ticket.date_of_purchase
        )
    );


    setDetailText(
        "detailsSubject",
        formatValue(
            ticket.ticket_subject
        )
    );


    setDetailText(
        "detailsDescription",
        formatValue(
            ticket.ticket_description
        )
    );


    setDetailText(
        "detailsFirstResponse",
        formatDate(
            ticket.first_response_time
        )
    );


    setDetailText(
        "detailsResolutionTime",
        formatDate(
            ticket.time_to_resolution
        )
    );


    setDetailText(
        "detailsResolution",
        formatValue(
            ticket.resolution
        )
    );


    setDetailText(
        "detailsUserId",
        formatValue(
            ticket.user_id
        )
    );


    setDetailText(
        "detailsCreatedAt",
        formatDate(
            ticket.created_at
        )
    );


    const modal =
        document.getElementById(
            "ticketDetailsModal"
        );


    if (modal) {

        modal.style.display =
            "block";
    }
}


/* =========================================================
   FUNÇÃO AUXILIAR PARA PREENCHER DETALHES
   ========================================================= */

function setDetailText(
    elementId,
    value
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {
        return;
    }


    element.textContent =
        value;
}


/* =========================================================
   FECHAR DETALHES
   ========================================================= */

function closeTicketDetails() {

    const modal =
        document.getElementById(
            "ticketDetailsModal"
        );


    if (!modal) {
        return;
    }


    modal.style.display =
        "none";
}


/* =========================================================
   INICIALIZAÇÃO
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        const token =
            getToken();


        if (!token) {

            redirectToLogin();

            return;
        }


        /* =================================================
           NOVO TICKET
           ================================================= */

        ticketModal =
            document.getElementById(
                "ticketModal"
            );


        const newTicketButton =
            document.getElementById(
                "newTicketButton"
            );


        if (
            newTicketButton &&
            ticketModal
        ) {

            newTicketButton.addEventListener(
                "click",
                function() {

                    ticketModal.style.display =
                        "block";
                }
            );
        }


        const closeModalButton =
            document.getElementById(
                "closeModalButton"
            );


        if (closeModalButton) {

            closeModalButton.addEventListener(
                "click",
                closeModal
            );
        }


        const cancelModalButton =
            document.getElementById(
                "cancelModalButton"
            );


        if (cancelModalButton) {

            cancelModalButton.addEventListener(
                "click",
                closeModal
            );
        }


        const ticketForm =
            document.getElementById(
                "ticketForm"
            );


        if (ticketForm) {

            ticketForm.addEventListener(
                "submit",
                createTicket
            );
        }


        /* =================================================
           MODAL DETALHES
           ================================================= */

        const ticketDetailsModal =
            document.getElementById(
                "ticketDetailsModal"
            );


        const closeTicketDetailsButton =
            document.getElementById(
                "closeTicketDetailsButton"
            );


        const closeTicketDetailsX =
            document.getElementById(
                "closeTicketDetails"
            );


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

            ticketDetailsModal.addEventListener(
                "click",
                function(event) {

                    if (
                        event.target ===
                        ticketDetailsModal
                    ) {

                        closeTicketDetails();
                    }
                }
            );
        }


        /* =================================================
           ESC
           ================================================= */

        document.addEventListener(
            "keydown",
            function(event) {

                if (
                    event.key !==
                    "Escape"
                ) {

                    return;
                }


                closeTicketDetails();


                if (
                    ticketModal &&
                    ticketModal.style.display ===
                        "block"
                ) {

                    closeModal();
                }
            }
        );


        /* =================================================
           FILTROS
           ================================================= */

        const filterSearch =
            document.getElementById(
                "filterSearch"
            );


        const filterCategory =
            document.getElementById(
                "filterCategory"
            );


        const filterPriority =
            document.getElementById(
                "filterPriority"
            );


        const filterStatus =
            document.getElementById(
                "filterStatus"
            );


        if (filterSearch) {

            filterSearch.addEventListener(
                "input",
                applyFilters
            );
        }


        if (filterCategory) {

            filterCategory.addEventListener(
                "change",
                applyFilters
            );
        }


        if (filterPriority) {

            filterPriority.addEventListener(
                "change",
                applyFilters
            );
        }


        if (filterStatus) {

            filterStatus.addEventListener(
                "change",
                applyFilters
            );
        }


        /* =================================================
           LOGOUT
           ================================================= */

        const logoutButton =
            document.getElementById(
                "logoutButton"
            );


        if (logoutButton) {

            logoutButton.addEventListener(
                "click",
                function() {

                    localStorage.removeItem(
                        "access_token"
                    );

                    window.location.href =
                        "/login";
                }
            );
        }


        /* =================================================
           FECHAR NOVO TICKET AO CLICAR FORA
           ================================================= */

        if (ticketModal) {

            ticketModal.addEventListener(
                "click",
                function(event) {

                    if (
                        event.target ===
                        ticketModal
                    ) {

                        closeModal();
                    }
                }
            );
        }


        /* =================================================
           CARREGAR TICKETS
           ================================================= */

        fetchTickets();

    }
);