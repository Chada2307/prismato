import type { PageLoad } from './$types';

export const ssr = false;
export const load: PageLoad = async ({ fetch }) => {
	try {
		const response = await fetch('http://localhost:8000/photos/');

		if (!response.ok) {
			throw new Error('blad pobierania z api');
		}

		const photos = await response.json();

		return {
			photos
		};
	} catch (error) {
		console.error('blad API', error);

		return {
			photos: []
		};
	}
};
