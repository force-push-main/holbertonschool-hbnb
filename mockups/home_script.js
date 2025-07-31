import cBB from "./assets/country_bounding_boxes.json" with {type: 'json'};

const testPlace = [
    {
        id: "d98555ab-e9c0-493c-9015-b80b5d7e13fd",
        title: "Cozy Apartment",
        description: "A nice place to stay",
        price: 70,
        latitude: 153.56,
        longitude: -10.68,
        user_id: "f247995d-7b5a-44e8-ab64-a8442a66f422",
        amenities: ["Kitchen", "Wifi", "pool"],
    },
    {
        id: "d98555ab-e9c0-493c-9015-b80b5d7e13fd",
        title: "An uncomfortable apartment",
        description: "A terrible place to stay",
        price: 180,
        latitude: 153.56,
        longitude: -10.68,
        user_id: "f247995d-7b5a-44e8-ab64-a8442a66f422",
        amenities: ["Kitchen", "Wifi", "pool"],
    },
];

const fetchData = async (url) => {
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error(`An error occured with status code: ${res.status}`);
    }
    const data = await res.json();
    return data;
    return testPlace;
};

const createPropertyTile = (place) => {
    const div = document.createElement("div");
    div.classList.add("property");
    div.innerHTML = `<div class="property-image">
                    Image
                </div>
                <div class="property-text-container">
                    <p><strong>${place.title}</strong></p>
                    <p class="price">$${place.price}/night – 4.45 stars</p>
                </div>`;
    return div;
};

const populatePageOnLoad = async () => {
    const url = "http://127.0.0.1:5000/api/v1/places/";
    const places = await fetchData(url);
    const propertyContainer = document.querySelector(".properties-container");
    places.forEach((place) => {
        const propertyTile = createPropertyTile(place);
        propertyContainer.appendChild(propertyTile);
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
};

// ------------ SEARCH BAR ----------------

const searchBar = document.querySelector(".search-bar");
const suggestedResults = document.querySelector("#suggested-results");

// ----- search by country ------

const handleSearch = async () => {
    const searchedCountry = cBB[searchBar.value];
    const url = "http://127.0.0.1:5000/api/v1/places/";
    const allPlaces = await fetchData(url);
    suggestedResults.innerHTML = "";
    const filteredResults = allPlaces.filter((place) => {
        const placeLatitude = place["latitude"];
        const placeLongitude = place["longitude"];
        if (
            placeLatitude > searchedCountry[0] &&
            placeLatitude < searchedCountry[2] &&
            placeLongitude > searchedCountry[1] &&
            placeLongitude < searchedCountry[3]
        ) {
            return true;
        }
        return false;
    });
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
                li.textContent = country;
                li.addEventListener("click", function () {
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
    const maxPrice = parseInt(priceSlider.value) < 125 ? parseInt(priceSlider.value) : Infinity;
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

const sortPropertiesByPrice = (order) => {
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

const handleSortBy = () => {
    const value = sortByPriceSelector.value;
    if (value === "low-to-high") {
        sortPropertiesByPrice("desc");
    } else {
        sortPropertiesByPrice("asc");
    }
};

sortByPriceSelector.addEventListener("input", handleSortBy);
