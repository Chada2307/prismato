<script lang="ts">
    let name: string = $state('ziomek');
    let count: number = $state(0);

    function increment(): void {
        count += 1;
    }


</script>

<div class="p-8 text-center bg-gray-50 rounded-xl shadow-md max-w-md mx-auto mt-10">
    <h1 class="text-3xl font-bold text-blue-600 mb-4">
        witaj {name}
    </h1>

    <p class="text-gray-700 mb-6">
        licznik wynosi: <strong class="text-xl">{count}</strong>
    </p>
    <button
        onclick={increment}
        class="bg-blue-500 hover:bg-blue-300 text-white font-semibold py-2 px-4 rounded"
    >
        zwieksz licznik
    </button>
    
</div>

<div class="p-8 text-center bg-gray-50 rounded-xl shadow-md max-w-md mx-auto mt-10">
<label for="nameInput">
        podaj imie
    </label>
    <input type="text" id="nameInput" bind:value={name}>
    
</div>
