<script lang="ts">
	import { Heart, Trash, Loader2 } from 'lucide-svelte';
	import { invalidateAll } from '$app/navigation';

	let { id, title, date, size, thumbnail_url, captured_at, camera_model, onDelete } = $props<{
		id: string;
		title: string;
		date: string;
		size: string;
		thumbnail_url: string;
		captured_at: string;
		camera_model: string;
		onDelete: () => Promise<void>;
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

	const BASE_URL = 'http://localhost:8000';
	const fullImageUrl = thumbnail_url.startsWith('http')
		? thumbnail_url
		: `${BASE_URL}${thumbnail_url}`;

	const dateFormatted = new Date(captured_at).toLocaleDateString('pl-PL', {
		day: 'numeric',
		month: 'long',
		year: 'numeric'
	});
</script>

<div
	class="group flex cursor-pointer flex-col overflow-hidden rounded-prismato border border-dark-text/5 bg-white shadow-sm transition-all hover:shadow-md"
>
	<div class="relative aspect-square w-full overflow-hidden bg-zinc-100">
		<img
			src={fullImageUrl}
			alt={camera_model}
			class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
			loading="lazy"
		/>

		<div
			class="absolute top-3 right-3 flex flex-col gap-2 opacity-0 transition-opacity duration-200 group-hover:opacity-100"
		>
			<button
				class="flex h-10 w-10 cursor-pointer items-center justify-center rounded-full bg-brand/80 text-white backdrop-blur-md hover:bg-danger"
			>
				<Heart size={18} />
			</button>
			<button
				onclick={handleDelete}
				disabled={isDeleting}
				class="flex h-10 w-10 cursor-pointer items-center justify-center rounded-full bg-brand/80 text-white backdrop-blur-md hover:bg-danger"
			>
				{#if isDeleting}
					<Loader2 size={18} class="animate-spin" />
				{:else}
					<Trash size={18} />
				{/if}
			</button>
		</div>
	</div>

	<div class="flex flex-col gap-0.5 p-4">
		<h3 class="truncate text-sm font-semibold text-dark-text">{camera_model}</h3>
		<p class="text-[10px] font-normal tracking-wider text-dark-text/50 uppercase">
			{dateFormatted}
		</p>
	</div>
</div>
