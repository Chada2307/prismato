<script lang="ts">
    import { Heart, Trash, Loader2, CheckCircle2, Circle } from 'lucide-svelte';
    import { PUBLIC_API_URL } from '$env/static/public';

    let { 
        id, 
        thumbnail_url = $bindable(), 
        is_favorite, 
        captured_at = $bindable(), 
        camera_model = $bindable(), 
        onDelete, 
        onFavorite, 
        isSelectionMode, 
        isSelected,      
        onSelect,
        onClickImage, 
    } = $props<{
        id: string;
        thumbnail_url: string;
        captured_at: string;
        is_favorite: boolean;
        camera_model: string;
        isSelectionMode: boolean;
        isSelected: boolean;
        onSelect: () => void;
        onDelete: () => Promise<void>;
        onFavorite: () => Promise<void>;
        onClickImage?: () => void;
    }>();
    
    let isDeleting = $state(false);
    let isProcessing = $derived(!thumbnail_url);
    let checkInterval: any;

    $effect(() => {
        
        if (isProcessing) {
            checkInterval = setInterval(async () => {
                try {
                    const res = await fetch(`${PUBLIC_API_URL}/photos/${id}`);
                    if (res.ok) {
                        const updatedData = await res.json();
                        
                        if (updatedData.thumbnail_url) {
                    
                            thumbnail_url = updatedData.thumbnail_url;
                            captured_at = updatedData.captured_at;
                            camera_model = updatedData.camera_model;
                            clearInterval(checkInterval);
                        }
                    }
                } catch (err) {
            
                }
            }, 3000);
        } else {
            clearInterval(checkInterval);
        }

        return () => clearInterval(checkInterval);
    });
    async function handleDelete(e: Event) {
        e.stopPropagation();
        if (!confirm('Czy na pewno chcesz usunac to zdjecie?')) return;

        isDeleting = true;

        try {
            await onDelete();
        } catch (err) {
            console.error(err);
            alert('blad polaczenia z serwerem');
        } finally {
            isDeleting = false;
        }
    }
    
    async function handleFavorite(e: Event) {
        e.stopPropagation();
        try {
            await onFavorite();
        } catch (err) {
            console.error(err);
            alert('blad polaczenia z serwerem');
        }
    }


    let thumbnail = $derived(thumbnail_url.startsWith('http')
        ? thumbnail_url
        : `${PUBLIC_API_URL}${thumbnail_url}`);


    let dateFormatted = $derived(new Date(captured_at).toLocaleDateString('pl-PL', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    }));
</script>


<div
    class="group flex cursor-pointer flex-col overflow-hidden rounded-prismato border transition-all hover:shadow-md
           {isSelected ? 'border-brand bg-brand/5 shadow-md ring-2 ring-brand' : 'border-dark-text/5 bg-white shadow-sm'}"
        onclick={() => { 
            console.log("kliklem");
            if (isSelectionMode){
                console.log("kliklem nowy modal");
                onSelect(); 
            } else if (onClickImage){
                console.log("kliklem nowy modal");
                onClickImage();
            }
        
        }}
>
    <div class="relative aspect-square w-full overflow-hidden bg-zinc-100">
        
        {#if isProcessing}
            <div class="flex h-full w-full flex-col items-center justify-center bg-gray-100 text-brand/50">
                <Loader2 class="mb-2 animate-spin" size={32} />
                <span class="text-xs font-medium text-gray-400">Przetwarzanie...</span>
            </div>
        {:else}
            <img
                src={thumbnail}
                alt="Photo {camera_model}"
                onclick={onClickImage}
                class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
            />
        {/if}

      
        {#if isSelectionMode}
            <div class="absolute left-3 top-3 z-10 transition-transform hover:scale-110">
                {#if isSelected}
                    <div class="rounded-full bg-brand text-brand shadow-sm">
                        <CheckCircle2 size={24} fill="currentColor" class="text-brand" />
                    </div>
                {:else}
                    <div class="rounded-full bg-black/20 text-white ">
                        <Circle size={24} />
                    </div>
                {/if}
            </div>
        {/if}

        {#if !isSelectionMode}
            <div class="absolute right-3 top-3 flex flex-col gap-2 opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                <button class="flex h-10 w-10 items-center justify-center rounded-full bg-brand/80 text-white bg-brand hover:bg-danger" onclick={handleFavorite}>
                    <Heart size={18} fill={is_favorite ? "red" : "none"} color={is_favorite ? "red" : "currentColor"} />
                </button>
                <button class="flex h-10 w-10 items-center justify-center rounded-full bg-brand/80 text-white bg-brand hover:bg-danger" onclick={handleDelete} disabled={isDeleting}>
                    {#if isDeleting} <Loader2 size={18} class="animate-spin" /> {:else} <Trash size={18} /> {/if}
                </button>
            </div>
        {/if}
    </div>

    <div class="flex flex-col gap-0.5 p-4">
        <h3 class="truncate text-sm font-semibold text-dark-text">{camera_model}</h3>
        <p class="text-[10px] font-normal uppercase tracking-wider text-dark-text/50">{dateFormatted}</p>
    </div>
</div>