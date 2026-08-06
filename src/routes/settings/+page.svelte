<PageNav title="Configurações" />

<main class="w-full max-w-lg mx-auto flex flex-col gap-5">
	<LlmSettingsCard />
	<EmbeddingsInfoPanel />
</main>

<script lang="ts">
	import PageNav from '$lib/components/PageNav.svelte';
	import LlmSettingsCard from '$lib/components/LlmSettingsCard.svelte';
	import EmbeddingsInfoPanel from '$lib/components/EmbeddingsInfoPanel.svelte';
</script>
