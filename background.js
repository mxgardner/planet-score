chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("PlanetScore: Message received in background.js:", message);

    if (message.action && message.action !== "getGWP") {
        console.warn("PlanetScore: Ignoring unrelated action message:", message.action);
        return true;
    }

    if (!message.productTitle || !message.price || !message.material) {
        console.error("PlanetScore: Ignoring incomplete 'getGWP' message:", message);
        sendResponse({ success: false, error: "Incomplete message received." });
        return true;
    }

    const { productTitle, price, material } = message;
    console.log("PlanetScore: Extracted message data:", { productTitle, price, material });

    if (!database) {
        console.error("PlanetScore: Database is not loaded yet.");
        sendResponse({
            success: false,
            error: "Database is not ready. Please try again shortly.",
        });
        return true;
    }

    console.log("PlanetScore: Database is ready. Looking up material:", material);

    const gwpPerEuro = findGWP(material);

    if (gwpPerEuro) {
        const estimatedGWP = (price * gwpPerEuro).toFixed(2);
        console.log(`PlanetScore: GWP/kg CO₂ per Euro: ${gwpPerEuro}`);
        console.log(`PlanetScore: Estimated GWP: ${estimatedGWP}`);
        sendResponse({
            success: true,
            productName: productTitle,
            material,
            gwp: estimatedGWP,
        });
    } else {
        console.error("PlanetScore: No GWP value found for material:", material);
        sendResponse({
            success: false,
            error: "Material not found in GWP database.",
        });
    }

    return true;
});


