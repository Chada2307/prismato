<script lang="ts">
	let { showModal = $bindable(), children } = $props();
	let dialog = $state<HTMLDialogElement>();

	$effect(() => {
		if (showModal) {
			dialog?.showModal();
		} else {
			dialog?.close();
		}
	});
</script>

<dialog
	bind:this={dialog}
	onclose={() => (showModal = false)}
	onclick={(e) => {
		if (e.target === dialog) showModal = false;
	}}
	class="fixed inset-0 z-50 m-auto h-fit w-[95%] max-w-lg rounded-2xl border-none bg-white p-0 shadow-2xl backdrop:bg-black/50 backdrop:backdrop-blur-sm"
>
	<div class="flex min-w-[300px] flex-col items-center justify-center gap-4 p-6">
		{#if children}
			{@render children()}
		{/if}

		<button
			class="mt-4 flex h-10 w-full items-center justify-center gap-2 rounded-lg bg-gray-200 px-4 font-medium text-black transition-colors hover:bg-gray-300"
			onclick={() => (showModal = false)}
		>
			Zamknij
		</button>
	</div>
</dialog>

<style>
	dialog[open] {
		animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}
	@keyframes zoom {
		from {
			transform: scale(0.95);
		}
		to {
			transform: scale(1);
		}
	}
	dialog[open]::backdrop {
		animation: fade 0.2s ease-out;
	}
	@keyframes fade {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
</style>
