<script lang="ts">
    import { invalidateAll } from '$app/navigation';
    import { onMount } from 'svelte';
    import PhotoCard from '$lib/components/PhotoCard.svelte';
    import { Loader2, FolderHeart, X, Trash2 } from 'lucide-svelte';
    import { PUBLIC_API_URL } from '$env/static/public';
    import Lightbox from '$lib/components/Lightbox.svelte';
    import DragAndDrop from '$lib/components/DragAndDrop.svelte';
    import { SelectionState } from '$lib/states/selection.svelte';
    import { uploader } from '$lib/states/upload.svelte';
    import * as api from '$lib/api/photos';

    const selection = new SelectionState();

    type Photo = {
        id: string;
        thumbnail_url: string;
        original_url: string;
        captured_at: string;
        camera_model: string;
        is_favorite: boolean;
    };

    let { data } = $props();

    let photos = $state<Photo[]>(data.photos);
    let count = $state<number | null>(data.info.count);

    let offset = $state(20);
    let isLoadingMore = $state(false);

    let hasMore = $state(data.photos.length >= 20);

    let showAlbumModal = $state(false);
    let userAlbums = $state<{id: string, title: string}[]>([]);
    let isAddingToAlbum = $state(false);
    let lightboxIndex = $state<number | null>(null);
        
    //03.11
    let syncInterval: ReturnType<typeof setInterval>;

    

    let groupedPhotos =  $derived.by(() => {
        const sorted = [...photos].sort((a,b) => {
            const dateA = a.captured_at ? new Date(a.captured_at).getTime() : 0;
            const dateB = b.captured_at ? new Date(b.captured_at).getTime() : 0;
            return dateB - dateA;
        });

        const groups: Record<string, typeof photos> = {};
        for(const photo of sorted){
            let label = "brak daty / przetwarzanie...";
            if(photo.captured_at){
                const date = new Date(photo.captured_at);
                const monthYear = date.toLocaleDateString('pl-PL', { month: 'long', year: 'numeric' });
                label = monthYear.charAt(0).toUpperCase() + monthYear.slice(1);
            }
            if(!groups[label]){
                groups[label] = [];
            }
            groups[label].push(photo);
        }
        return groups;
    });


    $effect(() => {
        photos = data.photos;
        offset = data.photos.length;
        hasMore = data.photos.length >= 20;
    });

    async function openAlbumModal() {
        showAlbumModal = true;
        try {
            userAlbums = await api.fetchAlbums();
        } catch (err) {
            console.error('Błąd pobierania albumów', err);
        }
    }

    async function addToAlbum(albumId: string) {
        isAddingToAlbum = true;
        try {
            await api.addPhotosToAlbum(albumId, selection.selectedIds);
            alert('Dodano zdjęcia do albumu!');
            showAlbumModal = false;
            selection.clear();
        } catch (err) {
            console.error(err);
        } finally {
            isAddingToAlbum = false;
        }
    }

    async function loadMore() {
        if (isLoadingMore || !hasMore) return;

        isLoadingMore = true;
        try {
            const newPhotos = await api.fetchPhotos(offset);

            const uniqueNewPhotos = newPhotos.filter(
                newPhoto => !photos.some(existing => existing.id === newPhoto.id)
            );

            photos.push(...uniqueNewPhotos);
            offset += newPhotos.length;

            if (newPhotos.length < 20) hasMore = false;
        } catch (err) {
            console.error('Błąd pobierania kolejnych zdjęc', err);
        } finally {
            isLoadingMore = false;
        }
    }
    
    function infiniteScroll(node: HTMLElement, callback: () => void) {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                callback();
            }
        }, { 
            rootMargin: '800px' 
        });

        observer.observe(node);

        return {
            destroy() {
                observer.disconnect();
            }
        };
    }

    async function moveToTrash(photoId: string) {
        try {
            await api.deletePhoto(photoId);
            photos = photos.filter((photo) => photo.id !== photoId);
            offset -= 1;
        } catch (err) {
            alert('Nie udało się przenieść do kosza');
        }
    }

    async function toggleFavorite(photoId: string) {
        try {
            const updatedData = await api.toggleFavoriteStatus(photoId);
            const index = photos.findIndex(p => p.id === photoId);
            if (index !== -1) photos[index].is_favorite = updatedData.is_favorite;
        } catch (err) {
            console.error(err);
        }
    }

    async function getInfo(){
        try{
            const res = await fetch(`${PUBLIC_API_URL}/photos/info`);
            if (res.ok){
                const response = await res.json();
                count = response;
            }
        }catch(err){
            console.error('błąd pobrania informacji', err);
        }
    }

    async function deleteSelectedPhotos(){
        if(!confirm(`Czy na pewno chcesz usunąć ${selection.selectedIds.length} zdjęć do kosza?`)) return;
        try {
            await api.bulkDeleteSoft(selection.selectedIds);
            photos = photos.filter(photo => !selection.selectedIds.includes(photo.id));
            selection.clear();
        } catch(err) {
            console.error(err);
        }
    }

    async function syncLatestPhotos() {
        try {
            const res = await fetch(`${PUBLIC_API_URL}/photos?skip=0&limit=20`);
            if (!res.ok) return;
            
            const latestPhotos = await res.json();
        
            for (const fresh of latestPhotos) {
                const existingIndex = photos.findIndex(p => p.id === fresh.id);
                
                if (existingIndex !== -1) {
            
                    if (photos[existingIndex].thumbnail_url !== fresh.thumbnail_url || 
                        photos[existingIndex].captured_at !== fresh.captured_at) {
                        photos[existingIndex] = fresh; 
                    }
                } else {
                    photos.unshift(fresh);
                    offset++; 
                }
            }

            if (uploader.isUploading) {
                const infoRes = await fetch(`${PUBLIC_API_URL}/photos/info`);
                if (infoRes.ok) count = (await infoRes.json()).count;
            }
        } catch (err) {
            
        }
    }

    onMount(() => {
        syncInterval = setInterval(syncLatestPhotos, 3000);
        return () => {
            clearInterval(syncInterval);
        };
    });
   
</script>

<div class="relative flex min-h-screen flex-col gap-8 pb-24">

    <header>
        
        <h2 class="text-3xl font-bold text-dark-text">Twoja Galeria</h2>
        <p class="text-dark-text/60">Łącznie zdjęć {count} zdjęć</p>
        <button 
        onclick={() => selection.toggleManual()}
        class="rounded-lg px-4 py-2 text-sm font-medium transition-colors {selection.isSelectionMode ? 'bg-brand text-white' : 'bg-gray-100 text-dark-text hover:bg-gray-200'}"
            >
        {selection.isSelectionMode ? 'Anuluj wybór' : 'Wybierz zdjęcia'}
        </button>
    </header>

    <div class="flex flex-col gap-10">
        {#each Object.entries(groupedPhotos) as [monthLabel, monthPhotos] (monthLabel)}
            <section>
                <h3 class="mb-4 text-xl font-bold text-dark-text/80">{monthLabel}</h3>
            
                <div class="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
                    {#each monthPhotos as photo, i (photo.id)}
                        <PhotoCard
                            id={photo.id}
                            bind:thumbnail_url={photos[i].thumbnail_url}
                            bind:captured_at={photos[i].captured_at}
                            bind:camera_model={photos[i].camera_model}
                            is_favorite={photo.is_favorite}
                            isSelectionMode={selection.isSelectionMode}
                            isSelected={selection.selectedIds.includes(photo.id)}
                            onSelect={() => selection.toggle(photo.id)}
                            onDelete={() => moveToTrash(photo.id)}
                            onFavorite={() => toggleFavorite(photo.id)}
                            onClickImage={() => lightboxIndex = photos.findIndex(p => p.id === photo.id)}
                        />
                    {/each}
                </div>
            </section>
        {/each}
    </div>

    {#if hasMore}
        <div 
            use:infiniteScroll={loadMore} 
            class="flex justify-center pb-24 pt-6 text-brand"
        >
            {#if isLoadingMore}
                <Loader2 size={32} class="animate-spin opacity-50" />
            {/if}
        </div>
    {/if}

    {#if !hasMore && photos.length > 0}
        <div class="flex justify-center pb-24 pt-6 text-sm font-medium text-gray-400">
            To już wszystkie zdjęcia w Twojej galerii.
        </div>
    {/if}

    {#if selection.isSelectionMode}
        <div class="fixed bottom-6 left-1/2 z-40 flex -translate-x-1/2 items-center gap-4 rounded-full border border-gray-200 bg-white/90 px-6 py-3 shadow-xl backdrop-blur-md transition-all">
            <span class="font-medium text-dark-text">Wybrano: <span class="font-bold text-brand">{selection.selectedIds.length}</span></span>
            
            <div class="h-6 w-px bg-gray-300"></div>
            
            <button onclick={openAlbumModal} class="flex items-center gap-2 rounded-full bg-brand px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-brand/90">
                <FolderHeart size={16} />
                Dodaj do albumu
            </button>
            
            <button onclick={deleteSelectedPhotos} class="flex items-center gap-1.5 rounded-full px-3 py-1.5 text-sm font-medium text-red-600 transition-colors hover:bg-red-50 hover:text-red-700">
                <Trash2 size={16} />
                    Usuń zaznaczone
            </button>

            <button onclick={() => selection.cancel()} class="flex h-9 w-9 items-center justify-center rounded-full bg-gray-100 text-gray-500 transition-colors hover:bg-gray-200 hover:text-dark-text">
                <X size={18} />
            </button>
        </div>
    {/if}
</div>

{#if showAlbumModal}
    <div class="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 px-4 backdrop-blur-sm">
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

{#if lightboxIndex !== null}
    <Lightbox 
        photos={photos} 
        initialIndex={lightboxIndex} 
        onClose={() => lightboxIndex = null} 
        onFavorite={(photoId) => toggleFavorite(photoId)}
        onAddToAlbum={(photoId) => {
            selection.selectSingle(photoId);
            openAlbumModal();
        }}
        onDelete={async (photoId) => {
            await moveToTrash(photoId);
            if(photos.length === 0){
                lightboxIndex = null;
            }else if (lightboxIndex! >= photos.length){
                lightboxIndex = photos.length - 1;
            }
        }}
    />
{/if}