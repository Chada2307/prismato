<script lang="ts">
	import './layout.css';
	import UploadWidget from '$lib/components/UploadWidget.svelte';
	let { children } = $props();
</script>

{@render children()}

<UploadWidget />
