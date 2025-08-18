import { fetchData, sendData } from './fetch.js';
import { getImages, toFixed } from './utils.js';

const place_id = new URL(window.location.href).searchParams.get('place_id');

const titleElement = document.querySelector('.place-title');
const slideElement = document.querySelector('.splide__list');
const ownerElement = document.querySelector('.owner-name');
const descElement = document.querySelector('.place-description');
const priceElement = document.querySelector('.place-price span');
const amenitiesElement = document.querySelector('.place-amenities');
const nightElements = document.querySelectorAll('.place-night');
const totalElement = document.querySelector('.place-total span');
const ratingElements = document.querySelectorAll('.review-form-rating');
const finalRatingElement = document.querySelector('.review-final-rating');
const reserveElement = document.querySelector('.place-reserve');
const reviewFormElement = document.querySelector('.review-form');
const reviewsElement = document.querySelector('.reviews');

let nights = 1;
let price = 0;
let rating = 0;

/**
 * @param {SubmitEvent} e
 */
const addReview = async (e) => {
	e.preventDefault();

	const text = e.target.text.value;
	const rating = parseInt(e.target.rating.value);

	if (!text.trim().length) {
		alert('Message cannot be blank');
		return;
	}
	if (!rating || rating <= 0 || rating > 5) {
		alert('Review rating must be in the range of 1 - 5');
		return;
	}

	const req = await sendData('/reviews', {
		body: {
			text,
			rating,
			place_id
		}
	});

	if (req.ok) {
		e.target.text.value = '';
		e.target.rating.value = '';
		ratingElements.forEach((el) => el.classList.remove('selected'));

		appendReview(req.body);
	}
};

const appendReview = (data) => {
	const reviewElement = document.createElement('div');
	reviewElement.classList.add('review');
	reviewElement.innerHTML = `
		 	<div class="review-content">
				<span class="review-username">${data.author.first_name} ${data.author.last_name}</span>
				<p class="review-message">${data.text}</p>
			</div>
			<div class="review-rating">${data.rating}</div>
		`;

	reviewsElement.append(reviewElement);
};

const onPageLoad = async () => {
	const data = await fetchData(place_id, `/places/${place_id}`);

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
			finalRatingElement.value = rating;

			ratingElements.forEach((btn) => btn.classList.remove('selected'));
			e.target.classList.add('selected');
		});
	});

	reserveElement.addEventListener('click', () => {
		alert(`You reserved: ${data.title} for ${nights} night${nights > 1 ? 's' : ''}, totaling for: $${price}`);
	});

	reviewFormElement.addEventListener('submit', addReview);

	data.reviews.forEach((review) => appendReview(review));
};

onPageLoad();
