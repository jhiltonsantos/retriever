<h2 class="m-0 font-['Comfortaa'] text-2xl font-semibold text-[var(--color-on-surface)]">
	Histórico de conversas
</h2>
<p class="mb-6 text-sm text-[var(--color-outline)]">Suas conversas anteriores com o tutor.</p>

<label class="input input-bordered mb-4 flex w-full items-center gap-2 rounded-full bg-[var(--color-surface-container-lowest)]">
	<Search size={18} class="text-[var(--color-outline)]" />
	<input
		type="text"
		class="grow bg-transparent outline-none"
		placeholder="Buscar conversas…"
		bind:value={query}
	/>
</label>

{#if loading}
	<div role="status" class="alert alert-info text-sm">
		<span class="loading loading-spinner loading-sm"></span>
		<span>Carregando conversas…</span>
	</div>
{:else if error}
	<div role="alert" class="alert alert-error text-sm"><span>{error}</span></div>
{:else if filteredConversations.length === 0}
	<p class="py-8 text-center text-sm text-[var(--color-outline)]">
		{query ? 'Nenhuma conversa encontrada.' : 'Nenhuma conversa ainda. Comece uma pelo botão "Novo Chat".'}
	</p>
{:else}
	<ul class="m-0 flex list-none flex-col gap-2 p-0">
		{#each filteredConversations as conv (conv.id)}
			<li class="group flex items-center justify-between rounded-2xl bg-[var(--color-surface-container)] px-4 py-3 text-sm hover:bg-[var(--color-surface-container-high)]">
				<a
					href="/chat?conv={conv.id}"
					class="flex flex-1 items-center justify-between no-underline"
				>
					<span class="truncate text-[var(--color-on-surface)]">{conv.title}</span>
					<span class="text-xs text-[var(--color-outline)] whitespace-nowrap">{conv.message_count} mensagens</span>
				</a>
				<button
					type="button"
					class="btn btn-ghost btn-circle btn-xs ml-2 opacity-0 group-hover:opacity-100"
					aria-label="Excluir conversa"
					onclick={(event) => onDelete(conv.id, event)}
				>
					<Trash2 size={16} class="text-error" />
				</button>
			</li>
		{/each}
	</ul>
{/if}

<script lang="ts">
	import { onMount } from 'svelte';
	import { Search, Trash2 } from '@lucide/svelte';
	import { getAllConversations, loadConversations } from '$lib/chat/conversations';
	import { deleteConversation } from '$lib/api/conversations';
	import { showConfirm } from '$lib/alerts.svelte';

	let query = $state('');
	let loading = $state(true);
	let error = $state<string | null>(null);

	const conversations = $derived(getAllConversations());
	const filteredConversations = $derived(
		query.trim()
			? conversations.filter((conv) =>
					conv.title.toLowerCase().includes(query.trim().toLowerCase())
				)
			: conversations
	);

	onMount(async () => {
		try {
			await loadConversations();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao carregar conversas.';
		} finally {
			loading = false;
		}
	});

	async function onDelete(id: string, event: MouseEvent) {
		event.preventDefault();
		event.stopPropagation();

		if (
			!(await showConfirm('Excluir esta conversa permanentemente?', {
				confirmLabel: 'Excluir',
				variant: 'error'
			}))
		) {
			return;
		}

		try {
			await deleteConversation(id);
			await loadConversations();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao excluir conversa.';
		}
	}
</script>
