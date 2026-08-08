<div class="flex shrink-0 justify-end p-8">
	<button
		type="button"
		class="btn btn-circle btn-ghost size-10"
		onclick={toggleTheme}
		aria-label={theme === 'retriever-dark' ? 'Mudar para tema claro' : 'Mudar para tema escuro'}
	>
		{#if theme === 'retriever-dark'}
			<Sun size={20} />
		{:else}
			<Moon size={20} />
		{/if}
	</button>
</div>

<script lang="ts">
	import { Sun, Moon } from '@lucide/svelte';
	import { getTheme, toggleTheme } from '$lib/theme.svelte';

	const theme = $derived(getTheme());
</script>
