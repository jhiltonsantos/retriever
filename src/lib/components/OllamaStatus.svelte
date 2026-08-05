{#if visible}
	<div role="status" class="alert alert-warning text-sm mb-4">
		<div>
			<p class="font-semibold m-0">Ollama não detectado</p>
			<p class="text-sm mt-1 m-0 opacity-90">
				Instale o
				<a class="link" href="https://ollama.com/download" target="_blank" rel="noreferrer">
					Ollama
				</a>
				e baixe os modelos <code class="text-xs">llama3</code> e
				<code class="text-xs">nomic-embed-text</code>.
			</p>
		</div>
	</div>
{/if}

<script lang="ts">
	import { onMount } from 'svelte';

	let visible = $state(false);

	onMount(async () => {
		if (window.retriever?.checkOllama) {
			const ok = await window.retriever.checkOllama();
			visible = !ok;
			return;
		}

		try {
			const res = await fetch('http://localhost:11434/api/tags');
			visible = !res.ok;
		} catch {
			visible = true;
		}
	});
</script>
