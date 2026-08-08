<div class="collapse-arrow collapse rounded-2xl bg-[var(--color-surface-container)] text-sm">
	<input type="checkbox" />
	<div class="collapse-title">Passos do agente</div>
	<div class="collapse-content flex flex-col gap-2">
		{#each steps as item}
			<p class="m-0 text-xs text-[var(--color-outline)]">
				<span class="badge badge-ghost font-mono">loop {item.loop}</span>
				<strong>{item.step}</strong> — {item.detail}
			</p>
		{/each}
	</div>
</div>

<script lang="ts">
	import type { AskAgentStep } from '$lib/api/types';

	type Props = {
		steps: AskAgentStep[];
	};

	let { steps }: Props = $props();
</script>
