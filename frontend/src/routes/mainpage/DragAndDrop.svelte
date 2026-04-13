<script lang="ts">
    let { onFileDropped } = $props<{ onFileDropped: (file: File) => void }>();
    let isDragging: boolean = $state(false);
    let imagePreview: string | null = $state(null);
    let selectedFile: File | null = $state(null);

    let fileInput: HTMLInputElement;

    function handleDragOver(e: DragEvent): void{
        e.preventDefault();
        isDragging = true;
    }
    function handleDragLeave(): void {
        isDragging = false;
    }
    function handleDrop(e: DragEvent): void{
        e.preventDefault();
        isDragging = false;
        if(e.dataTransfer?.files && e.dataTransfer.files.length > 0){
            processFile(e.dataTransfer.files[0]);
        }
    }
    function handleFileSelect(e: Event): void{
        const target = e.target as HTMLInputElement;
        if(target.files && target.files.length > 0){
            processFile(target.files[0]);
        }
    }
    function processFile(file: File): void {
        if(file.type.startsWith('image/')){
            selectedFile = file;
            imagePreview = URL.createObjectURL(file);
            if(onFileDropped){
                onFileDropped(file);
            }
        } else {
            alert('podaj zdjecie');
        }
    }
</script>

<div class="mb-6 text-left">
    <label
        class="block text-gray-700 text-sm font-bold mb-2"
        for="Photo"    
    >

      Zdjęcie profilowe
    </label>
    
    <div 
      role="button"
      tabindex="0"
      ondragover={handleDragOver}
      ondragleave={handleDragLeave}
      ondrop={handleDrop}
      onclick={() => fileInput.click()}
      onkeydown={(e) => e.key === 'Enter' && fileInput.click()}
      class="border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200 
             {isDragging ? 'border-blue-500 bg-blue-50 scale-[1.02]' : 'border-gray-300 bg-white hover:bg-gray-50'}"
    >
      {#if imagePreview}
        <div class="flex flex-col items-center">
          <img src={imagePreview} alt="Podgląd" class="max-h-48 rounded-lg mb-4 shadow-sm object-cover" />
          <p class="text-sm text-gray-600 font-medium">{selectedFile?.name}</p>
          <p class="text-xs text-gray-400 mt-1">Kliknij, aby zmienić zdjęcie</p>
        </div>
      {:else}
        <div class="text-gray-500">
          <svg class="mx-auto h-12 w-12 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
          </svg>
          <p class="font-medium text-gray-700">Przeciągnij i upuść zdjęcie tutaj</p>
          <p class="text-sm mt-1">lub kliknij, aby wybrać z dysku</p>
        </div>
      {/if}
    </div>

    <input 
      bind:this={fileInput}
      type="file" 
      accept="image/*" 
      class="hidden" 
      onchange={handleFileSelect} 
    />
  </div>