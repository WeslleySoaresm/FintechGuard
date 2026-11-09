"use strict";

document.addEventListener("DOMContentLoaded", () => {
    initializeMobileMenu();
    initializeFooterYear();
    loadPublicSettings();
});

/**
 * Abre e fecha o menu de navegação em telas pequenas.
 */
function initializeMobileMenu() {
    const menuButton = document.getElementById("menu-toggle");
    const navigation = document.getElementById("main-navigation");

    if (!menuButton || !navigation) {
        return;
    }

    menuButton.addEventListener("click", () => {
        const isOpen = navigation.classList.toggle("is-open");

        menuButton.setAttribute("aria-expanded", String(isOpen));
        menuButton.setAttribute(
            "aria-label",
            isOpen ? "Fechar menu" : "Abrir menu"
        );
        menuButton.textContent = isOpen ? "✕" : "☰";
    });

    navigation.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            navigation.classList.remove("is-open");
            menuButton.setAttribute("aria-expanded", "false");
            menuButton.setAttribute("aria-label", "Abrir menu");
            menuButton.textContent = "☰";
        });
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 760) {
            navigation.classList.remove("is-open");
            menuButton.setAttribute("aria-expanded", "false");
            menuButton.setAttribute("aria-label", "Abrir menu");
            menuButton.textContent = "☰";
        }
    });
}

/**
 * Mantém o ano do rodapé atualizado automaticamente.
 */
function initializeFooterYear() {
    const yearElement = document.getElementById("current-year");

    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

/**
 * Carrega as configurações publicadas pelo administrador.
 *
 * A API será implementada posteriormente no FastAPI.
 * Se ela ainda não existir ou estiver indisponível,
 * a página continuará exibindo o conteúdo padrão do HTML.
 */
async function loadPublicSettings() {
    try {
        const response = await fetch("/api/public/settings", {
            method: "GET",
            headers: {
                "Accept": "application/json"
            },
            credentials: "same-origin"
        });

        if (!response.ok) {
            return;
        }

        const settings = await response.json();

        if (!settings || typeof settings !== "object") {
            return;
        }

        applyPublicSettings(settings);
    } catch (error) {
        // A página permanece funcional com o conteúdo padrão.
        console.warn("Não foi possível carregar as configurações públicas.");
    }
}

/**
 * Atualiza somente os elementos previstos para conteúdo dinâmico.
 */
function applyPublicSettings(settings) {
    setText("site-name", settings.site_name);
    setText("hero-title", settings.hero_title);
    setText("hero-description", settings.hero_description);

    if (isValidHexColor(settings.primary_color)) {
        document.documentElement.style.setProperty(
            "--color-primary",
            settings.primary_color
        );
    }

    if (isValidHexColor(settings.primary_dark_color)) {
        document.documentElement.style.setProperty(
            "--color-primary-dark",
            settings.primary_dark_color
        );
    }

    if (isValidHexColor(settings.accent_color)) {
        document.documentElement.style.setProperty(
            "--color-accent",
            settings.accent_color
        );
    }

    setImage(
        "hero-image",
        settings.hero_image_url,
        "Imagem de apresentação do FintechGuard"
    );
}

/**
 * Altera o texto sem interpretar o conteúdo como HTML.
 */
function setText(elementId, value) {
    const element = document.getElementById(elementId);

    if (
        !element ||
        typeof value !== "string" ||
        !value.trim()
    ) {
        return;
    }

    element.textContent = value.trim();
}

/**
 * Aceita imagens do próprio site ou URLs HTTPS.
 */
function setImage(elementId, value, altText) {
    const image = document.getElementById(elementId);

    if (
        !image ||
        typeof value !== "string" ||
        !value.trim()
    ) {
        return;
    }

    const url = value.trim();

    const isLocalImage =
        url.startsWith("/static/uploads/") ||
        url.startsWith("/static/images/");

    let isHttpsImage = false;

    try {
        const parsedUrl = new URL(url);

        isHttpsImage =
            parsedUrl.protocol === "https:" &&
            !parsedUrl.username &&
            !parsedUrl.password;
    } catch {
        isHttpsImage = false;
    }

    if (!isLocalImage && !isHttpsImage) {
        console.warn("URL de imagem recusada por segurança.");
        return;
    }

    image.alt = altText;
    image.src = url;
    image.style.display = "";
}

/**
 * Valida cores hexadecimais como #155eef.
 */
function isValidHexColor(value) {
    return (
        typeof value === "string" &&
        /^#[0-9a-fA-F]{6}$/.test(value)
    );
}
