<section class="flex flex-col gap-4">
	<header class="flex items-start gap-3">
		<span
			class="flex size-12 shrink-0 items-center justify-center rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
		>
			<Layers size={20} />
		</span>
		<div>
			<div class="flex items-center gap-2">
				<h2 class="m-0 text-lg font-semibold text-[var(--color-on-surface)]">Embeddings</h2>
				<button
					type="button"
					class="btn btn-ghost btn-circle btn-xs"
					onclick={onInfoClick}
					aria-label="O que é isso?"
				>
					<Info size={18} />
				</button>
			</div>
			<p class="mt-1 text-sm text-[var(--color-outline)]">Sempre locais — sem opção de troca</p>
		</div>
	</header>

	<dl class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 pt-1 text-sm">
		<dt class="text-[var(--color-outline)]">Provedor</dt>
		<dd>{embeddings.provider === 'ollama' ? 'Ollama local' : embeddings.provider}</dd>
		<dt class="text-[var(--color-outline)]">Modelo</dt>
		<dd><code class="text-sm">{embeddings.model}</code></dd>
		<dt class="text-[var(--color-outline)]">Status</dt>
		<dd>
			{#if embeddings.checking && !embeddings.loaded}
				<span class="loading loading-spinner loading-xs"></span>
			{:else if embeddings.status === 'ready'}
				<span class="badge badge-success p-2 badge-sm">Conectado</span>
			{:else if embeddings.status === 'model_missing'}
				<span class="badge badge-warning p-2 badge-sm">Modelo ausente</span>
			{:else}
				<span class="badge badge-error p-2 badge-sm">Indisponível</span>
			{/if}
		</dd>
	</dl>

	{#if embeddings.status !== 'ready' && embeddings.provider === 'ollama'}
		<div class="flex flex-col gap-3 rounded-2xl bg-[var(--color-surface-container)] p-4 text-sm">
			<p class="m-0 font-semibold text-[var(--color-on-surface)]">Como configurar</p>
			<ol class="m-0 flex list-decimal flex-col gap-2 pl-5 text-[var(--color-on-surface-variant)]">
				<li>
					Instale o
					<a class="link" href={OLLAMA_DOWNLOAD_URL} onclick={externalLinkHandler(OLLAMA_DOWNLOAD_URL)}>
						Ollama
					</a>
					e deixe-o em execução.
				</li>
				<li>
					No terminal, baixe o modelo:
					<code class="text-sm">ollama pull {embeddings.model}</code>
				</li>
				<li>Clique em Validar para o Retriever conferir.</li>
			</ol>
		</div>
	{/if}

	<div>
		<button
			type="button"
			class="btn btn-outline btn-sm rounded-full"
			disabled={embeddings.checking}
			onclick={() => void refreshEmbeddingsStatus()}
		>
			{#if embeddings.checking}
				<span class="loading loading-spinner loading-xs"></span>
			{/if}
			Validar
		</button>
	</div>
</section>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Layers, Info } from '@lucide/svelte';
	import { showAlert } from '$lib/alerts.svelte';
	import {
		getEmbeddingsState,
		refreshEmbeddingsStatus,
		watchEmbeddingsStatus
	} from '$lib/embeddings-status.svelte';
	import { externalLinkHandler } from '$lib/external-link';

	const EMBEDDINGS_EXPLANATION =
		'Embeddings sao vetores numericos que representam o significado de um trecho de texto — e o que permite o tutor "buscar" o conteudo mais relevante pra responder sua pergunta.\n\n' +
		'Essa etapa roda sempre no Ollama local, independente do provedor de LLM escolhido em Provedores. Assim, o conteudo que voce indexa (PDFs, textos) nunca sai da sua maquina.\n\n' +
		'O modelo usado e o "nomic-embed-text". Trocar de modelo de embeddings exigiria reindexar tudo (vetores de modelos diferentes nao sao compativeis entre si), por isso essa opcao nao e configuravel.';

	const OLLAMA_DOWNLOAD_URL = 'https://ollama.com/download';
	const embeddings = getEmbeddingsState();

	async function onInfoClick() {
		await showAlert(EMBEDDINGS_EXPLANATION, { title: 'Embeddings' });
	}

	onMount(watchEmbeddingsStatus);
</script>
