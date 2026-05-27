<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import PhotoCard from '$lib/components/PhotoCard.svelte';
	import { Loader2 } from 'lucide-svelte';

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
			const res = await fetch(`http://localhost:8000/photos?skip=${offset}&limit=20`);
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

	async function moveToTrash(photoId: string) {
		const res = await fetch(`http://localhost:8000/photos/${photoId}`, { method: 'DELETE' });
		if (res.ok) {
			photos = photos.filter((photo) => photo.id !== photoId);
			offset -= 1;
		} else {
			alert('Nie udało sie przenieść do kosza');
			throw new Error('błąd');
		}
	}

	// const gallery = [
	// 	{
	// 		date: 'Today',
	// 		type: [
	// 			{ title: 'IMG_2026_01.jpg', size: '2.4 MB' },
	// 			{ title: 'IMG_2026_02.jpg', size: '3.1 MB' },
	// 			{ title: 'IMG_2026_03.jpg', size: '1.8 MB' },
	// 			{ title: 'IMG_2026_04.jpg', size: '4.2 MB' },
	// 			{ title: 'IMG_2026_05.jpg', size: '2.1 MB' },
	// 			{ title: 'IMG_2026_06.jpg', size: '5.0 MB' }
	// 		]
	// 	},
	// 	{
	// 		date: 'Yesterday',
	// 		type: [
	// 			{ title: 'Wakacje_01.jpg', size: '2.4 MB' },
	// 			{ title: 'Wakacje_02.jpg', size: '4.1 MB' },
	// 			{ title: 'Wakacje_03.jpg', size: '1.2 MB' }
	// 		]
	// 	},
	// 	{
	// 		date: '12 May 2026',
	// 		photos: [
	// 			{ title: 'Pies.png', size: '5.0 MB' },
	// 			{ title: 'Krajobraz.jpg', size: '2.1 MB' }
	// 		]
	// 	}
	// ];
</script>

<div class="flex flex-col gap-8">
	<header>
		<h2 class="text-3xl font-bold text-dark-text">Twoja Galeria</h2>
		<p class="text-dark-text/60">Znaleziono {photos.length} zdjęć</p>
	</header>

	<div class="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
		{#each photos as photo (photo.id)}
			<PhotoCard
				id={photo.id}
				thumbnail_url={photo.thumbnail_url}
				captured_at={photo.captured_at}
				camera_model={photo.camera_model}
				onDelete={() => moveToTrash(photo.id)}
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
