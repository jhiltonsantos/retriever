<div class="flex flex-col gap-6">
	<div class="flex gap-2">
		{#each tabs as tab (tab.id)}
			<button
				type="button"
				class="btn btn-sm rounded-full {activeTab === tab.id ? 'btn-primary' : 'btn-ghost'}"
				onclick={() => (activeTab = tab.id)}
			>
				{tab.label}
			</button>
		{/each}
	</div>

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
