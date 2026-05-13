<script lang="ts">
	import { Heart, Trash, Loader2 } from 'lucide-svelte';
  import { invalidateAll } from '$app/navigation';

	let { id, title, date, size, thumbnail_url, captured_at, camera_model } = $props<{
    id: string;
		title: string;
		date: string;
		size: string;
		thumbnail_url: string;
		captured_at: string;
		camera_model: string;

	}>();
  let isDeleting = $state(false);
  
  async function handleDelete(e:Event) {
    e.stopPropagation();
    if(!confirm('Czy na pewno chcesz usunac to zdjecie?')) return;

    isDeleting = true;

    try{
      const res = await fetch(`http://localhost:8000/photos/${id}`,{
        method: 'DELETE',
      });
      if(res.ok){
        await invalidateAll();
      } else{
        alert('Nie udalo sie usunac zdjecia');
      }
    } catch (err) {
      console.error(err);
      alert('blad polaczenia z serwerem');
    
    } finally {
      isDeleting = false;
    }
  }

	const BASE_URL = 'http://localhost:8000';
	const fullImageUrl = thumbnail_url.startsWith('http')? thumbnail_url : `${BASE_URL}${thumbnail_url}`;

	const dateFormatted = new Date(captured_at).toLocaleDateString('pl-PL', {
		day: 'numeric',
		month: 'long',
		year: 'numeric'
  	});
</script>

<div class="group flex flex-col overflow-hidden rounded-prismato bg-white shadow-sm hover:shadow-md transition-all cursor-pointer border border-dark-text/5">
  
  <div class="relative aspect-square w-full bg-zinc-100 overflow-hidden">
    
    <img 
      src={fullImageUrl} 
      alt={camera_model} 
      class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
      loading="lazy"
    />

    <div class="absolute right-3 top-3 flex flex-col gap-2 opacity-0 transition-opacity duration-200 group-hover:opacity-100">
      <button class="flex h-10 w-10 items-center justify-center rounded-full bg-brand/80 text-white backdrop-blur-md hover:bg-brand">
        <Heart size={18} />
      </button>
      <button
        onclick={handleDelete}
        disabled={isDeleting} 
        class="flex h-10 w-10 items-center justify-center rounded-full bg-brand/80 text-white backdrop-blur-md hover:bg-danger">
        
        {#if isDeleting}
            <Loader2 size={18} class="animate-spin" />
          {:else}
          <Trash size={18}/>
        {/if}
      </button>
    </div>
  </div>

  <div class="flex flex-col gap-0.5 p-4">
    <h3 class="truncate text-sm font-semibold text-dark-text">{camera_model}</h3>
    <p class="text-[10px] font-normal text-dark-text/50 uppercase tracking-wider">{dateFormatted}</p>
  </div>
  
</div>
