<script lang="ts">
    import { Maximize } from 'lucide-svelte';

    let { onClick, text = "Powiększ" } = $props<{
        onClick: () => void;
        text?: string;
    }>();
</script>

<button 
    onclick={onClick}
    class="group flex w-full items-center justify-center gap-2 rounded-lg bg-brand px-3 py-2 text-md 
    font-semibold text-white shadow-sm transition-all duration-200 hover:bg-brand/90 hover:shadow active:scale-95"
>
    <Maximize size={15} class="transition-transform duration-200 group-hover:scale-110" />
    {text}
</button>