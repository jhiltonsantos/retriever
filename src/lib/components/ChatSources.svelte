<div class="collapse-arrow collapse rounded-2xl bg-[var(--color-surface-container)] text-sm">
	<input type="checkbox" />
	<div class="collapse-title">Fontes</div>
	<div class="collapse-content flex flex-col gap-2">
		{#each sources as item}
			<div class="flex flex-col gap-1 border-l-2 border-[var(--color-outline-variant)] pl-2">
				<span class="text-xs font-semibold text-[var(--color-on-surface)]">
					{item.source}{item.page !== null ? ` · p. ${item.page}` : ''}
				</span>
				<p class="m-0 text-xs text-[var(--color-outline)]">{item.snippet}</p>
			</div>
		{/each}
	</div>
</div>

<script lang="ts">
	import type { AskSource } from '$lib/api/types';

	type Props = {
		sources: AskSource[];
	};

	let { sources }: Props = $props();
</script>
