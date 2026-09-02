<div class="flex h-full flex-col">
	<TopBar />
	<OllamaStatus />
	<div class="flex shrink-0 items-center justify-end px-16 pb-2">
		<button
			type="button"
			class="btn btn-ghost btn-outline btn-error btn-sm rounded-full"
			onclick={() => chatPanel?.clearHistory()}
		>
			Limpar
		</button>
	</div>
	<ChatPanel
		bind:this={chatPanel}
		{initialQuestion}
		conversationId={currentConversationId}
		onConversationCreated={onConversationCreated}
	/>
</div>

<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import TopBar from './TopBar.svelte';
	import OllamaStatus from './OllamaStatus.svelte';
	import ChatPanel from './ChatPanel.svelte';
	import { loadConversations } from '$lib/chat/conversations.svelte';

	let chatPanel = $state<ChatPanel | undefined>(undefined);
	const initialQuestion = $derived(page.url.searchParams.get('q') ?? undefined);
	const currentConversationId = $derived(page.url.searchParams.get('conv') ?? undefined);

	function onConversationCreated(id: string) {
		const url = new URL(page.url);
		url.searchParams.set('conv', id);
		goto(url.toString(), { replaceState: true });
		loadConversations();
	}
</script>
