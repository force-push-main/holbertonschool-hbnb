import cBB from "./assets/country_bounding_boxes.json" with {type: 'json'};

let placeData = [];
let lastFetchTime;
const maxAgeMs = 300000;

const imgPaths = [];
const startingImgId = 0;
const endingImgId = 18;
for (let i = 0; i <= endingImgId; i++) {
    imgPaths.push(`./assets/hbnb-demo-imgs/demo-img-${i}.jpg`);
}

const fetchData = async (url) => {
    if (typeof lastFetchTime == 'undefined' || Date.now() - lastFetchTime > maxAgeMs) {
            const res = await fetch(url);
            if (!res.ok) {
                throw new Error(
                    `An error occured with status code: ${res.status}`
                );
            }
            const data = await res.json();
            placeData = data;
            lastFetchTime = Date.now()
    }
    return placeData;
};



// ----------- POPULATION ACTIONS AND PROPERTY TILES --------

// ------ place data retrieval and manipulation ------

const toTitleCase = (str) => {
    if (!str) return "";
    return str.toLowerCase().replace(/\b\w/g, (char) => char.toUpperCase());
};

const findLocation = (place) => {
    const long = place.longitude;
    const lat = place.latitude;
    let location = Object.keys(cBB).find(
        (key) =>
            lat > cBB[key][0] &&
            lat < cBB[key][2] &&
            long > cBB[key][1] &&
            long < cBB[key][3]
    );
    if (typeof location == "undefined") {
        location = "Waterfront views";
    }
    return toTitleCase(location);
};

const getRndImgs = () => {
    const srcArr = [];
    const currImgs = [];
    while (srcArr.length < 3) {
        const rndIndex = Math.floor(
            Math.random() * (endingImgId - startingImgId + 1) + startingImgId
        );
        if (!currImgs.includes(rndIndex)) {
            srcArr.push(imgPaths[rndIndex]);
            currImgs.push(rndIndex);
        }
    }
    return srcArr;
};

// ------- property tile creation -----------

const createPropertyTile = (place) => {
    const div = document.createElement("div");
    div.classList.add("property");
    div.innerHTML = `
        <div class="property-image">
            <div class="loading-dot-container">
                <div class="loading-dot dot-1"></div>
                <div class="loading-dot dot-2"></div>
                <div class="loading-dot dot-3"></div>
            </div>
        </div>
        <div class="property-text-container">
        <p><strong>${toTitleCase(place.title)}</strong></p>
        <p class="price">$${place.price}/night – ${findLocation(place)}</p>
        </div>`;
    return div;
};

const addImgToTile = (tile) => {
    const imgArr = getRndImgs();
    const img = new Image(300, 300);
    img.src = imgArr[0];
    img.onload = () => {
        const imgContainer = tile.querySelector(".property-image");
        imgContainer.innerHTML = "";
        imgContainer.appendChild(img);
    };
};

// ------ page population events -------

const populatePageOnLoad = async () => {
    const url = "http://127.0.0.1:5000/api/v1/places/";
    const places = await fetchData(url);
    const propertyContainer = document.querySelector(".properties-container");
    propertyContainer.innerHTML = "";
    places.forEach((place) => {
        const propertyTile = createPropertyTile(place);
        propertyContainer.appendChild(propertyTile);
    });
    const propertyTiles = document.querySelectorAll(".property");
    propertyTiles.forEach((tile) => {
        addImgToTile(tile);
    });
};

populatePageOnLoad();

const populatePage = (places) => {
    const propertyContainer = document.querySelector(".properties-container");
    propertyContainer.innerHTML = "";
    places.forEach((place) => {
        const propertyTile = createPropertyTile(place);
        propertyContainer.appendChild(propertyTile);
    });
    const propertyTiles = document.querySelectorAll(".property");
    propertyTiles.forEach((tile) => {
        addImgToTile(tile);
    });
};

// ------------ SEARCH BAR EVENTS ----------------

const searchBar = document.querySelector(".search-bar");
const suggestedResults = document.querySelector(".suggested-results");

// ----- search by country ------

const findWaterFrontProps = (places) => {
    let waterfront = [];
    places.forEach((place) => {
        const long = place.longitude;
        const lat = place.latitude;
        let location = Object.keys(cBB).find(
            (key) =>
                lat > cBB[key][0] &&
                lat < cBB[key][2] &&
                long > cBB[key][1] &&
                long < cBB[key][3]
        );
        if (typeof location == "undefined") {
            waterfront.push(place);
        }
    });
    return waterfront;
};

const handleSearch = async () => {
    const searchedCountry = cBB[searchBar.value.toLowerCase()];
    const url = "http://127.0.0.1:5000/api/v1/places/";
    const allPlaces = await fetchData(url);
    let filteredResults;
    if (searchBar.value.toLowerCase() == "waterfront views") {
        filteredResults = findWaterFrontProps(allPlaces);
    } else {
        filteredResults = allPlaces.filter(
            (place) =>
                place["latitude"] > searchedCountry[0] &&
                place["latitude"] < searchedCountry[2] &&
                place["longitude"] > searchedCountry[1] &&
                place["longitude"] < searchedCountry[3]
        );
    }
    suggestedResults.innerHTML = "";
    if (filteredResults.length > 0) {
        populatePage(filteredResults);
    } else {
        const propertyContainer = document.querySelector(
            ".properties-container"
        );
        propertyContainer.innerHTML =
            "<h2>There are no results for that country</h2>";
    }
};

searchBar.addEventListener("search", handleSearch);

// ----- auto-complete ----

const handleAutoComplete = () => {
    suggestedResults.innerHTML = "";
    if (searchBar.value.length > 2) {
        const countries = Object.keys(cBB).filter((value) => {
            return value.includes(searchBar.value.toLowerCase());
        });
        if (countries.length > 0) {
            const ul = document.createElement("ul");
            countries.forEach((country) => {
                const li = document.createElement("li");
                li.textContent = toTitleCase(country);
                li.addEventListener("click", () => {
                    searchBar.value = li.textContent;
                    suggestedResults.innerHTML = "";
                    handleSearch();
                });
                ul.appendChild(li);
            });
            suggestedResults.appendChild(ul);
        }
    }
};

searchBar.addEventListener("input", handleAutoComplete);

// ---------- FILTERS ------------

// ----- price slider -----

const priceSlider = document.querySelector(".price-range-slider");

const handlePriceSlider = () => {
    const priceSelection = document.querySelector(".price-range-selection");
    const priceValue = priceSlider.value;
    if (priceValue == 125) {
        priceSelection.textContent = "Any";
    } else {
        priceSelection.textContent = `$${priceValue}`;
    }
};

priceSlider.addEventListener("input", handlePriceSlider);

// ----- confirm price range -----

const confirmPriceRangeBtn = document.querySelector(".price-range-confirm-btn");

const handlePriceRange = () => {
    const maxPrice =
        parseInt(priceSlider.value) < 125
            ? parseInt(priceSlider.value)
            : Infinity;
    const properties = document.querySelectorAll(".property");
    properties.forEach((property) => {
        const price = parseFloat(
            property.querySelector(".price").textContent.replace(/[$,]/g, "")
        );
        property.style.display = price <= maxPrice ? "flex" : "none";
    });
};

confirmPriceRangeBtn.addEventListener("click", handlePriceRange);

// ----- sort by price -----

const sortByPriceSelector = document.querySelector(".order-by-price-input");

const sortByPriceHelper = (order) => {
    const properties = Array.from(document.querySelectorAll(".property")).map(
        (el) => ({
            element: el,
            price: parseFloat(
                el.querySelector(".price").textContent.replace(/[$,]/g, "")
            ),
        })
    );
    properties.sort((a, b) =>
        order == "desc" ? b.price - a.price : a.price - b.price
    );
    const container = document.querySelector(".properties-container");
    properties.forEach((property) => container.appendChild(property.element));
};

const handleSortByPrice = () => {
    const value = sortByPriceSelector.value;
    if (value === "low-to-high") {
        sortByPriceHelper("asc");
    } else {
        sortByPriceHelper("desc");
    }
};

sortByPriceSelector.addEventListener("input", handleSortByPrice);



// ------------ PAGINATION ---------------
