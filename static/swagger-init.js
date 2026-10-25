window.addEventListener("load", function () {
    SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: "#swagger-ui",
        deepLinking: true,
        showExtensions: true,
        showCommonExtensions: true
    });
});