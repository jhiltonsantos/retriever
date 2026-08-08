<div class="w-full max-w-[720px] mx-auto flex-1 min-h-0 flex flex-col">
	{@render children()}
</div>

<script lang="ts">
	import type { LayoutProps } from './$types';

	let { children }: LayoutProps = $props();
</script>
