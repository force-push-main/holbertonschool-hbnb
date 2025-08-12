import { API_URL, MAX_AGE_MS, TOKEN } from './constants.js';

let results = {};

/**
 * Formats the URL to prepend `/` if not found.
 * @param {string} url The URL to format.
 */
const formatPath = (url) => {
	return url.startsWith('/') ? url : '/' + url;
};

/**
 * Simple fetch wrapper that returns cached result.
 * @param {string} page The unique ID used when caching the results
 * @param {string} url The URL path for the API.
 * @returns {any}
 */
export const fetchData = async (page, url) => {
	const result = results[page];

	if (!result?.lastFetchTime || Date.now() - result.lastFetchTime > MAX_AGE_MS) {
		let path = formatPath(url);

		const token = localStorage.getItem(TOKEN);
		const headers = new Headers();

		if (token) headers.append('Authorization', `Bearer ${token}`);

		const res = await fetch(API_URL + path, {
			headers
		});

		if (!res.ok) {
			throw new Error(`An error occured with status code: ${res.status}`);
		}
		const data = await res.json();
		const lastFetchTime = Date.now();

		results = {
			...results,
			[page]: {
				data,
				lastFetchTime
			}
		};
	}

	return results[page].data;
};

/**
 * Sends data to a post, put, or delete endpoint to the API.
 * @param {string} url The URL path for the API.
 * @param {import('./fetch.d.ts').SendDataOptions} opts The options to be send.
 */
export const sendData = async (url, opts) => {
	const token = localStorage.getItem(TOKEN);

	if (!token) {
		console.error('`access_token` is not found. Login to get one.');
		return;
	}

	const req = await fetch(API_URL + formatPath(url), {
		method: opts.method || 'POST',
		body: JSON.stringify(opts.body),
		headers: {
			Authorization: `Bearer ${token}`,
			'Content-Type': 'application/json'
		}
	});
	const res = await req.json();

	return {
		ok: req.ok,
		status: req.status,
		body: res
	};
};
