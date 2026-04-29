<script lang="ts">
	import { goto } from '$app/navigation';

	let username = $state('');
	let password = $state('');
	let isLoading = $state(false);

	async function handleLogin(e: Event) {
		e.preventDefault();
		isLoading = true;

		await new Promise((resolve) => setTimeout(resolve, 800));

		if (username === 'admin' && password === 'admin') {
			goto('/dashboard');
		} else {
			alert('Błędne dane! Użyj admin / admin');
			isLoading = false;
		}
	}
</script>

<div class="flex min-h-screen w-full items-center justify-center bg-main-bg p-4 font-['Inter']">
	<div
		class="flex w-full max-w-[600px] flex-col items-center gap-10 rounded-2xl bg-white p-12 shadow-[0px_4px_64px_0px_rgba(52,52,52,0.10)]"
	>
		<div class="flex flex-col items-center gap-4">
			<h1 class="text-6xl font-bold tracking-tight text-brand">PRISMATO</h1>
			<h2 class="text-3xl font-bold text-dark-text">Log In</h2>
		</div>

		<form onsubmit={handleLogin} class="flex w-full max-w-sm flex-col gap-6">
			<input
				type="text"
				placeholder="Username"
				bind:value={username}
				required
				class="h-12 w-full rounded-lg bg-main-bg px-4 text-xl text-dark-text outline outline-1 outline-dark-text/30 transition-all placeholder:text-dark-text/50 focus:outline-2 focus:outline-brand"
			/>

			<input
				type="password"
				placeholder="Password"
				bind:value={password}
				required
				class="h-12 w-full rounded-lg bg-main-bg px-4 text-xl text-dark-text outline outline-1 outline-dark-text/30 transition-all placeholder:text-dark-text/50 focus:outline-2 focus:outline-brand"
			/>

			<button
				type="submit"
				disabled={isLoading}
				class="mt-4 flex h-12 w-full items-center justify-center rounded-3xl bg-brand text-2xl font-normal text-white transition-colors hover:bg-brand-light disabled:opacity-70"
			>
				{isLoading ? 'Loading...' : 'Log In'}
			</button>
		</form>
	</div>
</div>
