import { PUBLIC_API_URL } from "$env/static/public";

export async function fetchAlbums(){
    const res = await fetch(`${PUBLIC_API_URL}/albums/`);
    if(!res.ok) throw new Error('Błąd pobiernia albumów');
    return res.json();
}

export async function addPhotosToAlbum(albumId: string, photoIds: string[]){
    const res = await fetch(`${PUBLIC_API_URL}/albums/${albumId}/photos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ photo_ids: photoIds })
    });
    if (!res.ok) throw new Error('Błąd podczas dodawania do albumu');
    return res.ok;
}
export async function fetchPhotos(offset: number, limit: number = 30, q: string = '') {
    const params = new URLSearchParams({
        skip: offset.toString(),
        limit: limit.toString() 
    })

    if (q.trim() !== ''){
        params.append('q', q.trim());
    }

    const res = await fetch(`${PUBLIC_API_URL}/photos?${params.toString()}`);
    if (!res.ok) throw new Error('Błąd pobierania kolejnych zdjęć');
    return res.json();
}

export async function fetchInfo() {
    const res = await fetch(`${PUBLIC_API_URL}/photos/info`);
    if (!res.ok) throw new Error('Błąd pobrania informacji');
    return res.json();
}

export async function deletePhoto(photoId: string) {
    const res = await fetch(`${PUBLIC_API_URL}/photos/${photoId}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Nie udało się przenieść do kosza');
    return res.ok;
}

export async function toggleFavoriteStatus(photoId: string) {
    const res = await fetch(`${PUBLIC_API_URL}/photos/${photoId}/favorite`, { method: 'PUT' });
    if (!res.ok) throw new Error('Błąd zmiany ulubionych');
    return res.json();
}

export async function bulkDeleteSoft(photoIds: string[]) {
    const res = await fetch(`${PUBLIC_API_URL}/trash/bulk-delete-soft`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ photo_ids: photoIds })
    });
    if (!res.ok) throw new Error('Błąd podczas masowego usuwania');
    return res.ok;
}

export async function nukeGallery() {
    const res = await fetch(`${PUBLIC_API_URL}/photos/nuke`, { 
        method: 'DELETE' 
    });
    if (!res.ok) throw new Error('Błąd podczas czyszczenia galerii');
    return res.json();
}

export async function addTagToPhoto(photoId: string, tagName: string) {
    const res = await fetch(`${PUBLIC_API_URL}/photos/${photoId}/tags?tag_name=${encodeURIComponent(tagName)}`, {
        method: 'POST'
    });
    if (!res.ok) throw new Error('Nie udało się dodać tagu');
    return res.json();
}

export async function removeTagFromPhoto(photoId: string, tagName: string) {
    const res = await fetch(`${PUBLIC_API_URL}/photos/${photoId}/tags/${encodeURIComponent(tagName)}`, {
        method: 'DELETE'
    });
    if (!res.ok) throw new Error('Nie udało się usunąć tagu');
    return res.json();
}