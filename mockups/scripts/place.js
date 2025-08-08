import { fetchData } from './fetch.js';
import { getImages, toFixed } from './utils.js';

const titleElement = document.querySelector('.place-title');
const slideElement = document.querySelector('.splide__list');
const ownerElement = document.querySelector('.owner-name');
const descElement = document.querySelector('.place-description');
const priceElement = document.querySelector('.place-price span');
const amenitiesElement = document.querySelector('.place-amenities');
const nightElements = document.querySelectorAll('.place-night');
const totalElement = document.querySelector('.place-total span');
const ratingElements = document.querySelectorAll('.review-rating');
const reserveElement = document.querySelector('.place-reserve');

let nights = 1;
let price = 0;
let rating = 0;

const onPageLoad = async () => {
	const place_id = new URL(window.location.href).searchParams.get('place_id');
	const data = await fetchData(place_id, `/places/${place_id}`);

	console.log(data);

	const images = getImages(5);

	price = toFixed(data.price * nights);
	titleElement.textContent = data.title;
	ownerElement.textContent = `${data.user.first_name} ${data.user.last_name}`;
	descElement.textContent = data.description;
	priceElement.textContent = `$${price}`;
	totalElement.textContent = `$${toFixed(data.price * nights)}`;

	images.forEach((img) => {
		const li = document.createElement('li');
		li.classList.add('splide__slide');

		const image = document.createElement('img');
		image.src = img;

		li.append(image);

		slideElement.append(li);
	});

	new Splide('.splide').mount();

	data.amenities.forEach((amenity) => {
		const el = document.createElement('li');
		el.textContent = amenity;
		el.classList.add('place-amenity');

		amenitiesElement.append(el);
	});

	nightElements.forEach((button) => {
		button.addEventListener('click', (e) => {
			nights = parseInt(e.target.textContent);
			price = toFixed(data.price * nights);
			totalElement.textContent = `$${toFixed(data.price * nights)}`;

			nightElements.forEach((btn) => btn.classList.remove('selected'));
			e.target.classList.add('selected');
		});
	});

	ratingElements.forEach((button) => {
		button.addEventListener('click', (e) => {
			rating = parseInt(e.target.textContent);

			ratingElements.forEach((btn) => btn.classList.remove('selected'));
			e.target.classList.add('selected');
		});
	});

	reserveElement.addEventListener('click', () => {
		alert(`You reserved: ${data.title} for ${nights} night${nights > 1 ? 's' : ''}, totaling for: ${price}`);
	});
};

onPageLoad();
