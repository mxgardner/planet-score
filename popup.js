document.addEventListener('DOMContentLoaded', () => {
    const resultDiv = document.getElementById('result');

    const displayMessage = (message, isError = false) => {
        resultDiv.textContent = message;
        resultDiv.style.color = isError ? 'red' : 'green';
    };

    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        console.log("Popup: Received message from background.js:", message);

        if (!message || typeof message.success === "undefined") {
            displayMessage("Unexpected error occurred. No valid response received.", true);
            return;
        }

        if (message.success) {
            displayMessage(
                `Product: ${message.productName}\nMaterial: ${message.material}\nEstimated GWP: ${message.gwp} kg CO₂`
            );
        } else {
            const errorMessage = message.error || "An unknown error occurred.";
            console.error("Popup: Error in received message:", errorMessage);
            displayMessage(`Error: ${errorMessage}`, true);
        }

        sendResponse({ received: true });
    });

    setTimeout(() => {
        if (resultDiv.textContent === 'Waiting for GWP data...') {
            displayMessage("No data received. Please refresh the product page.", true);
        }
    }, 5000);

    displayMessage('Waiting for GWP data...');
});


