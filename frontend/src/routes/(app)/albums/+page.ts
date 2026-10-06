import type { PageLoad } from './$types';
import { PUBLIC_API_URL } from '$env/static/public';

export const ssr = false;

export const load: PageLoad = async ({ fetch, depends }) => {
    depends ('api:albums');
    try{
        const response = await fetch(`${PUBLIC_API_URL}/albums/`, {
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        });
        if(!response.ok) throw new Error('Bład pobierania albumów');

        const albums = await response.json();
        return { albums };
    }catch(error){
        console.error('Api error:', error);
        return { albums: [] };
    }
};