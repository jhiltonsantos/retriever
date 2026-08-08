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
	<ChatPanel bind:this={chatPanel} {initialQuestion} />
</div>

<script lang="ts">
	import { page } from '$app/state';
	import TopBar from './TopBar.svelte';
	import OllamaStatus from './OllamaStatus.svelte';
	import ChatPanel from './ChatPanel.svelte';

	let chatPanel = $state<ChatPanel | undefined>(undefined);
	const initialQuestion = $derived(page.url.searchParams.get('q') ?? undefined);
</script>
