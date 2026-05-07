<script lang="ts">
    import DragAndDrop from './DragAndDrop.svelte';
    import { invalidateAll } from '$app/navigation';

    let responseMessage: string = $state('');
    let isLoading: boolean = $state(false);
    let dropzone: ReturnType<typeof DragAndDrop>;
    
    async function handleImage(file: File) {
        isLoading = true;
        responseMessage = 'Wysyłanie pliku...';
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const res = await fetch('http://localhost:8000/upload/', {
                method: 'POST',
                body: formData
            });

            if (res.ok) {
                await invalidateAll(); 
                
                if (dropzone) dropzone.reset();
                
                responseMessage = `Sukces! Zdjęcie dodane.`;
            } else {
                responseMessage = `Błąd: Coś poszło nie tak`;
            }
        } catch (error) {
            console.error(error);
            responseMessage = 'Błąd po stronie serwera';
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="w-full text-center">
    <DragAndDrop bind:this={dropzone} onFileDropped={handleImage} />
    
    {#if responseMessage}
        <p class="mt-4 rounded-lg p-3 text-center text-sm font-medium
            {isLoading ? 'bg-blue-100 text-blue-700' : 
             responseMessage.includes('Błąd') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}">
            {responseMessage}
        </p>
    {/if}
</div>