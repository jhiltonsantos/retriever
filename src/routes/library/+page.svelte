<h2 class="m-0 font-['Comfortaa'] text-2xl font-semibold text-[var(--color-on-surface)]">
	Materiais indexados
</h2>
<p class="mb-6 text-sm text-[var(--color-outline)]">PDFs e textos disponíveis para consulta pelo tutor.</p>

{#if loading}
	<div role="status" class="alert alert-info text-sm">
		<span class="loading loading-spinner loading-sm"></span>
		<span>Carregando materiais…</span>
	</div>
{:else if error}
	<div role="alert" class="alert alert-error text-sm"><span>{error}</span></div>
{:else if documents.length === 0}
	<div class="flex flex-col items-center gap-3 py-12 text-center">
		<span
			class="flex size-12 items-center justify-center rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
		>
			<FolderOpen size={20} />
		</span>
		<p class="m-0 font-semibold text-[var(--color-on-surface)]">Nenhum material catalogado ainda</p>
		<p class="m-0 max-w-sm text-sm text-[var(--color-outline)]">
			Indexe um PDF ou um texto para vê-lo listado aqui.
		</p>
		<a
			href="/ingest"
			class="btn btn-sm mt-2 rounded-full border-none bg-[var(--color-primary)] text-[var(--color-primary-content)]"
		>
			Indexar materiais
		</a>
	</div>
{:else}
	<ul class="m-0 flex list-none flex-col gap-2 p-0">
		{#each documents as doc (doc.source)}
			<li class="flex items-center justify-between rounded-2xl bg-[var(--color-surface-container)] px-4 py-3 text-sm">
				<span class="truncate">{doc.source}</span>
				<span class="badge badge-ghost">{doc.type === 'pdf' ? 'PDF' : 'Texto'} · {doc.chunks} trechos</span>
			</li>
		{/each}
	</ul>
{/if}

<script lang="ts">
	import { onMount } from 'svelte';
	import { FolderOpen } from '@lucide/svelte';
	import { getDocuments } from '$lib/api/ingest';
	import type { DocumentInfo } from '$lib/api/types';

	let documents = $state<DocumentInfo[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);

	onMount(async () => {
		try {
			documents = (await getDocuments()).documents;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao carregar materiais.';
		} finally {
			loading = false;
		}
	});
</script>
