<script lang="ts">
	import PhotoCard from '$lib/components/PhotoCard.svelte';

	const gallery = [
		{
			date: 'Today',
			photos: [
				{ title: 'IMG_2026_01.jpg', size: '2.4 MB' },
				{ title: 'IMG_2026_02.jpg', size: '3.1 MB' },
				{ title: 'IMG_2026_03.jpg', size: '1.8 MB' },
				{ title: 'IMG_2026_04.jpg', size: '4.2 MB' },
				{ title: 'IMG_2026_05.jpg', size: '2.1 MB' },
				{ title: 'IMG_2026_06.jpg', size: '5.0 MB' }
			]
		},
		{
			date: 'Yesterday',
			photos: [
				{ title: 'Wakacje_01.jpg', size: '2.4 MB' },
				{ title: 'Wakacje_02.jpg', size: '4.1 MB' },
				{ title: 'Wakacje_03.jpg', size: '1.2 MB' }
			]
		},
		{
			date: '12 May 2026',
			photos: [
				{ title: 'Pies.png', size: '5.0 MB' },
				{ title: 'Krajobraz.jpg', size: '2.1 MB' }
			]
		}
	];
</script>

<div class="flex flex-col gap-12">
	{#each gallery as group (group.date)}
		<section class="flex flex-col gap-6">
			<h2 class="font-['Inter'] text-3xl font-normal text-dark-text">
				{group.date}
			</h2>

			<div
				class="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6"
			>
				{#each group.photos as photo (photo)}
					<PhotoCard title={photo.title} date={group.date} size={photo.size} />
				{/each}
			</div>
		</section>
	{/each}
</div>
