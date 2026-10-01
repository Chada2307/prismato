import type { PageLoad } from './$types';
import { PUBLIC_API_URL } from '$env/static/public';

export const ssr = false;
export const load: PageLoad = async ({ fetch }) => {
	try {
		const response = await fetch(`${PUBLIC_API_URL}/photos/`);

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
