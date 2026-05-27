<script lang="ts">
	import DragAndDrop from './DragAndDrop.svelte';
	import { invalidateAll } from '$app/navigation';

	let responseMessage: string = $state('');
	let isLoading: boolean = $state(false);
	let dropzone: ReturnType<typeof DragAndDrop>;

	async function handleImages(files: File[]) {
		isLoading = true;

		let sucessCount = 0;
		let errorCount = 0;

		for (let i = 0; i < files.length; i++) {
			responseMessage = `Wysyłanie pliku: ${i + 1} z ${files.length}...`;
			const formData = new FormData();
			formData.append('file', files[i]);

			try {
				const res = await fetch('http://localhost:8000/photos/upload/', {
					method: 'POST',
					body: formData
				});

				if (res.ok) {
					sucessCount++;
					responseMessage = `Sukces! Zdjęcie dodane.`;
				} else {
					errorCount++;
					responseMessage = `Błąd: Coś poszło nie tak`;
				}
			} catch (error) {
				console.error(error);
				errorCount++;
			}
		}

		try {
			await invalidateAll();
			if (dropzone) dropzone.reset();

			if (errorCount === 0) {
				responseMessage = `Sukces. Dodano ${sucessCount} zdjęć`;
			} else {
				responseMessage = `Zakończono. Dodano: ${sucessCount}, Błędy: ${errorCount}`;
			}
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="w-full text-center">
	<DragAndDrop bind:this={dropzone} onFilesDropped={handleImages} />

	{#if responseMessage}
		<p
			class="mt-4 rounded-lg p-3 text-center text-sm font-medium
            {isLoading
				? 'bg-blue-100 text-blue-700'
				: responseMessage.includes('Błąd')
					? 'bg-red-100 text-red-700'
					: 'bg-green-100 text-green-700'}"
		>
			{responseMessage}
		</p>
	{/if}
</div>
