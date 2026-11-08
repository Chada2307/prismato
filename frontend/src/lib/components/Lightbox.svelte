<script lang="ts">
    import { X, ChevronLeft, ChevronRight, Heart, Trash2, FolderPlus, Loader2, Tag as TagIcon } from 'lucide-svelte';
    import { addTagToPhoto, removeTagFromPhoto } from '$lib/api/photos';
    import { PUBLIC_API_URL } from '$env/static/public';

   let { 
        photos, 
        initialIndex, 
        onClose,
        onFavorite,
        onDelete,
        onAddToAlbum
    } = $props<{
        photos: any[];
        initialIndex: number;
        onClose: () => void;
        onFavorite: (id: string) => void;
        onDelete: (id: string) => Promise<void>;
        onAddToAlbum: (id: string) => void;
    }>()

    let currentIndex = $state(initialIndex);
    let isLoading = $state(true);

    let currentPhoto = $derived(photos[currentIndex]);

    let newTagInput = $state('');
    let isTagging = $state(false);

    let originalUrl = $derived(
        currentPhoto.original_url
        ? (currentPhoto.original_url.startsWith('http') ? currentPhoto.original_url : `${PUBLIC_API_URL}${currentPhoto.original_url}`)
        : (currentPhoto.thumbnail_url.startsWith('http') ? currentPhoto.thumbnail_url : `${PUBLIC_API_URL}${currentPhoto.thumbnail_url}`)
    );

    async function handleAddTag(e: KeyboardEvent) {
        if (e.key !== 'Enter' || !newTagInput.trim()) return;
        
        const tagName = newTagInput.trim().toLowerCase();
        
        if (currentPhoto.tags?.some(t => t.name === tagName)) {
            newTagInput = '';
            return;
        }

        isTagging = true;
        try {
            const data = await addTagToPhoto(currentPhoto.id, tagName);
            if (!currentPhoto.tags) currentPhoto.tags = [];
            currentPhoto.tags.push({ id: 'temp-id', name: data.tag }); 
            newTagInput = '';
        } catch (err) {
            console.error(err);
            alert('Błąd podczas dodawania tagu');
        } finally {
            isTagging = false;
        }
    }

    async function handleRemoveTag(tagName: string) {
        try {
            await removeTagFromPhoto(currentPhoto.id, tagName);
    
            currentPhoto.tags = currentPhoto.tags.filter(t => t.name !== tagName);
        } catch (err) {
            console.error(err);
        }
    }

    function next(){
        if (currentIndex < photos.length - 1){
            currentIndex++;
            isLoading = true;
        }
    }
    function prev(){
        if(currentIndex > 0 ){
            currentIndex--;
            isLoading = true;
        }
    }

    function handleKeydown(e: KeyboardEvent){
        if (e.key === 'Escape') onClose();
        if (e.key === 'ArrowRight') next();
        if (e.key === 'ArrowLeft') prev();
    }

    $effect(() => {
        document.body.style.overflow = 'hidden';
        return () => { document.body.style.overflow = 'auto'; };
    });


</script>

<svelte:window onkeydown={handleKeydown} />

<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-md" onclick={onClose}>
    
    <div class="absolute left-0 right-0 top-0 z-50 flex items-center justify-end bg-gradient-to-b from-black/70 to-transparent p-6 text-white pointer-events-none">
        <div class="flex items-center gap-4 pointer-events-auto">
            <button 
                onclick={(e) => { e.stopPropagation(); onFavorite(currentPhoto.id); }} 
                class="rounded-full bg-white/10 p-2.5 transition-all hover:bg-white/20 hover:scale-105"
                title="Dodaj do ulubionych"
            >
                <Heart size={24} fill={currentPhoto.is_favorite ? "red" : "none"} color={currentPhoto.is_favorite ? "red" : "white"} />
            </button>
            
            <button 
                onclick={(e) => { e.stopPropagation(); onAddToAlbum(currentPhoto.id); }} 
                class="rounded-full bg-white/10 p-2.5 transition-all hover:bg-white/20 hover:scale-105 hover:text-brand"
                title="Dodaj do albumu"
            >
                <FolderPlus size={24} />
            </button>
            
            <button 
                onclick={(e) => { e.stopPropagation(); onDelete(currentPhoto.id); }} 
                class="rounded-full bg-white/10 p-2.5 transition-all hover:bg-white/20 hover:scale-105 hover:text-red-400"
                title="Przenieś do kosza"
            >
                <Trash2 size={24} />
            </button>
            
            <div class="mx-2 h-6 w-px bg-white/30"></div>
            
            <button 
                class="rounded-full bg-white/10 p-2.5 transition-all hover:bg-white/20 hover:scale-105 hover:text-gray-300" 
                onclick={(e) => { e.stopPropagation(); onClose(); }}
                title="Zamknij (Esc)"
            >
                <X size={28} />
            </button>
        </div>
    </div>

    {#if currentIndex > 0}
        <button class="absolute left-6 z-50 rounded-full bg-white/10 p-3 text-white transition-colors hover:bg-white/20 sm:left-12" onclick={(e) => { e.stopPropagation(); prev(); }}>
            <ChevronLeft size={36} />
        </button>
    {/if}

    {#if currentIndex < photos.length - 1}
        <button class="absolute right-6 z-50 rounded-full bg-white/10 p-3 text-white transition-colors hover:bg-white/20 sm:right-12" onclick={(e) => { e.stopPropagation(); next(); }}>
            <ChevronRight size={36} />
        </button>
    {/if}

    <div class="relative flex h-full w-full items-center justify-center p-4 sm:p-12" onclick={(e) => e.stopPropagation()}>
        {#if isLoading}
            <div class="absolute flex items-center justify-center">
                <Loader2 size={48} class="animate-spin text-white/50" />
            </div>
        {/if}
        
        <img 
            src={originalUrl} 
            alt={currentPhoto.camera_model}
            class="max-h-full max-w-full object-contain drop-shadow-2xl transition-opacity duration-300 {isLoading ? 'opacity-0' : 'opacity-100'}"
            onload={() => isLoading = false}
        />
    </div>
    
    <div 
        class="absolute bottom-24 right-6 z-50 w-72 sm:right-12 sm:w-80 rounded-2xl bg-black/60 p-5 backdrop-blur-md border border-white/10 shadow-2xl pointer-events-auto transition-all" 
        onclick={(e) => e.stopPropagation()}
    >
        <div class="flex flex-col gap-3">
            <div class="flex items-center gap-2 text-sm font-semibold text-white/90">
                <TagIcon size={16} />
                <span>Etykiety ({currentPhoto.tags?.length || 0})</span>
            </div>

            <div class="flex flex-wrap gap-2">
                {#each currentPhoto.tags || [] as tag (tag.name)}
                    <div class="group flex items-center gap-1 rounded-full bg-white/20 pl-3 pr-1 py-1 text-xs font-medium text-white transition-colors hover:bg-white/30">
                        <span>{tag.name}</span>
                        <button 
                            onclick={() => handleRemoveTag(tag.name)}
                            class="rounded-full p-1 opacity-50 transition-all hover:bg-red-500 hover:text-white hover:opacity-100"
                            title="Usuń tag"
                        >
                            <X size={12} />
                        </button>
                    </div>
                {/each}
            </div>

            <div class="relative mt-2">
                <input 
                    type="text" 
                    bind:value={newTagInput}
                    onkeydown={handleAddTag}
                    disabled={isTagging}
                    placeholder="Wpisz tag i wciśnij Enter..."
                    class="w-full rounded-lg border border-white/20 bg-black/40 px-3 py-2 text-sm text-white placeholder-white/40 outline-none transition-all focus:border-brand focus:bg-black/60 focus:ring-1 focus:ring-brand disabled:opacity-50"
                />
            </div>
        </div>
    </div>

    <div class="absolute bottom-0 left-0 right-0 flex justify-center bg-gradient-to-t from-black/80 to-transparent p-8 text-white pointer-events-none">
        <div class="text-center">
            <p class="font-medium text-lg">{currentPhoto.camera_model || 'Nieznany aparat'}</p>
            <p class="text-sm text-white/70">
                {new Date(currentPhoto.captured_at).toLocaleString('pl-PL', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute:'2-digit' })}
            </p>
        </div>
    </div>
</div>