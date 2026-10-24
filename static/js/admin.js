const pageMessage = document.getElementById("pageMessage");

function showMessage(message, type = "success") {
    if (!pageMessage) return;

    pageMessage.textContent = message;
    pageMessage.className = `message ${type}`;
    pageMessage.hidden = false;
}

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        credentials: "same-origin",
        ...options,
    });

    if (response.status === 401 || response.status === 403) {
        window.location.assign("/admin/login");
        throw new Error("Sessão expirada ou sem permissão.");
    }

    if (response.status === 204) {
        return {};
    }

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(
            data.detail || `Erro HTTP ${response.status}`
        );
    }

    return data;
}

const FIELD_MAP = {
    site_name: "siteName",
    brand_name: "brandName",
    tagline: "tagline",
    description: "description",
    hero_title: "heroTitle",
    hero_description: "heroDescription",
    contact_email: "contactEmail",
    support_url: "supportUrl",
    logo_url: "logoUrl",
    hero_image_url: "heroImageUrl",
    primary_color: "primaryColor",
    primary_dark_color: "primaryDarkColor",
    accent_color: "accentColor",
};

function fillForm(data) {
    for (const [key, elementId] of Object.entries(FIELD_MAP)) {
        const element = document.getElementById(elementId);

        if (
            element &&
            data[key] !== undefined &&
            data[key] !== null
        ) {
            element.value = data[key];
        }
    }

    updateImagePreview("logoUrl", "logoPreview");
    updateImagePreview("heroImageUrl", "heroImagePreview");
}

function updateImagePreview(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);

    if (!input || !preview) return;

    const url = input.value.trim();

    preview.replaceChildren();

    if (!url) {
        preview.hidden = true;
        return;
    }

    const image = document.createElement("img");
    image.src = url;
    image.alt = "Pré-visualização da imagem";
    image.loading = "lazy";

    image.addEventListener("error", () => {
        preview.textContent = "Não foi possível carregar esta imagem.";
    });

    preview.appendChild(image);
    preview.hidden = false;
}

async function loadSettings() {
    try {
        const data = await apiRequest("/admin/api/settings");
        fillForm(data);
    } catch (error) {
        showMessage(error.message, "error");
    }
}

async function saveSettings(event, fieldPairs) {
    event.preventDefault();

    const form = event.currentTarget;
    const payload = {};

    for (const [elementId, key] of fieldPairs) {
        const element = document.getElementById(elementId);

        if (element) {
            payload[key] =
                element.value.trim();
        }
    }

    const button = event.submitter;

    if (button) button.disabled = true;

    try {
        const data = await apiRequest("/admin/api/settings", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        fillForm(data);
        showMessage("Alterações salvas com sucesso.");
    } catch (error) {
        showMessage(error.message, "error");
    } finally {
        if (button) button.disabled = false;
    }
}

document.getElementById("settingsForm")?.addEventListener(
    "submit",
    (event) => saveSettings(event, [
        ["siteName", "site_name"],
        ["tagline", "tagline"],
        ["description", "description"],
        ["contactEmail", "contact_email"],
        ["supportUrl", "support_url"],
    ])
);

document.getElementById("contentForm")?.addEventListener(
    "submit",
    (event) => saveSettings(event, [
        ["heroTitle", "hero_title"],
        ["heroDescription", "hero_description"],
    ])
);

document.getElementById("brandingForm")?.addEventListener(
    "submit",
    (event) => saveSettings(event, [
        ["brandName", "brand_name"],
        ["logoUrl", "logo_url"],
        ["heroImageUrl", "hero_image_url"],
        ["primaryColor", "primary_color"],
        ["primaryDarkColor", "primary_dark_color"],
        ["accentColor", "accent_color"],
    ])
);

document.getElementById("logoUrl")?.addEventListener(
    "input",
    () => updateImagePreview("logoUrl", "logoPreview")
);

document.getElementById("heroImageUrl")?.addEventListener(
    "input",
    () => updateImagePreview("heroImageUrl", "heroImagePreview")
);

document.getElementById("uploadForm")?.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const fileInput = document.getElementById("imageFile");
        const targetInput = document.getElementById("imageTarget");
        const file = fileInput?.files?.[0];

        if (!file) {
            showMessage("Selecione uma imagem primeiro.", "error");
            return;
        }

        const allowedTypes = [
            "image/png",
            "image/jpeg",
            "image/webp",
        ];

        const maxSize = 5 * 1024 * 1024;

        if (!allowedTypes.includes(file.type)) {
            showMessage("Formato inválido. Use PNG, JPG ou WEBP.", "error");
            return;
        }

        if (file.size > maxSize) {
            showMessage("A imagem deve ter no máximo 5 MB.", "error");
            return;
        }

        const button = document.getElementById("uploadButton");
        if (button) button.disabled = true;

        try {
            const formData = new FormData();
            formData.append("file", file);

            const result = await apiRequest("/admin/api/upload", {
                method: "POST",
                body: formData,
            });

            if (!result.url) {
                throw new Error("O servidor não retornou o endereço da imagem.");
            }

            const target = targetInput?.value || "logo_url";
            const targetElementId = FIELD_MAP[target];

            if (!targetElementId) {
                throw new Error("Destino da imagem inválido.");
            }

            const targetElement = document.getElementById(targetElementId);

            if (targetElement) {
                targetElement.value = result.url;
            }

            if (target === "logo_url") {
                updateImagePreview("logoUrl", "logoPreview");
            } else if (target === "hero_image_url") {
                updateImagePreview("heroImageUrl", "heroImagePreview");
            }

            const uploadedPath = document.getElementById("uploadedImagePath");

            if (uploadedPath) {
                uploadedPath.textContent = `Imagem enviada: ${result.url}`;
            }

            fileInput.value = "";
            showMessage(
                "Imagem enviada. Salve a identidade visual para aplicar a alteração."
            );
        } catch (error) {
            showMessage(error.message, "error");
        } finally {
            if (button) button.disabled = false;
        }
    }
);

document.getElementById("logoutButton")?.addEventListener(
    "click",
    async () => {
        try {
            await apiRequest("/admin/logout", {
                method: "POST",
            });
        } catch (error) {
            showMessage(error.message, "error");
        } finally {
            window.location.assign("/admin/login");
        }
    }
);

loadSettings();