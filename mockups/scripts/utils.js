import { TOKEN } from './constants.js';

/**
 * Gets a random set of images from the `asset` folder.
 * @param {number} imgCount The number of images to get
 * @returns {string[]}
 */
export const getImages = (imgCount = 1) => {
	const start = 1;
	const end = 18;
	const imgs = [];

	for (let i = 1; i <= imgCount; i++) {
		const rndIndex = Math.floor(Math.random() * (end - start) + start);
		imgs.push(`./assets/hbnb-demo-imgs/demo-img-${rndIndex}.jpg`);
	}

	return imgs;
};

/**
 * Converts a string to title-case.
 * @param {string} str The string to convert
 * @returns {string} The converted string
 */
export const toTitleCase = (str) => {
	if (!str) return '';
	return str.toLowerCase().replace(/\b\w/g, (char) => char.toUpperCase());
};

/**
 * Converts a string number (if available) and fixes it to 2 decimal points.
 * @param {number | string} num The number convert & fix.
 * @returns {number}
 */
export const toFixed = (num) => {
	return (typeof num === 'number' ? num : parseInt(num)).toFixed(2);
};

export const getJWT = () => {
	const token = localStorage.getItem(TOKEN);

	const payloadBase64url = token.split('.')[1];

	const decodedPayload = atob(
		payloadBase64url.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((payloadBase64url.length * 4) % 3)
	);

	return JSON.parse(decodedPayload);
};

export const isJwtExpired = () => {
	const token = localStorage.getItem(TOKEN);
	if (!token) return true;

	const data = getJWT();

	return data.exp < Date.now() / 1000;
};
