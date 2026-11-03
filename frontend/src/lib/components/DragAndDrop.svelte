<script lang="ts">
    let { 
        onFilesDropped,
        disabled = false 
    } = $props<{ 
        onFilesDropped: (file: File[]) => void;
        disabled?: boolean;
    }>();
    
    let isDragging: boolean = $state(false);
    let imagePreviews: string[] = $state([]);
    let selectedFiles: File[] = $state([]);

    let fileInput: HTMLInputElement;
    let folderInput: HTMLInputElement;

    export function reset() {
        imagePreviews.forEach((url) => URL.revokeObjectURL(url));
        selectedFiles = [];
        imagePreviews = [];
        if (fileInput) fileInput.value = '';
        if (folderInput) folderInput.value = '';
    }

    function handleDragOver(e: DragEvent): void {
        if (disabled) return;
        e.preventDefault();
        isDragging = true;
    }
    
    function handleDragLeave(): void {
        if (disabled) return;
        isDragging = false;
    }
    async function handleDrop(e: DragEvent) {
        if (disabled) return;
        e.preventDefault();
        isDragging = false;

        const items = e.dataTransfer?.items;
        if (!items) return;

        const extractedFiles: File[] = [];

        async function readEntry(entry: any) {
            if (entry.isFile) {
                return new Promise<void>((resolve) => {
                    entry.file((file: File) => {
                        extractedFiles.push(file);
                        resolve();
                    });
                });
            } else if (entry.isDirectory) {
                const dirReader = entry.createReader();
                return new Promise<void>((resolve) => {
                    dirReader.readEntries(async (entries: any[]) => {
                        for (const childEntry of entries) {
                            await readEntry(childEntry);
                        }
                        resolve();
                    });
                });
            }
        }

        const promises = [];
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            if (item.kind === 'file') {
                const entry = item.webkitGetAsEntry();
                if (entry) {
                    promises.push(readEntry(entry));
                }
            }
        }

        await Promise.all(promises);
        
        processFiles(extractedFiles);
    }
    
    function handleFileSelect(e: Event): void {
        if (disabled) return;
        const target = e.target as HTMLInputElement;
        if (target.files && target.files.length > 0) {
            processFiles(Array.from(target.files));
        }
    }
    
    function processFiles(files: File[]): void {
        const validFiles = files.filter((file) => file.type.startsWith('image/'));

        if (validFiles.length > 0) {
            selectedFiles = validFiles;
            imagePreviews = [URL.createObjectURL(validFiles[0])];
            
            if (onFilesDropped) {
                onFilesDropped(validFiles);
            }
        } else {
            alert('Brak poprawnych plików graficznych w tym folderze/zaznaczeniu.');
        }
    }
</script>

<div class="mb-6 text-left {disabled ? 'opacity-50 pointer-events-none' : ''}">
    <label class="mb-2 block text-sm font-bold text-gray-700" for="Photo"> Wybierz zdjęcia lub foldery </label>

    <div
        role="region"
        aria-label="Obszar zrzucania plików"
        ondragover={handleDragOver}
        ondragleave={handleDragLeave}
        ondrop={handleDrop}
        class="rounded-xl border-2 border-dashed p-8 text-center transition-all duration-200
             {isDragging
            ? 'scale-[1.02] border-brand bg-brand/5'
            : 'border-gray-300 bg-white hover:bg-gray-50'}"
    >
        {#if imagePreviews.length > 0}
            <div class="flex flex-col items-center">
                <img
                    src={imagePreviews[0]}
                    alt="Podgląd"
                    class="mb-4 max-h-48 rounded-lg object-cover shadow-sm"
                />
                <p class="text-sm font-medium text-gray-600">Wybrano plików: {selectedFiles.length}</p>
                {#if selectedFiles.length > 1}
                    <p class="text-xs text-gray-500">(+{selectedFiles.length - 1} innych)</p>
                {/if}
            </div>
        {:else}
            <div class="flex flex-col items-center justify-center text-gray-500">
                <svg class="mb-3 h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
                </svg>
                <p class="font-medium text-gray-700">Przeciągnij i upuść pliki lub foldery tutaj</p>
                
                <div class="mt-4 flex items-center justify-center gap-3">
                    <button
                        type="button"
                        class="rounded-lg bg-gray-100 px-4 py-2 text-sm font-semibold text-dark-text transition-colors hover:bg-gray-200"
                        onclick={(e) => {
                            e.stopPropagation();
                            if (!disabled) fileInput.click();
                        }}
                    >
                        Wybierz pliki
                    </button>
                    <span class="text-sm text-gray-400">lub</span>
                    <button
                        type="button"
                        class="rounded-lg bg-brand/10 px-4 py-2 text-sm font-semibold text-brand transition-colors hover:bg-brand/20"
                        onclick={(e) => {
                            e.stopPropagation();
                            if (!disabled) folderInput.click();
                        }}
                    >
                        Wybierz folder
                    </button>
                </div>
            </div>
        {/if}
    </div>

    <input
        bind:this={fileInput}
        type="file"
        accept="image/*"
        multiple
        class="hidden"
        onchange={handleFileSelect}
        {disabled}
    />
    <input
        bind:this={folderInput}
        type="file"
        accept="image/*"
        multiple
        webkitdirectory
        class="hidden"
        onchange={handleFileSelect}
        {disabled}
    />
</div>