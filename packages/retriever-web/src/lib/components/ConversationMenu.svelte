<div
	bind:this={menuEl}
	class="fixed z-[70] flex w-40 flex-col overflow-hidden rounded-2xl border border-[var(--color-outline-variant)]/40 bg-[var(--color-surface-container-low)] py-1 shadow-[0px_8px_24px_rgba(0,0,0,0.18)]"
	style="left: {x}px; top: {y}px;"
	role="menu"
>
	<button
		type="button"
		class="px-4 py-2 text-left text-sm text-[var(--color-on-surface)] hover:bg-[var(--color-surface-container-high)]"
		role="menuitem"
		onclick={onRename}
	>
		Renomear
	</button>
	<button
		type="button"
		class="px-4 py-2 text-left text-sm text-error hover:bg-[var(--color-surface-container-high)]"
		role="menuitem"
		onclick={onDelete}
	>
		Excluir
	</button>
</div>

<script lang="ts">
	import { onMount } from 'svelte';

	type Props = {
		x: number;
		y: number;
		onRename: () => void;
		onDelete: () => void;
		onClose: () => void;
	};

	let { x, y, onRename, onDelete, onClose }: Props = $props();
	let menuEl = $state<HTMLDivElement | null>(null);

	onMount(() => {
		function onPointerDown(event: PointerEvent) {
			if (menuEl && !menuEl.contains(event.target as Node)) onClose();
		}
		function onKeydown(event: KeyboardEvent) {
			if (event.key === 'Escape') onClose();
		}
		window.addEventListener('pointerdown', onPointerDown, true);
		window.addEventListener('keydown', onKeydown);
		return () => {
			window.removeEventListener('pointerdown', onPointerDown, true);
			window.removeEventListener('keydown', onKeydown);
		};
	});
</script>
