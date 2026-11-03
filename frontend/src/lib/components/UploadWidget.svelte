<script lang="ts">
    import { uploader } from '$lib/states/upload.svelte';
    import { ChevronDown, ChevronUp, CheckCircle, Loader2 } from 'lucide-svelte';
    
    let progress = $derived(
        uploader.totalFiles > 0 
        ? Math.round((uploader.uploadedFiles / uploader.totalFiles) * 100) 
        : 0
    );
</script>

{#if uploader.isUploading}
    <div class="fixed bottom-6 right-6 z-[100] w-80 overflow-hidden rounded-xl border border-gray-200 bg-white shadow-2xl transition-all">
        
        <button 
            class="flex w-full items-center justify-between bg-gray-50 p-3 hover:bg-gray-100"
            onclick={() => uploader.isMinimized = !uploader.isMinimized}
        >
            <div class="flex items-center gap-2">
                {#if progress === 100}
                    <CheckCircle size={18} class="text-green-500" />
                    <span class="text-sm font-bold text-gray-700">Wgrywanie ukończone</span>
                {:else}
                    <Loader2 size={18} class="animate-spin text-brand" />
                    <span class="text-sm font-bold text-gray-700">Przesyłanie w tle...</span>
                {/if}
            </div>
            {#if uploader.isMinimized}
                <ChevronUp size={18} class="text-gray-500" />
            {:else}
                <ChevronDown size={18} class="text-gray-500" />
            {/if}
        </button>

        {#if !uploader.isMinimized}
            <div class="p-4">
                <div class="mb-2 h-2 w-full overflow-hidden rounded-full bg-gray-100">
                    <div 
                        class="h-full bg-brand transition-all duration-300" 
                        style="width: {progress}%"
                    ></div>
                </div>
                <div class="flex justify-between text-xs font-medium text-gray-500">
                    <span>Wysłano: {uploader.uploadedFiles} / {uploader.totalFiles}</span>
                    <span>{progress}%</span>
                </div>
                {#if uploader.errorCount > 0}
                    <div class="mt-2 text-xs text-red-500">Błędy: {uploader.errorCount}</div>
                {/if}
            </div>
        {/if}
    </div>
{/if}