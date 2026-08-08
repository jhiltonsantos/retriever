<div class="flex flex-col h-full min-h-0 gap-4">
	<header class="flex items-start justify-between gap-4 shrink-0">
		<PageNav class="!mb-0 flex-1" title="Conversa com o tutor" />
		<button
			type="button"
			class="btn btn-ghost btn-sm btn-outline btn-error shrink-0 mt-0.5"
			onclick={() => chatPanel?.clearHistory()}
		>
			Limpar
		</button>
	</header>

	<main class="w-full flex-1 min-h-0 flex flex-col">
		<ChatPanel bind:this={chatPanel} />
	</main>
</div>

<script lang="ts">
	import ChatPanel from '$lib/components/ChatPanel.svelte';
	import PageNav from '$lib/components/PageNav.svelte';

	let chatPanel = $state<ChatPanel | undefined>(undefined);
</script>
