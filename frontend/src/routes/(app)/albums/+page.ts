import type { PageLoad } from './$types';
import { PUBLIC_API_URL } from '$env/static/public';

export const ssr = false;

export const load: PageLoad = async ({ fetch }) => {
    try{
        const response = await fetch(`${PUBLIC_API_URL}/albums/`);
        if(!response.ok) throw new Error('Bład pobierania albumów');

        const album = await response.json();
        return { albums };
    }catch(error){
        console.error('Api error:', error);
        return { albums: [] };
    }
};