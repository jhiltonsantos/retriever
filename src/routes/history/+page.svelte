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
			<li
				class="group flex items-center justify-between rounded-2xl bg-[var(--color-surface-container)] px-4 py-3 text-sm hover:bg-[var(--color-surface-container-high)]"
				oncontextmenu={(e) => onContextMenu(e, conv.id)}
				onpointerdown={(e) => onPointerDownConv(e, conv.id)}
				onpointerup={onPointerUpConv}
				onpointermove={onPointerMoveConv}
			>
				{#if renamingId === conv.id}
					<input
						class="input input-sm flex-1 rounded-full bg-[var(--color-surface-container-lowest)] px-4 text-sm"
						bind:value={renameValue}
						onkeydown={(e) => {
							if (e.key === 'Enter') commitRename(conv.id);
							if (e.key === 'Escape') cancelRename();
						}}
						onblur={() => commitRename(conv.id)}
						use:autofocus
					/>
				{:else}
					<a href="/chat?conv={conv.id}" class="flex flex-1 items-center justify-between no-underline">
						<span class="truncate text-[var(--color-on-surface)]">{conv.title}</span>
						<span class="text-xs text-[var(--color-outline)] whitespace-nowrap">{conv.message_count} mensagens</span>
					</a>
					<button
						type="button"
						class="btn btn-ghost btn-circle btn-xs ml-2 opacity-0 group-hover:opacity-100"
						aria-label="Excluir conversa"
						onclick={(event) => onDeleteFromButton(conv.id, event)}
					>
						<Trash2 size={16} class="text-error" />
					</button>
				{/if}
			</li>
		{/each}
	</ul>
{/if}

{#if menuState}
	<ConversationMenu
		x={menuState.x}
		y={menuState.y}
		onRename={() =>
			startRename(menuState!.id, conversations.find((c) => c.id === menuState!.id)?.title ?? '')}
		onDelete={() => performDelete(menuState!.id)}
		onClose={closeMenu}
	/>
{/if}

<script lang="ts">
	import { onMount } from 'svelte';
	import { Search, Trash2 } from '@lucide/svelte';
	import { getAllConversations, loadConversations } from '$lib/chat/conversations.svelte';
	import { deleteConversation, updateConversationTitle } from '$lib/api/conversations';
	import { showConfirm } from '$lib/alerts.svelte';
	import ConversationMenu from '$lib/components/ConversationMenu.svelte';

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

	let menuState = $state<{ id: string; x: number; y: number } | null>(null);
	let renamingId = $state<string | null>(null);
	let renameValue = $state('');
	let longPressTimer: ReturnType<typeof setTimeout> | null = null;

	function autofocus(node: HTMLInputElement) {
		node.focus();
		node.select();
	}

	function clampX(x: number) {
		return Math.min(x, window.innerWidth - 170);
	}
	function clampY(y: number) {
		return Math.min(y, window.innerHeight - 90);
	}
	function openMenu(id: string, x: number, y: number) {
		menuState = { id, x: clampX(x), y: clampY(y) };
	}
	function closeMenu() {
		menuState = null;
	}

	function onContextMenu(event: MouseEvent, id: string) {
		event.preventDefault();
		openMenu(id, event.clientX, event.clientY);
	}
	function onPointerDownConv(event: PointerEvent, id: string) {
		if (event.pointerType !== 'touch') return;
		longPressTimer = setTimeout(() => openMenu(id, event.clientX, event.clientY), 500);
	}
	function onPointerUpConv() {
		if (longPressTimer) {
			clearTimeout(longPressTimer);
			longPressTimer = null;
		}
	}
	function onPointerMoveConv() {
		if (longPressTimer) {
			clearTimeout(longPressTimer);
			longPressTimer = null;
		}
	}

	function startRename(id: string, currentTitle: string) {
		renamingId = id;
		renameValue = currentTitle;
		closeMenu();
	}
	async function commitRename(id: string) {
		const title = renameValue.trim();
		renamingId = null;
		if (!title) return;
		try {
			await updateConversationTitle(id, title);
			await loadConversations();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao renomear conversa.';
		}
	}
	function cancelRename() {
		renamingId = null;
	}

	onMount(async () => {
		try {
			await loadConversations();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao carregar conversas.';
		} finally {
			loading = false;
		}
	});

	async function performDelete(id: string) {
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

	function onDeleteFromButton(id: string, event: MouseEvent) {
		event.preventDefault();
		event.stopPropagation();
		performDelete(id);
	}
</script>
