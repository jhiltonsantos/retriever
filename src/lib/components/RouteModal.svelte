<div class="fixed inset-0 z-50 flex items-center justify-center p-8">
	<div
		class="absolute inset-0 bg-[var(--color-on-surface)]/40 backdrop-blur-sm"
		onclick={onClose}
		aria-hidden="true"
	></div>
	<div
		bind:this={dialogEl}
		role="dialog"
		aria-modal="true"
		tabindex="-1"
		class="relative z-10 max-h-[85vh] w-full overflow-y-auto rounded-[3rem] border border-[var(--color-outline-variant)]/40 bg-[var(--color-surface-container-low)] p-10 shadow-[0px_20px_60px_rgba(0,0,0,0.15)] {size ===
		'lg'
			? 'max-w-4xl'
			: 'max-w-2xl'}"
	>
		<button
			type="button"
			class="btn btn-ghost btn-circle absolute top-6 right-6"
			onclick={onClose}
			aria-label="Fechar"
		>
			<X size={20} />
		</button>
		{@render children()}
	</div>
</div>

<script lang="ts">
	import { onMount } from 'svelte';
	import type { Snippet } from 'svelte';
	import { X } from '@lucide/svelte';

	type Props = {
		onClose: () => void;
		size?: 'md' | 'lg';
		children: Snippet;
	};

	let { onClose, size = 'md', children }: Props = $props();
	let dialogEl = $state<HTMLDivElement | null>(null);

	onMount(() => {
		dialogEl?.focus();

		function onKeydown(event: KeyboardEvent) {
			if (event.key === 'Escape') {
				onClose();
			}
		}

		window.addEventListener('keydown', onKeydown);
		return () => window.removeEventListener('keydown', onKeydown);
	});
</script>
