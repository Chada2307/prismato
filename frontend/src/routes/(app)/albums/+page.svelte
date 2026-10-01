<script lang="ts">
    import { FolderHeart, Plus, Loader2 } from 'lucide-svelte';
    import { PUBLIC_API_URL } from '$env/static/public';

    let { data } = $props();
    
    let albums = $state(data.albums);
    
    let newAlbumTitle = $state('');
    let isCreating = $state(false);

    async function createAlbum(e: Event) {
        e.preventDefault();
        if (!newAlbumTitle.trim()) return;

        isCreating = true;
        try {
            const res = await fetch(`${PUBLIC_API_URL}/albums/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: newAlbumTitle.trim() })
            });

            if (res.ok) {
                const newAlbum = await res.json();
         
                albums = [newAlbum, ...albums];
                newAlbumTitle = ''; 
            } else {
                alert('Nie udało się utworzyć albumu');
            }
        } catch (err) {
            console.error(err);
        } finally {
            isCreating = false;
        }
    }
</script>

<div class="flex flex-col gap-8">
    <header class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
            <h2 class="text-3xl font-bold text-dark-text">Twoje Albumy</h2>
            <p class="text-dark-text/60">Zarządzaj swoimi kolekcjami</p>
        </div>
        <form onsubmit={createAlbum} class="flex items-center gap-2">
            <input 
                type="text" 
                bind:value={newAlbumTitle} 
                placeholder="Nazwa nowego albumu..." 
                class="rounded-lg border border-gray-200 px-4 py-2 focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
                disabled={isCreating}
            />
            <button 
                type="submit" 
                disabled={isCreating || !newAlbumTitle.trim()}
                class="flex h-10 w-10 items-center justify-center rounded-lg bg-brand text-white transition-colors hover:bg-brand/90 disabled:opacity-50"
            >
                {#if isCreating}
                    <Loader2 size={20} class="animate-spin" />
                {:else}
                    <Plus size={20} />
                {/if}
            </button>
        </form>
    </header>

    {#if albums.length === 0}
        <div class="flex flex-col items-center justify-center rounded-2xl border border-dashed border-gray-200 py-20 text-gray-400">
            <FolderHeart size={48} class="mb-4 opacity-50" />
            <p>Nie masz jeszcze żadnych albumów.</p>
        </div>
    {:else}
        <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
            {#each albums as album (album.id)}
    
                <a 
                    href="/albums/{album.id}" 
                    class="group flex cursor-pointer flex-col gap-3 rounded-xl border border-gray-100 bg-white p-4 shadow-sm transition-all hover:border-brand/30 hover:shadow-md"
                >
                    <div class="flex items-center justify-between">
                        <div class="rounded-lg bg-brand/10 p-3 text-brand transition-colors group-hover:bg-brand group-hover:text-white">
                            <FolderHeart size={28} />
                        </div>
                    </div>
                    
                    <div class="flex flex-col">
                        <h3 class="truncate font-semibold text-dark-text" title={album.title}>
                            {album.title}
                        </h3>
                        <p class="text-sm text-gray-400">
                            {album.photo_count} {album.photo_count === 1 ? 'zdjęcie' : 'zdjęć'}
                        </p>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>