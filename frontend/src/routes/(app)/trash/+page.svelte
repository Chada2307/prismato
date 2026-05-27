<script lang="ts">
	import PhotoCard from '$lib/components/PhotoCard.svelte';

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

	$effect(() => {
		photos = data.photos;
		offset = data.photos.length;
		hasMore = data.photos.length >= 20;
	});

	async function loadMore() {
		isLoadingMore = true;
		try {
			const res = await fetch(`http://localhost:8000/trash?skip=${offset}&limit=20`);
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
		const res = await fetch(`http://localhost:8000/trash/${photoId}`, { method: 'DELETE' });
		if (res.ok) {
			photos = photos.filter((photo) => photo.id !== photoId);
			offset -= 1;
		} else {
			alert('Nie udało usunąć');
			throw new Error('błąd');
		}
	}
</script>

<div class="flex flex-col gap-8">
	<header>
		<h2 class="text-3xl font-bold text-dark-text">Twój śmietnik</h2>
		<p class="text-dark-text/60">Znaleziono {photos.length} zdjęć</p>
	</header>

	<div class="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
		{#each photos as photo (photo.id)}
			<PhotoCard
				id={photo.id}
				thumbnail_url={photo.thumbnail_url}
				captured_at={photo.captured_at}
				camera_model={photo.camera_model}
				onDelete={() => hardDelete(photo.id)}
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
</div>
