<script lang="ts">
	import { Image, Search, Map, Heart, Folder, Trash, Upload } from 'lucide-svelte';
	import { page } from '$app/state';
	import Model from '$lib/components/Model.svelte';
	import UploadCard from '$lib/components/UploadCard.svelte';
	let { children } = $props();

	let isModalOpen = $state(false);
</script>

<div class="flex h-screen overflow-hidden bg-main-bg font-['Inter']">
	<aside
		class="z-20 flex w-48 flex-col rounded-r-2xl bg-dark-text py-6 shadow-[4px_0_24px_rgba(0,0,0,0.15)]"
	>
		<div class="mt-2 mb-8 text-center text-3xl font-bold tracking-tight text-brand">PRISMATO</div>

		<nav class="flex flex-col gap-3 px-3">
			<a
				href="/photos"
				class="flex items-center gap-4 rounded-lg px-4 py-2.5 text-white transition-colors hover:bg-white/10 hover:text-brand
				{page.url.pathname === '/photos' ? 'bg-cyan-600/50 text-white' : 'bg-dark-text hover:text-white'}"
			>
				<span class="text-lg"><Image size={24} /></span>
				<span class="text-base font-normal">photos</span>
			</a>

			<a
				href="/search"
				class="flex items-center gap-4 rounded-lg px-4 py-2.5 text-white transition-colors hover:bg-white/10 hover:text-brand
				{page.url.pathname === '/search' ? 'bg-cyan-600/50 text-white' : 'bg-dark-text hover:text-white'}"
			>
				<span class="text-lg"><Search size={24} /></span>
				<span class="text-base font-normal">search</span>
			</a>

			<a
				href="/map"
				class="flex items-center gap-4 rounded-lg px-4 py-2.5 text-white transition-colors hover:bg-white/10 hover:text-brand-light
				{page.url.pathname === '/map' ? 'bg-cyan-600/50 text-white' : 'bg-dark-text hover:text-white'}"
			>
				<span class="text-lg"><Map size={24} /></span>
				<span class="text-base font-normal">map</span>
			</a>
		</nav>

		<nav class="mt-8 flex flex-col gap-3 px-3">
			<div class="mb-2 px-4 text-sm font-normal text-white/40">Library</div>

			<a
				href="/favourites"
				class="flex items-center gap-4 rounded-lg px-4 py-2.5 text-white transition-colors hover:bg-white/10 hover:text-brand-light
				{page.url.pathname === '/favourites'
					? 'bg-cyan-600/50 text-white'
					: 'bg-dark-text hover:text-white'}"
			>
				<span class="text-lg"><Heart size={24} /></span>
				<span class="text-base font-normal">favourites</span>
			</a>

			<a
				href="/albums"
				class="flex items-center gap-4 rounded-lg px-4 py-2.5 text-white transition-colors hover:bg-white/10 hover:text-brand-light
				{page.url.pathname === '/albums' ? 'bg-cyan-600/50 text-white' : 'bg-dark-text hover:text-white'}"
			>
				<span class="text-lg"><Folder size={24} /></span>
				<span class="text-base font-normal">albums</span>
			</a>

			<a
				href="/trash"
				class="flex items-center gap-4 rounded-lg px-4 py-2.5 text-white transition-colors hover:bg-white/10 hover:text-brand-light
				{page.url.pathname === '/trash' ? 'bg-cyan-600/50 text-white' : 'bg-dark-text hover:text-white'}"
			>
				<span class="text-lg"><Trash size={24} /></span>
				<span class="text-base font-normal">trash</span>
			</a>
		</nav>
	</aside>

	<div class="flex min-w-0 flex-1 flex-col">
		<header class="z-10 flex h-20 items-center justify-between bg-brand px-10 shadow-md">
			<div class="relative w-full max-w-[450px]">
				<input
					type="text"
					placeholder="search for..."
					class="h-10 w-full rounded-full bg-main-bg pr-4 pl-12 text-dark-text transition-all outline-none placeholder:text-dark-text/50 focus:ring-2 focus:ring-white"
				/>
				<span class="absolute top-2 left-4 text-dark-text/50"><Search size={24} /></span>
			</div>

			<div class="flex items-center gap-6">
				<button
					onclick={() => (isModalOpen = true)}
					class="flex h-10 cursor-pointer items-center justify-center gap-2 rounded-lg bg-main-bg px-4 font-medium text-dark-text transition-colors hover:bg-white hover:text-brand hover:ring-2 hover:ring-white"
				>
					<span><Upload size={24} /></span> upload
				</button>

				<div
					class="flex h-12 w-12 cursor-pointer items-center justify-center rounded-full bg-main-bg font-bold text-brand shadow-sm transition-transform hover:scale-105"
				>
					P
				</div>
			</div>
		</header>

		<main class="flex-1 overflow-y-auto p-10">
			{@render children()}
		</main>
	</div>
</div>
<Model bind:showModal={isModalOpen}>
	<UploadCard />
</Model>
