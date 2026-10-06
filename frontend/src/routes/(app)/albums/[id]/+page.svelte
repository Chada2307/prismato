<script lang="ts">
    import { PUBLIC_API_URL } from '$env/static/public';
    import PhotoCard from '$lib/components/PhotoCard.svelte';
    import { ArrowLeft, ImageOff } from 'lucide-svelte';
     import Lightbox from '$lib/components/Lightbox.svelte';

    let { data } = $props();

    let album = $state(data.album);
    let photos = $state(data.photos);
    let lightboxIndex = $state<number | null>(null);


    $effect(() =>{
        album = data.album;
        photos = data.photos;
    });

    async function moveToTrash(photoId: string){
        const res = await fetch (`${PUBLIC_API_URL}/photos/${photoId}`, { method: 'DELETE' });
        if (res.ok){
            photos = photos.filter((p: any) => p.id !== photoId);
            if(album) album.photo_count -= 1;
        }else{
            alert('Bład podczas usuwania zdjęcia');
        }
    }

    async function toggleFavorite(photoId: string)  {
        const res = await fetch(`${PUBLIC_API_URL}/photos/${photoId}/favorite`, { method: 'PUT' });
        if(res.ok){
            const updated = await res.json();
            const index = photos.findIndex((p: any) => p.id === photoId);
            if(index !== -1) photos[index].is_favorite = updated.is_favorite;
        }
    }
</script>
{#if !album}
    <div class="flex h-64 flex-col items-center justify-center text-gray-500">
        <ImageOff size={48} class="mb-4 opacity-50" />
        <h2 class="text-xl font-bold text-dark-text">Nie znaleziono albumu</h2>
        <a href="/albums" class="mt-4 text-brand hover:underline">Wróć do listy albumów</a>
    </div>
{:else}
    <div class="flex flex-col gap-8 pb-24">
    
        <header class="flex flex-col gap-4">
            <a href="/albums" class="flex w-fit items-center gap-2 text-sm text-gray-500 transition-colors hover:text-brand">
                <ArrowLeft size={16} />
                Wróć do albumów
            </a>
            
            <div>
                <h2 class="text-3xl font-bold text-dark-text">{album.title}</h2>
                <p class="text-dark-text/60">
                    {album.photo_count} {album.photo_count === 1 ? 'zdjęcie' : 'zdjęć'}
                </p>
            </div>
        </header>

        {#if photos.length === 0}
            <div class="flex flex-col items-center justify-center rounded-2xl border border-dashed border-gray-200 py-20 text-gray-400">
                <ImageOff size={48} class="mb-4 opacity-50" />
                <p>Ten album jest na razie pusty.</p>
                <p class="text-sm">Przejdź do Galerii, zaznacz zdjęcia i dodaj je tutaj!</p>
            </div>
        {:else}
            <div class="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
                {#each photos as photo, index (photo.id)}
                    <PhotoCard
                        id={photo.id}
                        thumbnail_url={photo.thumbnail_url}
                        captured_at={photo.captured_at}
                        camera_model={photo.camera_model}
                        is_favorite={photo.is_favorite}
                        
                        isSelectionMode={false}
                        isSelected={false}
                        onSelect={() => {}}
                        
                        onDelete={() => moveToTrash(photo.id)}
                        onFavorite={() => toggleFavorite(photo.id)}
                        onClickImage={() => lightboxIndex = index}
                    />
                {/each}
            </div>
        {/if}
    </div>
{/if}
{#if lightboxIndex !== null}
    <Lightbox 
        photos={photos} 
        initialIndex={lightboxIndex} 
        onClose={() => lightboxIndex = null} 
    />
{/if}