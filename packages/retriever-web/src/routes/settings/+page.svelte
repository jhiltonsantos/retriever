<div class="flex flex-row gap-8 pt-6">
	<nav class="flex w-40 shrink-0 flex-col gap-2">
		{#each tabs as tab (tab.id)}
			<button
				type="button"
				class="flex h-11 items-center rounded-r-full border-l-4 pl-5 pr-4 text-left text-sm font-semibold {activeTab ===
				tab.id
					? 'border-l-[var(--color-primary)] bg-[var(--color-primary-container)]/10 text-[var(--color-primary)]'
					: 'border-l-transparent text-[var(--color-on-surface-variant)] hover:bg-[var(--color-surface-container)]'}"
				onclick={() => (activeTab = tab.id)}
			>
				{tab.label}
			</button>
		{/each}
	</nav>

	<div class="flex min-w-0 flex-1 flex-col gap-8">
		{#if activeTab === 'providers'}
			<LlmSettingsCard />
			<div class="h-px bg-[var(--color-outline-variant)]/30"></div>
			<EmbeddingsInfoPanel />
		{:else if activeTab === 'profile'}
			<ProfileCard />
		{:else if activeTab === 'about'}
			<AboutCard />
		{/if}
	</div>
</div>

<script lang="ts">
	import LlmSettingsCard from '$lib/components/LlmSettingsCard.svelte';
	import EmbeddingsInfoPanel from '$lib/components/EmbeddingsInfoPanel.svelte';
	import ProfileCard from '$lib/components/ProfileCard.svelte';
	import AboutCard from '$lib/components/AboutCard.svelte';

	type TabId = 'providers' | 'profile' | 'about';

	const tabs: { id: TabId; label: string }[] = [
		{ id: 'providers', label: 'Provedores' },
		{ id: 'profile', label: 'Perfil' },
		{ id: 'about', label: 'Sobre' }
	];

	let activeTab = $state<TabId>('providers');
</script>
