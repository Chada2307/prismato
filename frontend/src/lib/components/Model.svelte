<script lang="ts">
	//import UploadCard from './UploadCard.svelte';
	let { showModal = $bindable(), header, children } = $props();

	let dialog = $state<HTMLDialogElement>();

	import DragAndDrop from '../../routes/(app)/dashboard/DragAndDrop.svelte';

	let responseMessage: string = $state('');
	let isLoading: boolean = $state(false);

	async function handleImage(file: File) {
		console.log('Plik:', file);
		isLoading = true;
		const formData = new FormData();
		formData.append('file', file);
		try {
			const res = await fetch('http://localhost:8000/upload/', {
				method: 'POST',
				body: formData
			});

			if (res.ok) {
				const result = await res.json();
				responseMessage = `sukces plik zapisany jako ${result.photo_id}`;
			} else {
				responseMessage = `coś poszło nie tak`;
			}
		} catch (error) {
			console.error(error);
			responseMessage = 'błąd po stronie serwera';
		} finally {
			isLoading = false;
		}
	}

	$effect(() => {
		if (showModal) dialog?.showModal();
	});
</script>

<dialog
	bind:this={dialog}
	onclose={() => (showModal = false)}
	onclick={(e) => {
		if (e.target === dialog) dialog.close();
	}}
	class="fixed inset-0 z-50 m-auto h-fit w-[95%] max-w-lg rounded-2xl border-none bg-white p-0 shadow-2xl backdrop:bg-black/50 backdrop:backdrop-blur-sm"
>
	<div class="flex min-w-[300px] flex-col items-center justify-center gap-4">
		<DragAndDrop onFileDropped={handleImage} />

		{#if responseMessage}
			<p
				class="mt-4 rounded-lg p-3 text-center text-sm font-medium
                {isLoading
					? 'bg-blue-100 text-blue-700'
					: responseMessage.includes('błąd') || responseMessage.includes('coś')
						? 'bg-red-100 text-red-700'
						: 'bg-green-100 text-green-700'}"
			>
				{responseMessage}
			</p>
		{/if}

		<button
			class="flex h-10 items-center justify-center gap-2 rounded-lg bg-gray-200 px-4 font-medium text-black transition-colors hover:bg-gray-300"
			autofocus
			onclick={() => dialog?.close()}
		>
			Zamknij
		</button>
	</div>
</dialog>

<style>
	dialog {
		max-width: 32em;
		border-radius: 0.8em;
		border: none;
		padding: 2em;
	}
	dialog::backdrop {
		background: rgba(0, 0, 0, 0.5);
	}
	dialog > div {
		padding: 1em;
	}
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
	button {
		display: block;
	}
</style>
