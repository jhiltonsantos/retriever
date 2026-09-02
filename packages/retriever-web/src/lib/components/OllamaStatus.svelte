{#if visible}
	<div
		role="status"
		class="mx-8 mb-2 flex shrink-0 items-center gap-2 rounded-full bg-[var(--color-warning)]/10 px-4 py-2 text-xs text-[var(--color-warning)]"
	>
		<TriangleAlert size={14} class="shrink-0" />
		<span>
			Ollama não detectado. Instale o
			<a class="link" href="https://ollama.com/download" target="_blank" rel="noreferrer">
				Ollama
			</a>
			e baixe os modelos <code class="text-xs">llama3</code> e
			<code class="text-xs">nomic-embed-text</code>.
		</span>
	</div>
{/if}

<script lang="ts">
	import { onMount } from 'svelte';
	import { TriangleAlert } from '@lucide/svelte';

	let visible = $state(false);

	onMount(async () => {
		try {
			const res = await fetch('http://localhost:11434/api/tags');
			visible = !res.ok;
		} catch {
			visible = true;
		}
	});
</script>
