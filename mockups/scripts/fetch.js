import { API_URL, MAX_AGE_MS, TOKEN } from './constants.js';

let results = {};

/**
 * Simple fetch wrapper that returns cached result.
 * @param {string} page The unique ID used when caching the results
 * @param {string} url The URL path for the API.
 * @returns {any}
 */
export const fetchData = async (page, url) => {
	const result = results[page];

	if (!result?.lastFetchTime || Date.now() - result.lastFetchTime > MAX_AGE_MS) {
		let path = url.startsWith('/') ? url : '/' + url;

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
