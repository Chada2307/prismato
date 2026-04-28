<script lang="ts">
    import { goto } from '$app/navigation';
	let login: string = $state('')
    let passw: string = $state('')

    let errorMessage: string = $state('')
    let isLoading: boolean = $state(false);

    async function handleLogin(e: Event) {
        e.preventDefault();

        errorMessage = '';
        isLoading = true;

        await new Promise(resolve => setTimeout(resolve, 800));

        if(login === 'admin' && passw === 'admin'){
            goto('/mainpage');
        }else{
            errorMessage = 'bad login or passwd';
            isLoading = false;
        }
    }




</script>


<div class="flex min-h-screen w-full items-center justify-center bg-gray-50 p-4">
    <div class="flex w-full max-w-[592px] flex-col items-center gap-8 rounded-[29px] border border-gray-100 bg-white p-12 shadow-sm">
        <h1 class="mb-4 font-['Inter'] text-6xl font-normal text-black">Prismato</h1>

        <form onsubmit={handleLogin} class="flex w-full max-w-sm flex-col gap-4">
            
            <input
                id="login"
                type="text"
                bind:value={login}
                required
                placeholder="username"
                class="h-12 w-full rounded-[10px] bg-zinc-300 px-4 font-['Inter'] text-xl outline-none"
            />

            <input
                id="passw"
                type="password"
                bind:value={passw}
                required
                placeholder="password"
                class="h-12 w-full rounded-[10px] bg-zinc-300 px-4 font-['Inter'] text-xl outline-none"
            />

            {#if errorMessage}
                <p class="text-center text-sm text-red-500 font-['Inter']">{errorMessage}</p>
            {/if}

            <button
                type="submit"
                disabled={isLoading}
                class="mt-4 h-14 w-40 self-center rounded-[10px] bg-indigo-800/25 font-['Inter'] text-2xl text-black transition-colors hover:bg-indigo-800/40 disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {isLoading ? '...' : 'log in'}
            </button>
        </form>
    </div>
</div>
