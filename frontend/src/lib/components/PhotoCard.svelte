<script lang="ts">
	import { Heart, Trash } from 'lucide-svelte';

	let { title, date, size } = $props<{
		title: string;
		date: string;
		size: string;
	}>();
</script>

<div
	class="group flex cursor-pointer flex-col overflow-hidden rounded-prismato bg-white shadow-[0px_4px_12px_0px_rgba(52,52,52,0.05)] outline outline-1 outline-dark-text/5 transition-all hover:shadow-[0px_8px_24px_0px_rgba(52,52,52,0.12)]"
>
	<div class="relative aspect-square w-full bg-dark-text/5">
		<div class="flex h-full w-full items-center justify-center text-4xl text-dark-text/20">🏔️</div>

		<div
			class="absolute top-3 right-3 flex flex-col gap-2 opacity-0 transition-opacity duration-200 group-hover:opacity-100"
		>
			<button
				class="flex h-8 w-8 items-center justify-center rounded-full bg-brand/80 text-white backdrop-blur-md transition-colors hover:bg-brand"
			>
				<Heart size={18} />
			</button>
			<button
				class="flex h-8 w-8 items-center justify-center rounded-full bg-brand/80 text-white backdrop-blur-md transition-colors hover:bg-danger"
			>
				<Trash size={18} />
			</button>
		</div>
	</div>

	<div class="flex flex-col gap-1 p-4">
		<h3 class="truncate text-base font-semibold text-dark-text">{title}</h3>
		<p class="text-xs font-normal text-dark-text/60">{date} - {size}</p>
	</div>
</div>
