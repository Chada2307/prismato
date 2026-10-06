<script lang="ts">
    import { X, ChevronLeft, ChevronRight, Loader2 } from 'lucide-svelte';
    import { PUBLIC_API_URL } from '$env/static/public';

    let { photos, initialIndex, onClose} = $props<{
        photos: any[];
        initialIndex: number;
        onClose: () => void;
    }>();

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
    
    <button class="absolute right-6 top-6 z-50 rounded-full bg-white/10 p-2 text-white transition-colors hover:bg-white/20" onclick={onClose}>
        <X size={28} />
    </button>

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