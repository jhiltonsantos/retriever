<div class="flex h-full min-h-0 flex-col gap-4">
	<div class="flex items-start justify-between gap-4">
		<div>
			<h2 class="m-0 font-['Comfortaa'] text-2xl font-semibold text-[var(--color-on-surface)]">
				Materiais indexados
			</h2>
			<p class="m-0 text-sm text-[var(--color-outline)]">PDFs e textos disponíveis para consulta pelo tutor.</p>
		</div>
		<div class="join shrink-0 gap-1 pr-10 pt-1">
			<button
				type="button"
				class="btn btn-sm join-item {view === 'list' ? 'btn-primary' : 'btn-soft'}"
				onclick={() => (view = 'list')}
			>
				Lista
			</button>
			<button
				type="button"
				class="btn btn-sm join-item {view === 'graph' ? 'btn-primary' : 'btn-soft'}"
				onclick={() => (view = 'graph')}
			>
				Grafo
			</button>
		</div>
	</div>

	{#if view === 'list'}
		{#if loading}
			<div role="status" class="alert alert-info text-sm">
				<span class="loading loading-spinner loading-sm"></span>
				<span>Carregando materiais…</span>
			</div>
		{:else if error}
			<div role="alert" class="alert alert-error text-sm"><span>{error}</span></div>
		{:else if materials.length === 0}
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
				{#each materials as material (material.id)}
					<li class="group flex items-center justify-between rounded-2xl bg-[var(--color-surface-container)] px-4 py-3 text-sm">
						<div class="flex min-w-0 flex-col gap-0.5">
							<span class="truncate font-medium text-[var(--color-on-surface)]">{material.title ?? material.source}</span>
							<span class="truncate text-xs text-[var(--color-outline)]">{material.source}</span>
						</div>
						<div class="flex shrink-0 items-center gap-2">
							<span class="badge badge-ghost">{material.type === 'pdf' ? 'PDF' : 'Texto'} · {material.chunk_count} trechos</span>
							<button
								type="button"
								class="btn btn-ghost btn-circle btn-xs opacity-0 group-hover:opacity-100"
								aria-label="Excluir material"
								onclick={() => onDelete(material.id)}
							>
								<Trash2 size={16} class="text-error" />
							</button>
						</div>
					</li>
				{/each}
			</ul>
		{/if}
	{:else}
		<div class="min-h-0 flex-1">
			<MaterialsGraph />
		</div>
	{/if}
</div>

<script lang="ts">
	import { onMount } from 'svelte';
	import { FolderOpen, Trash2 } from '@lucide/svelte';
	import { listMaterials, deleteMaterial } from '$lib/api/materials';
	import type { MaterialInfo } from '$lib/api/types';
	import { showConfirm } from '$lib/alerts.svelte';
	import MaterialsGraph from '$lib/components/MaterialsGraph.svelte';

	let materials = $state<MaterialInfo[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let view = $state<'list' | 'graph'>('list');

	onMount(async () => {
		await loadMaterials();
	});

	async function loadMaterials() {
		loading = true;
		error = null;
		try {
			const response = await listMaterials();
			materials = response.materials;
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao carregar materiais.';
		} finally {
			loading = false;
		}
	}

	async function onDelete(id: string) {
		if (
			!(await showConfirm('Excluir este material permanentemente?', {
				confirmLabel: 'Excluir',
				variant: 'error'
			}))
		) {
			return;
		}

		try {
			await deleteMaterial(id);
			await loadMaterials();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao excluir material.';
		}
	}
</script>
