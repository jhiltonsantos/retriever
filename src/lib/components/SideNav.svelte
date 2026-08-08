<aside
	class="m-5 flex h-[calc(100vh-2.5rem)] w-[265px] shrink-0 flex-col gap-8 overflow-y-auto rounded-[1.25rem] border border-[var(--color-outline-variant)]/30 bg-[var(--color-surface-container-low)] p-4"
>
	<div class="flex h-14 items-center gap-2">
		<img src={favicon} alt="" class="size-10" />
		<span class="font-['Comfortaa'] text-2xl font-bold text-[var(--color-primary)]">Retriever</span>
	</div>

	<button
		type="button"
		class="btn w-full rounded-full border-none bg-[var(--color-primary)] text-[var(--color-primary-content)]"
		onclick={onNewChat}
	>
		<Plus size={18} /> Novo Chat
	</button>

	<nav class="flex flex-1 flex-col gap-1 overflow-y-auto">
		{#each mainItems as item (item.href)}
			<a
				href={item.href}
				class="flex h-11 items-center gap-3 rounded-r-full border-l-4 pl-5 pr-4 text-sm font-semibold no-underline {isActive(
					item.href
				)
					? 'border-l-[var(--color-primary)] bg-[var(--color-primary-container)]/10 text-[var(--color-primary)]'
					: 'border-l-transparent text-[var(--color-on-surface-variant)] hover:bg-[var(--color-surface-container)]'}"
			>
				<item.icon size={18} />
				{item.label}
			</a>
		{/each}

		<div class="mt-4 flex flex-col gap-1">
			<p class="px-5 text-xs tracking-wide text-[var(--color-outline)] uppercase">Recentes</p>
			{#if recentConversations.length === 0}
				<p class="px-5 text-xs text-[var(--color-outline)]">Nenhuma conversa ainda</p>
			{:else}
				{#each recentConversations as conv (conv.id)}
					{#if renamingId === conv.id}
						<input
							class="input input-sm mx-1 rounded-full bg-[var(--color-surface-container)] px-4 text-sm"
							bind:value={renameValue}
							onkeydown={(e) => {
								if (e.key === 'Enter') commitRename(conv.id);
								if (e.key === 'Escape') cancelRename();
							}}
							onblur={() => commitRename(conv.id)}
							use:autofocus
						/>
					{:else}
						<a
							href="/chat?conv={conv.id}"
							class="truncate rounded-r-full px-5 py-2 text-sm text-[var(--color-on-surface-variant)] no-underline hover:bg-[var(--color-surface-container)]"
							oncontextmenu={(e) => onContextMenu(e, conv.id)}
							onpointerdown={(e) => onPointerDownConv(e, conv.id)}
							onpointerup={onPointerUpConv}
							onpointermove={onPointerMoveConv}
						>
							{conv.title}
						</a>
					{/if}
				{/each}
			{/if}
		</div>
	</nav>

	<div class="flex flex-col gap-1 border-t border-[var(--color-outline-variant)]/30 pt-4">
		{#each bottomItems as item (item.href)}
			<a
				href={item.href}
				class="flex h-11 items-center gap-3 rounded-r-full border-l-4 pl-5 pr-4 text-sm no-underline {isActive(
					item.href
				)
					? 'border-l-[var(--color-primary)] bg-[var(--color-primary-container)]/10 text-[var(--color-primary)]'
					: 'border-l-transparent text-[var(--color-on-surface-variant)] hover:bg-[var(--color-surface-container)]'}"
			>
				<item.icon size={18} />
				{item.label}
			</a>
		{/each}
	</div>
</aside>

{#if menuState}
	<ConversationMenu
		x={menuState.x}
		y={menuState.y}
		onRename={() =>
			startRename(menuState!.id, recentConversations.find((c) => c.id === menuState!.id)?.title ?? '')}
		onDelete={() => onDeleteConv(menuState!.id)}
		onClose={closeMenu}
	/>
{/if}

<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { Database, Folder, History, Settings, CircleHelp, Plus } from '@lucide/svelte';
	import favicon from '$lib/assets/favicon.svg';
	import { listRecentConversations, loadConversations } from '$lib/chat/conversations.svelte';
	import ConversationMenu from '$lib/components/ConversationMenu.svelte';
	import { updateConversationTitle, deleteConversation } from '$lib/api/conversations';
	import { showAlert, showConfirm } from '$lib/alerts.svelte';

	const mainItems = [
		{ href: '/ingest', label: 'Indexar materiais', icon: Database },
		{ href: '/library', label: 'Visualizar materiais', icon: Folder },
		{ href: '/history', label: 'Histórico', icon: History }
	];

	const bottomItems = [
		{ href: '/settings', label: 'Configurações', icon: Settings },
		{ href: '/info', label: 'Info', icon: CircleHelp }
	];

	const recentConversations = $derived(listRecentConversations());

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
			showAlert(err instanceof Error ? err.message : 'Erro ao renomear conversa.');
		}
	}
	function cancelRename() {
		renamingId = null;
	}

	async function onDeleteConv(id: string) {
		closeMenu();
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
			showAlert(err instanceof Error ? err.message : 'Erro ao excluir conversa.');
		}
	}

	onMount(() => {
		loadConversations();
	});

	function isActive(href: string): boolean {
		return page.url.pathname.startsWith(href);
	}

	function onNewChat() {
		goto('/chat');
	}
</script>
