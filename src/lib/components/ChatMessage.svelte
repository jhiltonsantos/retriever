<div
	class="chat {message.role === 'user' ? 'chat-end' : 'chat-start'}"
	aria-label="{label}: {message.content}"
>
	<div class="chat-header text-xs opacity-70">
		{label}
		<time class="text-xs" datetime={message.createdAt}>{time}</time>
	</div>
	<div
		class="chat-bubble whitespace-pre-wrap leading-relaxed {message.role === 'user'
			? 'chat-bubble-primary'
			: 'chat-bubble-neutral'}"
	>
		{message.content}
	</div>
	{#if message.sources?.length || message.agentSteps?.length}
		<div class="chat-footer flex flex-col gap-2 mt-1 w-full max-w-md">
			{#if message.sources?.length}
				<ChatSources sources={message.sources} />
			{/if}
			{#if message.agentSteps?.length}
				<AgentSteps steps={message.agentSteps} />
			{/if}
		</div>
	{/if}
</div>

<script lang="ts">
	import type { ChatMessage as ChatMessageType } from '$lib/chat/types';
	import AgentSteps from './AgentSteps.svelte';
	import ChatSources from './ChatSources.svelte';

	type Props = {
		message: ChatMessageType;
	};

	let { message }: Props = $props();

	const label = $derived(message.role === 'user' ? 'Você' : 'Tutor');
	const time = $derived(
		new Date(message.createdAt).toLocaleTimeString('pt-BR', {
			hour: '2-digit',
			minute: '2-digit'
		})
	);
</script>
