<script lang="ts">

    import { onMount } from 'svelte';
    import 'leaflet/dist/leaflet.css';
    import { PUBLIC_API_URL } from '$env/static/public';

    let mapElement: HTMLElement;
    let map: any;
    let photos: any[] = $state([]);
    let isLoading = $state(true);

    onMount(async () =>{
        const L = (await import('leaflet')).default;
        map = L.map(mapElement).setView([52.0693, 19.4803], 6);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18,
        }).addTo(map);

        try{
            const res = await fetch(`${PUBLIC_API_URL}/photos/map-data`);
            if(res.ok){
                photos = await res.json();

                photos.forEach(photo => {

                    const imageUrl = photo.thumbnail_url.startsWith('http')
                        ? photo.thumbnail_url
                        : `${PUBLIC_API_URL}${photo.thumbnail_url}`;
                    console.log(`${PUBLIC_API_URL}${photo.thumbnail_url}`);
                    const pinIcon = L.divIcon({
                        className: 'custom-pin',
                    html: `
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ef4444" stroke="#ffffff" stroke-width="2" style="width: 36px; height: 36px; filter: drop-shadow(0px 4px 4px rgba(0,0,0,0.3));">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0z" />
                    </svg>
                    `,
                    iconSize: [36, 36],
                    iconAnchor: [18, 36], 
                    popupAnchor: [0, -32] 
                    });

                    L.marker([photo.lat, photo.lng], { icon: pinIcon })
                     .addTo(map)
                     .bindPopup(`
                        <div class="p-1">
                            <img src="${imageUrl}" class="w-full rounded-md" />
                            <a href="/photos" class="block mt-2 text-center text-sm font-bold text-brand">Zobacz w galerii</a>
                        </div>
                     `);
                });
            }
        }catch(err){
            console.error(err);
        } finally{
            isLoading = false;
        }

        return () => {
            if (map) map.remove();
        };
    });
</script>
<div class="relative flex h-[calc(100vh-80px)] w-full flex-col overflow-hidden rounded-2xl border border-gray-200 bg-zinc-100 shadow-sm">
    {#if isLoading}
        <div class="absolute inset-0 z-10 flex items-center justify-center bg-white/80 backdrop-blur-sm">
            <span class="animate-pulse text-lg font-medium text-brand">Wczytywanie mapy świata...</span>
        </div>
    {/if}

    <div bind:this={mapElement} class="h-full w-full z-0"></div>
</div>

<style>
    :global(.leaflet-container img) {
        max-width: none !important;
        display: inline !important;
    }
    :global(.custom-pin) {
        background: transparent !important;
        border: none !important;
    }
    
    :global(.leaflet-popup-content-wrapper) {
        border-radius: 12px;
        overflow: hidden;
        padding: 0;
    }
    :global(.leaflet-popup-content) {
        margin: 8px;
    }
</style>