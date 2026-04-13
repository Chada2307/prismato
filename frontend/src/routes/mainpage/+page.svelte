<script lang="ts">
	import DragAndDrop from './DragAndDrop.svelte';
	import { createCounter } from './counter.svelte';
	let name: string = $state('ziomek');

	const counter = createCounter();

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
	<h1 class="mb-6 text-3xl font-bold text-blue-600">
		Witaj, {name}!
	</h1>

	<div class="mb-6 text-left">
		<label for="nameInput" class="mb-2 block text-sm font-bold text-gray-700">
			Jak masz na imię?
		</label>
		<input
			id="nameInput"
			type="text"
			bind:value={name}
			placeholder="Wpisz swoje imię..."
			class="w-full appearance-none rounded border px-3 py-2 text-gray-700 shadow focus:ring-2 focus:ring-blue-500 focus:outline-none"
		/>
	</div>
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

	<p class="mb-6 text-gray-700">
		Licznik wynosi: <strong class="text-xl">{counter.value}</strong>
	</p>

	<button
		onclick={counter.increment}
		class="rounded bg-blue-500 px-6 py-2 font-semibold text-white transition-colors hover:bg-blue-600"
	>
		Zwiększ licznik
	</button>
	<button
		onclick={counter.decrement}
		class="rounded bg-blue-500 px-6 py-2 font-semibold text-white transition-colors hover:bg-blue-600"
	>
		zmniejsz licznik
	</button>
</div>
