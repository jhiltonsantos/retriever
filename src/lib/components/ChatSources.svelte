<div class="collapse collapse-arrow bg-base-200 text-sm">
	<input type="checkbox" />
	<div class="collapse-title">Fontes</div>
	<div class="collapse-content flex flex-col gap-2">
		{#each sources as item}
			<div class="flex flex-col gap-1 border-l-2 border-base-300 pl-2">
				<span class="font-semibold text-xs text-base-content/90">
					{item.source}{item.page !== null ? ` · p. ${item.page}` : ''}
				</span>
				<p class="text-xs text-base-content/70 m-0">{item.snippet}</p>
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
