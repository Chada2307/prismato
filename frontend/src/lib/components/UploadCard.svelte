<script lang="ts">
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
</script>

<div class="mx-auto mt-10 max-w-lg rounded-xl bg-gray-50 p-8 text-center shadow-md">
	<DragAndDrop onFileDropped={handleImage} />
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
