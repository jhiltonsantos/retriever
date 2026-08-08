<a
	class="flex flex-1 flex-col justify-between gap-6 self-stretch rounded-[3rem] border border-[var(--color-outline-variant)]/30 bg-[var(--color-surface-container-low)] p-8 text-inherit no-underline shadow-[0_4px_24px_rgba(0,0,0,0.05)] transition-transform hover:-translate-y-1"
	{href}
>
	<span
		class="flex size-12 items-center justify-center rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
	>
		<Icon size={20} />
	</span>
	<div class="flex flex-col gap-3">
		<h2 class="m-0 font-['Comfortaa'] text-2xl font-semibold text-[var(--color-on-surface)]">
			{title}
		</h2>
		<p class="m-0 text-sm leading-relaxed text-[var(--color-outline)]">{description}</p>
	</div>
</a>

<script lang="ts">
	import type { Component } from 'svelte';

	type Props = {
		href: string;
		title: string;
		description: string;
		icon: Component<{ size?: number | string }>;
	};

	let { href, title, description, icon: Icon }: Props = $props();
</script>
