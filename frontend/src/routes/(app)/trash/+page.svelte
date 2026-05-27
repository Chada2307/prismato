<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import PhotoCard from '$lib/components/PhotoCard.svelte';
	let { data } = $props();

	async function hardDelete(photoId: string) {
		const res = await fetch(`http://localhost:8000/trash/${photoId}`, { method: 'DELETE' });
		if (res.ok) {
			await invalidateAll();
		} else {
			alert('Nie udało sie przenieść do kosza');
			throw new Error('błąd');
		}
	}
</script>

<div class="flex flex-col gap-8">
	<header>
		<h2 class="text-3xl font-bold text-dark-text">Twoja Galeria</h2>
		<p class="text-dark-text/60">Znaleziono {data.photos.length} zdjęć</p>
	</header>

	<div class="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
		{#each data.photos as photo (photo.id)}
			<PhotoCard
				id={photo.id}
				thumbnail_url={photo.thumbnail_url}
				captured_at={photo.captured_at}
				camera_model={photo.camera_model}
				onDelete={() => hardDelete(photo.id)}
			/>
		{/each}
	</div>
</div>
