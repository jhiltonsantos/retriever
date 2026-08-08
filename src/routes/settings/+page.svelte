<div class="flex flex-col gap-8">
	<LlmSettingsCard />
	<div class="h-px bg-[var(--color-outline-variant)]/30"></div>
	<EmbeddingsInfoPanel />
</div>

<script lang="ts">
	import LlmSettingsCard from '$lib/components/LlmSettingsCard.svelte';
	import EmbeddingsInfoPanel from '$lib/components/EmbeddingsInfoPanel.svelte';
</script>
