<section class="card bg-base-200 border border-base-300">
	<div class="card-body gap-4">
		<header class="flex items-start gap-3">
			<span class="badge badge-accent font-mono">{'{ }'}</span>
			<div>
				<h2 class="card-title text-lg m-0">Embeddings</h2>
				<p class="text-sm text-base-content/60 mt-1">Sempre locais — sem opção de troca</p>
			</div>
		</header>

		<dl class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 text-sm">
			<dt class="text-base-content/60">Provedor</dt>
			<dd>Ollama local</dd>
			<dt class="text-base-content/60">Modelo</dt>
			<dd><code class="text-xs">nomic-embed-text</code></dd>
			<dt class="text-base-content/60">Status</dt>
			<dd>
				{#if checking}
					<span class="loading loading-spinner loading-xs"></span>
				{:else if online}
					<span class="badge badge-success badge-sm">conectado</span>
				{:else}
					<span class="badge badge-error badge-sm">indisponível</span>
				{/if}
			</dd>
		</dl>

		<div role="status" class="alert alert-info text-sm">
			<span>
				Os embeddings rodam sempre no Ollama local. Assim, o conteúdo que você indexa nunca sai
				da sua máquina — quando o LLM é remoto, só a pergunta e os trechos recuperados são
				enviados.
			</span>
		</div>
	</div>
</section>

<script lang="ts">
	import { onMount } from 'svelte';

	let checking = $state(true);
	let online = $state(false);

	onMount(async () => {
		try {
			if (window.retriever?.checkOllama) {
				online = await window.retriever.checkOllama();
				return;
			}
			const res = await fetch('http://localhost:11434/api/tags');
			online = res.ok;
		} catch {
			online = false;
		} finally {
			checking = false;
		}
	});
</script>
