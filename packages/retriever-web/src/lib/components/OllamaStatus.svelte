{#if embeddings.loaded && embeddings.status !== 'ready' && embeddings.provider === 'ollama'}
	<div
		role="status"
		class="mx-8 mb-2 flex shrink-0 items-center gap-2 rounded-full bg-[var(--color-warning)]/10 px-4 py-2 text-xs text-[var(--color-warning)]"
	>
		<TriangleAlert size={14} class="shrink-0" />
		{#if embeddings.status === 'model_missing'}
			<span>
				Ollama detectado, mas falta o modelo de embeddings. Rode
				<code class="text-xs">ollama pull {embeddings.model}</code> e valide em Configurações.
			</span>
		{:else}
			<span>
				Ollama não detectado. Instale o
				<a class="link" href={OLLAMA_DOWNLOAD_URL} onclick={externalLinkHandler(OLLAMA_DOWNLOAD_URL)}>
					Ollama
				</a>
				e baixe o modelo <code class="text-xs">{embeddings.model}</code>.
			</span>
		{/if}
	</div>
{/if}

<script lang="ts">
	import { onMount } from 'svelte';
	import { TriangleAlert } from '@lucide/svelte';
	import { getEmbeddingsState, watchEmbeddingsStatus } from '$lib/embeddings-status.svelte';
	import { externalLinkHandler } from '$lib/external-link';

	const OLLAMA_DOWNLOAD_URL = 'https://ollama.com/download';
	const embeddings = getEmbeddingsState();

	onMount(watchEmbeddingsStatus);
</script>
