<script lang="ts">
    import DragAndDrop from './DragAndDrop.svelte';
    import { uploader } from '$lib/states/upload.svelte';

    let { onCloseModal } = $props<{ onCloseModal?: () => void }>();

    let dropzone: ReturnType<typeof DragAndDrop>;

    function handleImages(files: File[]) {
        if (files.length === 0) return;

        
        uploader.startUpload(files);

        
        if (dropzone) dropzone.reset();

        
        if (onCloseModal) {
            onCloseModal();
        }
    }
</script>

<div class="w-full text-center">
    
    <DragAndDrop bind:this={dropzone} onFilesDropped={handleImages} />
</div>