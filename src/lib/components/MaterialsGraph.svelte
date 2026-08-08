<div class="flex h-full min-h-0 flex-col gap-3">
	<label
		class="input input-bordered flex w-full items-center gap-2 rounded-full bg-[var(--color-surface-container-lowest)]"
	>
		<Search size={18} class="text-[var(--color-outline)]" />
		<input
			type="text"
			class="grow bg-transparent outline-none"
			placeholder="Buscar material…"
			bind:value={query}
			oninput={() => (focusId = null)}
		/>
		{#if query || focusId}
			<button type="button" class="btn btn-ghost btn-circle btn-xs" aria-label="Limpar busca" onclick={clearFilter}>
				<X size={14} />
			</button>
		{/if}
	</label>

	<div class="relative min-h-0 flex-1 overflow-hidden rounded-2xl bg-[var(--color-surface-container-lowest)]">
		<div bind:this={containerEl} class="h-full w-full"></div>
		{#if loading}
			<div class="absolute inset-0 flex items-center justify-center">
				<span class="loading loading-spinner loading-md"></span>
			</div>
		{:else if error}
			<div class="absolute inset-0 flex items-center justify-center px-6 text-center text-sm text-[var(--color-outline)]">
				{error}
			</div>
		{/if}
	</div>
</div>

<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { Search, X } from '@lucide/svelte';
	import { getMaterialsGraph } from '$lib/api/materials';
	import type { GraphEdge, MaterialGraphNode } from '$lib/api/types';

	let containerEl = $state<HTMLDivElement | null>(null);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let query = $state('');
	let focusId = $state<string | null>(null);

	let nodes = $state<MaterialGraphNode[]>([]);
	let edges = $state<GraphEdge[]>([]);

	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	let graphInstance: any = null;
	let resizeObserver: ResizeObserver | null = null;
	let colors = { primary: '', accent: '', outline: '' };

	function resolveColor(name: string): string {
		return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
	}

	function nodeColor(node: MaterialGraphNode): string {
		return node.type === 'pdf' ? colors.primary : colors.accent;
	}

	function nodeVal(node: MaterialGraphNode): number {
		// force-graph usa raio = sqrt(val) * nodeRelSize -- materiais tem centenas
		// de chunks, entao o valor bruto (ate ~900) rendeu um circulo cobrindo o
		// canvas inteiro. Log comprime isso pra uma faixa de raio razoavel.
		return 1 + Math.log10(node.chunk_count + 1);
	}

	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	function linkEndpointId(endpoint: string | { id: string }): string {
		return typeof endpoint === 'object' ? endpoint.id : endpoint;
	}

	function clearFilter() {
		query = '';
		focusId = null;
	}

	// Quais materiais devem ficar visiveis: null = mostra tudo. Com busca ou
	// clique num no, mostra so o(s) selecionado(s) e seus vizinhos fortes
	// (mesmo criterio de KNN mutuo usado para desenhar as linhas).
	const visibleIds = $derived.by((): Set<string> | null => {
		let base: Set<string> | null = null;
		if (focusId) {
			base = new Set([focusId]);
		} else if (query.trim()) {
			const q = query.trim().toLowerCase();
			base = new Set(nodes.filter((n) => n.label.toLowerCase().includes(q)).map((n) => n.id));
		}
		if (base === null) return null;

		const expanded = new Set(base);
		for (const edge of edges) {
			if (!edge.strong) continue;
			if (base.has(edge.source)) expanded.add(edge.target);
			if (base.has(edge.target)) expanded.add(edge.source);
		}
		return expanded;
	});

	$effect(() => {
		const visible = visibleIds;
		graphInstance
			?.nodeVisibility((node: MaterialGraphNode) => visible === null || visible.has(node.id))
			.linkVisibility((link: GraphEdge) => {
				if (!link.strong) return false;
				if (visible === null) return true;
				const source = linkEndpointId(link.source as never);
				const target = linkEndpointId(link.target as never);
				return visible.has(source) && visible.has(target);
			});
	});

	async function loadGraph() {
		loading = true;
		error = null;
		try {
			const data = await getMaterialsGraph();
			nodes = data.nodes;
			edges = data.edges;
			// copias rasas: o force-graph muta os objetos de link (troca source/target
			// por referencia de no) -- passar copias mantem `edges` intacto pro filtro.
			graphInstance
				?.graphData({ nodes: data.nodes.map((n) => ({ ...n })), links: data.edges.map((e) => ({ ...e })) })
				.nodeColor(nodeColor)
				.nodeVal(nodeVal);
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao carregar grafo.';
		} finally {
			loading = false;
		}
	}

	onMount(async () => {
		colors = {
			primary: resolveColor('--color-primary'),
			accent: resolveColor('--color-accent'),
			outline: resolveColor('--color-outline')
		};

		const { default: ForceGraph } = await import('force-graph');
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		graphInstance = new ForceGraph(containerEl!) as any;
		graphInstance
			.nodeId('id')
			.nodeLabel((node: MaterialGraphNode) => `${node.label} (${node.chunk_count})`)
			.nodeVisibility(() => true)
			.linkVisibility((link: GraphEdge) => link.strong)
			.linkWidth((link: GraphEdge) => Math.max(1, link.weight * 4))
			.linkColor(() => colors.outline)
			.onNodeClick((node: MaterialGraphNode) => {
				focusId = focusId === node.id ? null : node.id;
				query = '';
			})
			.onBackgroundClick(clearFilter)
			.width(containerEl!.clientWidth)
			.height(containerEl!.clientHeight);

		// Materiais mais similares ficam visualmente mais perto, mesmo sem linha
		// desenhada entre eles -- reflete a proximidade real, nao so as ligacoes
		// fortes marcadas com `strong`.
		graphInstance
			.d3Force('link')
			?.distance((link: GraphEdge) => 40 + (1 - link.weight) * 260);

		resizeObserver = new ResizeObserver(() => {
			graphInstance?.width(containerEl!.clientWidth).height(containerEl!.clientHeight);
		});
		resizeObserver.observe(containerEl!);

		await loadGraph();
	});

	onDestroy(() => {
		resizeObserver?.disconnect();
		graphInstance?._destructor?.();
	});
</script>
