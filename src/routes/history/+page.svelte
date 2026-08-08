<h2 class="m-0 font-['Comfortaa'] text-2xl font-semibold text-[var(--color-on-surface)]">
	Histórico de conversas
</h2>
<p class="mb-6 text-sm text-[var(--color-outline)]">Suas conversas anteriores com o tutor.</p>

{#if conversations.length === 0}
	<p class="py-8 text-center text-sm text-[var(--color-outline)]">
		Nenhuma conversa ainda. Comece uma pelo botão "Novo Chat".
	</p>
{:else}
	<ul class="m-0 flex list-none flex-col gap-2 p-0">
		{#each conversations as conv (conv.id)}
			<li>
				<a
					href="/chat"
					class="flex items-center justify-between rounded-2xl bg-[var(--color-surface-container)] px-4 py-3 text-sm no-underline hover:bg-[var(--color-surface-container-high)]"
				>
					<span class="truncate">{conv.title}</span>
					<span class="text-xs text-[var(--color-outline)]">{conv.messageCount} mensagens</span>
				</a>
			</li>
		{/each}
	</ul>
{/if}

<script lang="ts">
	import { listRecentConversations } from '$lib/chat/conversations';

	const conversations = listRecentConversations();
</script>
