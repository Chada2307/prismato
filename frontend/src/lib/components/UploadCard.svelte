<script lang="ts">
    import DragAndDrop from './DragAndDrop.svelte';
    import { invalidateAll } from '$app/navigation';
    import { PUBLIC_API_URL } from '$env/static/public';

    let responseMessage: string = $state('');
    let isLoading: boolean = $state(false);
    let dropzone: ReturnType<typeof DragAndDrop>;

    let totalFiles = $state(0);
    let uploadedFiles = $state(0);
    let errorCount = $state(0);

    async function handleImages(files: File[]) {
        if (files.length === 0) return;

        isLoading = true;
        totalFiles = files.length;
        uploadedFiles = 0;
        errorCount = 0;
        responseMessage = '';

        for (let i = 0; i < files.length; i++) {
            const formData = new FormData();
            formData.append('file', files[i]);

            try {
                const res = await fetch(`${PUBLIC_API_URL}/photos/upload/`, {
                    method: 'POST',
                    body: formData
                });

                if (res.ok) {
                    uploadedFiles++;
                } else {
                    errorCount++;
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
                responseMessage = `Sukces. Dodano ${uploadedFiles} zdjęć!`;
            } else {
                responseMessage = `Zakończono. Dodano: ${uploadedFiles}, Błędy: ${errorCount}`;
            }
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="w-full text-center">
    <DragAndDrop bind:this={dropzone} onFilesDropped={handleImages} disabled={isLoading} />

    {#if isLoading && totalFiles > 0}
        <div class="mt-6 rounded-xl border border-brand bg-brand/5 p-6 text-center shadow-sm">
            <h3 class="mb-3 text-sm font-bold uppercase tracking-wider text-dark-text/70">
                Przesyłanie do biblioteki...
            </h3>
            
            <div class="h-2 w-full overflow-hidden rounded-full bg-gray-200">
                <div 
                    class="h-full bg-brand transition-all duration-300" 
                    style="width: {(uploadedFiles / totalFiles) * 100}%"
                ></div>
            </div>
            
            <div class="mt-3 flex justify-between text-sm font-medium">
                <span class="text-brand">{uploadedFiles} / {totalFiles}</span>
                {#if errorCount > 0}
                    <span class="text-red-500">Błędy: {errorCount}</span>
                {/if}
            </div>
        </div>
    {/if}

    {#if responseMessage && !isLoading}
        <p
            class="mt-4 rounded-lg p-3 text-center text-sm font-medium
            {responseMessage.includes('Błąd') || responseMessage.includes('Błędy')
                ? 'bg-red-100 text-red-700'
                : 'bg-green-100 text-green-700'}"
        >
            {responseMessage}
        </p>
    {/if}
</div>