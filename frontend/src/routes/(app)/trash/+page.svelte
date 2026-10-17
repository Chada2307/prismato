<script lang="ts">
	import { invalidateAll } from '$app/navigation';
    import PhotoCard from '$lib/components/PhotoCard.svelte';
    import { Loader2, FolderHeart, X, Trash2 } from 'lucide-svelte';
    import { PUBLIC_API_URL } from '$env/static/public';
	type Photo = {
		id: string;
		thumbnail_url: string;
		captured_at: string;
		camera_model: string;
	};

	let { data } = $props();

	let photos = $state<Photo[]>(data.photos);

	let offset = $state(20);
	let isLoadingMore = $state(false);

	let hasMore = $state(data.photos.length >= 20);

	let selectedPhotoIds = $state<string[]>([]);
	let manualSelectionMode = $state(false);
	let isSelectionMode = $derived(manualSelectionMode || selectedPhotoIds.length > 0);

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

	async function loadMore() {
		isLoadingMore = true;
		try {
			const res = await fetch(`${PUBLIC_API_URL}/trash?skip=${offset}&limit=20`);
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

	async function hardDelete(photoId: string) {
		const res = await fetch(`${PUBLIC_API_URL}/trash/${photoId}`, { method: 'DELETE' });
		if (res.ok) {
			photos = photos.filter((photo) => photo.id !== photoId);
			offset -= 1;
		} else {
			alert('Nie udało usunąć');
			throw new Error('błąd');
		}
	}

	function cancelSelection() {
        selectedPhotoIds = [];
		manualSelectionMode = false;
    }

	async function deleteSelectedPhotos(){
        if(!confirm(`Czy na pewno chcesz usunąć ${selectedPhotoIds.length} zdjęc do kosza?`)) return;

        try{
            const res = await fetch(`${PUBLIC_API_URL}/trash/bulk-delete-hard`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ photo_ids: selectedPhotoIds }) 
            });

            if(res.ok){
                photos = photos.filter(photo => !selectedPhotoIds.includes(photo.id));
                selectedPhotoIds = [];
            }
   
        }catch(err){
                console.error("Błąd podczas masowego usuwania: ", console.error());
        }
    }
</script>

<div class="flex flex-col gap-8">
	<header>
		<h2 class="text-3xl font-bold text-dark-text">Twój śmietnik</h2>
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
				onDelete={() => hardDelete(photo.id)}
				isSelectionMode={isSelectionMode}
                isSelected={selectedPhotoIds.includes(photo.id)}
				onSelect={() => toggleSelection(photo.id)}
			/>
		{/each}
	</div>
	{#if hasMore}
		<div class="flex justify-center pt-6 pb-12">
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
		<div class="flex justify-center pt-6 pb-12 text-sm text-gray-400">
			To już wszystkie zdjęcia w Twojej galerii.
		</div>
	{/if}

	{#if isSelectionMode}
        <div class="fixed bottom-6 left-1/2 z-40 flex -translate-x-1/2 items-center gap-4 rounded-full border border-gray-200 bg-white/90 px-6 py-3 shadow-xl backdrop-blur-md transition-all">
            <span class="font-medium text-dark-text">Wybrano: <span class="font-bold text-brand">{selectedPhotoIds.length}</span></span>
            
            <div class="h-6 w-px bg-gray-300"></div>
            
            <!-- <button onclick={openAlbumModal} class="flex items-center gap-2 rounded-full bg-brand px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-brand/90">
                <FolderHeart size={16} />
                Dodaj do albumu
            </button> -->
            
            <button onclick={deleteSelectedPhotos} class="flex items-center gap-1.5 rounded-full px-3 py-1.5 text-sm font-medium text-red-600 transition-colors hover:bg-red-50 hover:text-red-700">
                <Trash2 size={16} />
                    Usuń zaznaczone
            </button>

            <button onclick={cancelSelection} class="flex h-9 w-9 items-center justify-center rounded-full bg-gray-100 text-gray-500 transition-colors hover:bg-gray-200 hover:text-dark-text">
                <X size={18} />
            </button>
           
           
        </div>
    {/if}
</div>
