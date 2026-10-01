<script lang="ts">
    import { Heart, Trash, Loader2, CheckCircle2, Circle } from 'lucide-svelte';
    import { PUBLIC_API_URL } from '$env/static/public';

    let { 
        id, 
        thumbnail_url, 
        is_favorite, 
        captured_at, 
        camera_model, 
        onDelete, 
        onFavorite, 
        isSelectionMode, 
        isSelected,      
        onSelect 
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
    }>();
    
    let isDeleting = $state(false);

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


    let fullImageUrl = $derived(thumbnail_url.startsWith('http')
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
    onclick={() => { if (isSelectionMode) onSelect(); }}
>
    <div class="relative aspect-square w-full overflow-hidden bg-zinc-100">
        <img
            src={fullImageUrl}
            alt={camera_model}
            class="h-full w-full object-cover transition-transform duration-500 {isSelected ? 'scale-105' : 'group-hover:scale-110'}"
            loading="lazy"
        />

      
        {#if isSelectionMode}
            <div class="absolute left-3 top-3 z-10 transition-transform hover:scale-110">
                {#if isSelected}
                    <div class="rounded-full bg-white text-brand shadow-sm">
                        <CheckCircle2 size={24} fill="currentColor" class="text-brand" />
                    </div>
                {:else}
                    <div class="rounded-full bg-black/20 text-white backdrop-blur-md">
                        <Circle size={24} />
                    </div>
                {/if}
            </div>
        {/if}

        {#if !isSelectionMode}
            <div class="absolute right-3 top-3 flex flex-col gap-2 opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                <button class="flex h-10 w-10 items-center justify-center rounded-full bg-brand/80 text-white backdrop-blur-md hover:bg-danger" onclick={handleFavorite}>
                    <Heart size={18} fill={is_favorite ? "red" : "none"} color={is_favorite ? "red" : "currentColor"} />
                </button>
                <button class="flex h-10 w-10 items-center justify-center rounded-full bg-brand/80 text-white backdrop-blur-md hover:bg-danger" onclick={handleDelete} disabled={isDeleting}>
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