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
		<dd>Ollama local</dd>
		<dt class="text-[var(--color-outline)]">Modelo</dt>
		<dd><code class="text-sm">nomic-embed-text</code></dd>
		<dt class="text-[var(--color-outline)]">Status</dt>
		<dd>
			{#if checking}
				<span class="loading loading-spinner loading-xs"></span>
			{:else if online}
				<span class="badge badge-success p-2 badge-sm">Conectado</span>
			{:else}
				<span class="badge badge-error p-2 badge-sm">Indisponível</span>
			{/if}
		</dd>
	</dl>
</section>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Layers, Info } from '@lucide/svelte';
	import { showAlert } from '$lib/alerts.svelte';

	const EMBEDDINGS_EXPLANATION =
		'Embeddings sao vetores numericos que representam o significado de um trecho de texto — e o que permite o tutor "buscar" o conteudo mais relevante pra responder sua pergunta.\n\n' +
		'Essa etapa roda sempre no Ollama local, independente do provedor de LLM escolhido em Provedores. Assim, o conteudo que voce indexa (PDFs, textos) nunca sai da sua maquina.\n\n' +
		'O modelo usado e o "nomic-embed-text". Trocar de modelo de embeddings exigiria reindexar tudo (vetores de modelos diferentes nao sao compativeis entre si), por isso essa opcao nao e configuravel.';

	let checking = $state(true);
	let online = $state(false);

	async function onInfoClick() {
		await showAlert(EMBEDDINGS_EXPLANATION, { title: 'Embeddings' });
	}

	onMount(async () => {
		try {
			const res = await fetch('http://localhost:11434/api/tags');
			online = res.ok;
		} catch {
			online = false;
		} finally {
			checking = false;
		}
	});
</script>
