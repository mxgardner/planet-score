const materialKeywords = {
    "Aluminum": ["aluminum", "metal bottle", "aluminium"],
    "Plastic": ["plastic", "bpa-free", "polymer"],
    "Steel": ["steel", "stainless", "metal"],
    "Glass": ["glass", "jar", "crystal"],
    "Wood": ["wood", "bamboo", "timber"],
    "Iron": ["iron", "cast iron", "skillet"],
    "Leather": ["leather", "hide", "genuine leather"],
    "Oil": ["oil", "petroleum", "crude oil"]
};

const productTitle = document.querySelector("#productTitle")?.innerText.trim();
const priceWhole = document.querySelector(".a-price-whole")?.innerText.trim() || '';
const priceFraction = document.querySelector(".a-price-fraction")?.innerText.trim() || '';
const price = `${priceWhole.replace(/[^\d]/g, '')}.${priceFraction.replace(/[^\d]/g, '')}`.replace(/^\./, '') || null;

let matchedMaterial = null;
if (productTitle) {
    for (const [material, keywords] of Object.entries(materialKeywords)) {
        if (keywords.some(keyword => productTitle.toLowerCase().includes(keyword))) {
            matchedMaterial = material;
            break;
        }
    }
}

chrome.runtime.sendMessage(
    {
        productTitle,
        price,
        material: matchedMaterial,
    },
    (response) => {
        console.log("PlanetScore: Response from background.js:", response);
    }
);

console.log("PlanetScore: Scraped Product Title:", productTitle);
console.log("PlanetScore: Scraped Price:", price);
console.log("PlanetScore: Matched Material:", matchedMaterial);
