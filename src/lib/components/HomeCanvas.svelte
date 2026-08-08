<div class="relative flex h-full flex-col">
	<TopBar />
	<OllamaStatus />
	<div class="flex flex-1 flex-col items-center justify-center gap-12 overflow-y-auto px-16 pb-40">
		<div class="flex flex-col items-center gap-3 text-center">
			<span
				class="flex size-16 items-center justify-center rounded-full bg-gradient-to-br from-[var(--color-primary-container)] to-[var(--color-surface-tint)]"
			>
				<img src={favicon} alt="" class="size-10" />
			</span>
			<h1
				class="m-0 font-['Comfortaa'] text-5xl leading-[56px] font-bold tracking-[-0.02em] text-[var(--color-on-surface)]"
			>
				{greeting}
			</h1>
			<p class="m-0 text-lg text-[var(--color-outline)]">Como posso ajudar com seus materiais hoje?</p>
		</div>

		<div class="flex w-full max-w-[896px] gap-4">
			<ActionCard
				href="/ingest"
				title="Indexar materiais"
				description="Envie um PDF ou cole um texto para consultas futuras."
				icon={Database}
			/>
			<ActionCard
				href="/library"
				title="Visualizar materiais"
				description="Veja os materiais já indexados no seu catálogo."
				icon={Folder}
			/>
			<ActionCard
				href="/history"
				title="Histórico"
				description="Volte a conversas anteriores com o tutor."
				icon={History}
			/>
		</div>
	</div>

	<ChatComposer bind:value={draft} submitting={false} onSubmit={startChatFromHome} />
</div>

<script lang="ts">
	import { goto } from '$app/navigation';
	import { Database, Folder, History } from '@lucide/svelte';
	import favicon from '$lib/assets/favicon.svg';
	import TopBar from './TopBar.svelte';
	import OllamaStatus from './OllamaStatus.svelte';
	import ActionCard from './ActionCard.svelte';
	import ChatComposer from './ChatComposer.svelte';

	let draft = $state('');

	const greeting = (() => {
		const hour = new Date().getHours();
		if (hour < 12) return 'Bom dia!';
		if (hour < 18) return 'Boa tarde!';
		return 'Boa noite!';
	})();

	function startChatFromHome() {
		const question = draft.trim();
		if (!question) return;
		goto(`/chat?q=${encodeURIComponent(question)}`);
	}
</script>
