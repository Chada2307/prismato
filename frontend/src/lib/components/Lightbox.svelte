<script lang="ts">
    import { X, ChevronLeft, ChevronRight, Heart, Trash2, FolderPlus, Loader2 } from 'lucide-svelte';
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

    let originalUrl = $derived(
        currentPhoto.original_url
        ? (currentPhoto.original_url.startsWith('http') ? currentPhoto.original_url : `${PUBLIC_API_URL}${currentPhoto.original_url}`)
        : (currentPhoto.thumbnail_url.startsWith('http') ? currentPhoto.thumbnail_url : `${PUBLIC_API_URL}${currentPhoto.thumbnail_url}`)
    );

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
    
    <div class="absolute bottom-0 left-0 right-0 flex justify-center bg-gradient-to-t from-black/80 to-transparent p-8 text-white pointer-events-none">
        <div class="text-center">
            <p class="font-medium text-lg">{currentPhoto.camera_model || 'Nieznany aparat'}</p>
            <p class="text-sm text-white/70">
                {new Date(currentPhoto.captured_at).toLocaleString('pl-PL', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute:'2-digit' })}
            </p>
        </div>
    </div>
</div>