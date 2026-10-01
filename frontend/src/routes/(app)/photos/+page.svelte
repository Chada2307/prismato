<script lang="ts">
    import { invalidateAll } from '$app/navigation';
    import PhotoCard from '$lib/components/PhotoCard.svelte';
    import { Loader2, FolderHeart, X } from 'lucide-svelte';
    import { PUBLIC_API_URL } from '$env/static/public';

    type Photo = {
        id: string;
        thumbnail_url: string;
        captured_at: string;
        camera_model: string;
        is_favorite: boolean;
    };

    let { data } = $props();

    let photos = $state<Photo[]>(data.photos);

    let offset = $state(20);
    let isLoadingMore = $state(false);

    let hasMore = $state(data.photos.length >= 20);

    let selectedPhotoIds = $state<string[]>([]);
	let manualSelectionMode = $state(false);
    let isSelectionMode = $derived(manualSelectionMode || selectedPhotoIds.length > 0);

    let showAlbumModal = $state(false);
    let userAlbums = $state<{id: string, title: string}[]>([]);
    let isAddingToAlbum = $state(false);

    $effect(() => {
        photos = data.photos;
        offset = data.photos.length;
        hasMore = data.photos.length >= 20;
    });

	function toggleManualSelection() {
    manualSelectionMode = !manualSelectionMode;
    if (!manualSelectionMode) {
        selectedPhotoIds = [];
    }
}
    function toggleSelection(photoId: string) {
        if (selectedPhotoIds.includes(photoId)) {
            selectedPhotoIds = selectedPhotoIds.filter(id => id !== photoId);
        } else {
            selectedPhotoIds.push(photoId);
        }
    }

    function cancelSelection() {
        selectedPhotoIds = [];
		manualSelectionMode = false;
    }

    async function openAlbumModal() {
        showAlbumModal = true;
        try {
            const res = await fetch(`${PUBLIC_API_URL}/albums/`);
            if (res.ok) userAlbums = await res.json();
        } catch (err) {
            console.error('Błąd pobierania albumów', err);
        }
    }

    async function addToAlbum(albumId: string) {
        isAddingToAlbum = true;
        try {
            const res = await fetch(`${PUBLIC_API_URL}/albums/${albumId}/photos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ photo_ids: selectedPhotoIds })
            });

            if (res.ok) {
                alert('Dodano zdjęcia do albumu!');
                showAlbumModal = false;
                selectedPhotoIds = [];
            } else {
                alert('Błąd podczas dodawania do albumu');
            }
        } catch (err) {
            console.error(err);
        } finally {
            isAddingToAlbum = false;
        }
    }

    async function loadMore() {
        isLoadingMore = true;
        try {
            const res = await fetch(`${PUBLIC_API_URL}/photos?skip=${offset}&limit=20`);
            if (res.ok) {
                const newPhotos = await res.json();
                photos.push(...newPhotos);
                offset += newPhotos.length;
                if (newPhotos.length < 20) {
                    hasMore = false;
                }
            }
        } catch (err) {
            console.error('Błąd pobierania kolejnych zdjęc', err);
        } finally {
            isLoadingMore = false;
        }
    }

    async function moveToTrash(photoId: string) {
        const res = await fetch(`${PUBLIC_API_URL}/photos/${photoId}`, { method: 'DELETE' });
        if (res.ok) {
            photos = photos.filter((photo) => photo.id !== photoId);
            offset -= 1;
        } else {
            alert('Nie udało sie przenieść do kosza');
            throw new Error('błąd');
        }
    }

    async function toggleFavorite(photoId: string) {
        try {
            const res = await fetch(`${PUBLIC_API_URL}/photos/${photoId}/favorite`, { method: 'PUT' });
            if (res.ok) {
                const updatedData = await res.json();
                const index = photos.findIndex(p => p.id === photoId);
                if (index !== -1) {
                    photos[index].is_favorite = updatedData.is_favorite;
                }
            }
        } catch (err) {
            console.error('blad zmiany ulubionych', err);
        }
    }
</script>

<div class="relative flex min-h-screen flex-col gap-8 pb-24">
    <header>
        <h2 class="text-3xl font-bold text-dark-text">Twoja Galeria</h2>
        <p class="text-dark-text/60">Znaleziono {photos.length} zdjęć</p>
		<button 
        onclick={toggleManualSelection}
        class="rounded-lg px-4 py-2 text-sm font-medium transition-colors {isSelectionMode ? 'bg-brand text-white' : 'bg-gray-100 text-dark-text hover:bg-gray-200'}"
    >
        {isSelectionMode ? 'Anuluj wybór' : 'Wybierz zdjęcia'}
    </button>
    </header>

    <div class="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
        {#each photos as photo (photo.id)}
            <PhotoCard
                id={photo.id}
                thumbnail_url={photo.thumbnail_url}
                captured_at={photo.captured_at}
                camera_model={photo.camera_model}
                is_favorite={photo.is_favorite}
                isSelectionMode={isSelectionMode}
                isSelected={selectedPhotoIds.includes(photo.id)}
                onSelect={() => toggleSelection(photo.id)}
                onDelete={() => moveToTrash(photo.id)}
                onFavorite={() => toggleFavorite(photo.id)}
            />
        {/each}
    </div>

    {#if hasMore}
        <div class="flex justify-center pb-12 pt-6">
            <button
                onclick={loadMore}
                disabled={isLoadingMore}
                class="flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-6 py-3 font-medium text-dark-text shadow-sm transition-all hover:bg-gray-50 hover:shadow-md disabled:opacity-50"
            >
                {#if isLoadingMore}
                    <Loader2 size={18} class="animate-spin text-brand" />
                    Wczytywanie...
                {:else}
                    Załaduj więcej zdjęć
                {/if}
            </button>
        </div>
    {/if}

    {#if !hasMore && photos.length > 0}
        <div class="flex justify-center pb-12 pt-6 text-sm text-gray-400">
            To już wszystkie zdjęcia w Twojej galerii.
        </div>
    {/if}

    {#if isSelectionMode}
        <div class="fixed bottom-6 left-1/2 z-40 flex -translate-x-1/2 items-center gap-4 rounded-full border border-gray-200 bg-white/90 px-6 py-3 shadow-xl backdrop-blur-md transition-all">
            <span class="font-medium text-dark-text">Wybrano: <span class="font-bold text-brand">{selectedPhotoIds.length}</span></span>
            
            <div class="h-6 w-px bg-gray-300"></div>
            
            <button onclick={openAlbumModal} class="flex items-center gap-2 rounded-full bg-brand px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-brand/90">
                <FolderHeart size={16} />
                Dodaj do albumu
            </button>

            <button onclick={cancelSelection} class="flex h-9 w-9 items-center justify-center rounded-full bg-gray-100 text-gray-500 transition-colors hover:bg-gray-200 hover:text-dark-text">
                <X size={18} />
            </button>
        </div>
    {/if}
</div>

{#if showAlbumModal}
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4 backdrop-blur-sm">
        <div class="w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-2xl">
            <div class="flex items-center justify-between border-b border-gray-100 p-4">
                <h3 class="text-lg font-bold text-dark-text">Wybierz album</h3>
                <button onclick={() => showAlbumModal = false} class="text-gray-400 hover:text-dark-text"><X size={20}/></button>
            </div>
            
            <div class="max-h-[60vh] overflow-y-auto p-2">
                {#if userAlbums.length === 0}
                    <div class="p-6 text-center text-gray-500">
                        Nie masz jeszcze żadnych albumów. <br/>Przejdź do zakładki Albumy, aby je utworzyć.
                    </div>
                {:else}
                    <div class="flex flex-col gap-1">
                        {#each userAlbums as album}
                            <button 
                                onclick={() => addToAlbum(album.id)}
                                disabled={isAddingToAlbum}
                                class="flex items-center gap-3 rounded-xl p-3 text-left transition-colors hover:bg-brand/5 disabled:opacity-50"
                            >
                                <div class="rounded-lg bg-brand/10 p-2 text-brand"><FolderHeart size={20}/></div>
                                <span class="font-medium text-dark-text">{album.title}</span>
                            </button>
                        {/each}
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}