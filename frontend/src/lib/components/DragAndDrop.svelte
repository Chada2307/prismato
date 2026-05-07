<script lang="ts">
	let { onFileDropped } = $props<{ onFileDropped: (file: File) => void }>();
	let isDragging: boolean = $state(false);
	let imagePreview: string | null = $state(null);
	let selectedFile: File | null = $state(null);

	let fileInput: HTMLInputElement;

	export function reset(){
		selectedFile = null;
		imagePreview = null;	
		if(fileInput) fileInput.value = '';
	}

	function handleDragOver(e: DragEvent): void {
		e.preventDefault();
		isDragging = true;
	}
	function handleDragLeave(): void {
		isDragging = false;
	}
	function handleDrop(e: DragEvent): void {
		e.preventDefault();
		isDragging = false;
		if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
			processFile(e.dataTransfer.files[0]);
		}
	}
	function handleFileSelect(e: Event): void {
		const target = e.target as HTMLInputElement;
		if (target.files && target.files.length > 0) {
			processFile(target.files[0]);
		}
	}
	function processFile(file: File): void {
		if (file.type.startsWith('image/')) {
			selectedFile = file;
			imagePreview = URL.createObjectURL(file);
			if (onFileDropped) {
				onFileDropped(file);
			}
		} else {
			alert('podaj zdjecie');
		}
	}
</script>

<div class="mb-6 text-left">
	<label class="mb-2 block text-sm font-bold text-gray-700" for="Photo"> Photo </label>

	<div
		role="button"
		tabindex="0 "
		ondragover={handleDragOver}
		ondragleave={handleDragLeave}
		ondrop={handleDrop}
		onclick={() => fileInput.click()}
		onkeydown={(e) => e.key === 'Enter' && fileInput.click()}
		class="cursor-pointer rounded-xl border-2 border-dashed p-8 text-center transition-all duration-200
             {isDragging
			? 'scale-[1.02] border-blue-500 bg-blue-50'
			: 'border-gray-300 bg-white hover:bg-gray-50'}"
	>
		{#if imagePreview}
			<div class="flex flex-col items-center">
				<img
					src={imagePreview}
					alt="Podgląd"
					class="mb-4 max-h-48 rounded-lg object-cover shadow-sm"
				/>
				<p class="text-sm font-medium text-gray-600">{selectedFile?.name}</p>
				<p class="mt-1 text-xs text-gray-400">Click to change photo</p>
			</div>
		{:else}
			<div class="text-gray-500">
				<svg
					class="mx-auto mb-3 h-12 w-12 text-gray-400"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
					></path>
				</svg>
				<p class="font-medium text-gray-700">Drag and drop photo here</p>
				<p class="mt-1 text-sm">or click to choose file from the disk</p>
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
