<script lang="ts">
	
	import PhotoCard from '$lib/components/PhotoCard.svelte';

		let { data } = $props();
	

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
    <p class="text-dark-text/60">Znaleziono {data.photos.length} zdjęć</p>
  </header>

  <div class="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
    {#each data.photos as photo (photo.id)}
      <PhotoCard 
        thumbnail_url={photo.thumbnail_url}
        captured_at={photo.captured_at}
        camera_model={photo.camera_model}
      />
    {/each}
  </div>
</div>
