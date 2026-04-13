<script lang="ts">
	import path from "path";
    import DragAndDrop from "./DragAndDrop.svelte";
    import { createCounter } from "./counter.svelte";
	import { form } from "$app/server";
    let name: string = $state('ziomek');
    
    const counter = createCounter();

    let responseMessage: string = $state('');
    let isLoading: boolean = $state(false);


    async function handleImage(file: File){
        console.log("Plik:", file);
        isLoading = true;
        const formData = new FormData();
        formData.append('file', file);
        try{
            const res = await fetch('http://localhost:8000/upload/',{
                method: 'POST',
                body: formData
            });

            if(res.ok){
                const result = await res.json()
                responseMessage = `sukces plik zapisany jako ${result.photo_id}`;
            }else{
                responseMessage = `coś poszło nie tak`;
            }
        }catch(error){
            console.error(error);
            responseMessage = "błąd po stronie serwera"
        }finally{
            isLoading = false;
        }
    }
</script>

<div class="p-8 text-center bg-gray-50 rounded-xl shadow-md max-w-lg mx-auto mt-10">
  <h1 class="text-3xl font-bold text-blue-600 mb-6">
    Witaj, {name}!
  </h1>
  
  <div class="mb-6 text-left">
    <label for="nameInput" class="block text-gray-700 text-sm font-bold mb-2">
      Jak masz na imię?
    </label>
    <input 
      id="nameInput"
      type="text" 
      bind:value={name} 
      placeholder="Wpisz swoje imię..."
      class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  </div>
  <DragAndDrop onFileDropped={handleImage}/>
  {#if responseMessage}
    <p class="mt-4 p-3 rounded-lg text-sm text-center font-medium
      {isLoading ? 'bg-blue-100 text-blue-700' : 
       responseMessage.includes('Błąd') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}"
    >
      {responseMessage}
    </p>
  {/if}
  
  <p class="text-gray-700 mb-6">
    Licznik wynosi: <strong class="text-xl">{counter.value}</strong>
  </p>

  <button 
    onclick={counter.increment}
    class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-6 rounded transition-colors"
  >
    Zwiększ licznik
  </button>
  <button 
    onclick={counter.decrement}
    class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-6 rounded transition-colors"
  >
    zmniejsz licznik
  </button>
</div>