import type { PageLoad } from './$types';
import { PUBLIC_API_URL } from '$env/static/public';

export const ssr = false;

export const load: PageLoad = async ({ params, fetch }) =>{
    const albumId = params.id;

    try{
        const albumRes = await fetch (`${PUBLIC_API_URL}/albums/${albumId}`);
        if (!albumRes.ok) throw new Error('Nie znaleziono albumu');
        const album = await albumRes.json();

        const photoRes = await fetch(`${PUBLIC_API_URL}/albums/${albumId}/photos`);
        const photos = photoRes.ok ? await photoRes.json() : [];

        return { album, photos};
    }catch(error){
        console.error(error);
        return{ album : null, photos: []};
    }
};