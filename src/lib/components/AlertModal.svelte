{#if request}
	<div class="fixed inset-0 z-[60] flex items-center justify-center p-8">
		<div
			class="absolute inset-0 bg-[var(--color-on-surface)]/40 backdrop-blur-sm"
			onclick={() => resolveCurrent(false)}
			aria-hidden="true"
		></div>
		<div
			bind:this={dialogEl}
			role="alertdialog"
			aria-modal="true"
			tabindex="-1"
			class="relative w-full max-w-sm rounded-3xl border border-[var(--color-outline-variant)]/30 bg-[var(--color-surface-container-low)] p-6 shadow-xl"
		>
			{#if request.title}
				<h3 class="m-0 mb-2 text-base font-semibold text-[var(--color-on-surface)]">{request.title}</h3>
			{/if}
			<p class="m-0 text-sm whitespace-pre-line text-[var(--color-on-surface-variant)]">{request.message}</p>
			<div class="mt-5 flex justify-end gap-3">
				{#if request.kind === 'confirm'}
					<button type="button" class="btn btn-ghost rounded-full" onclick={() => resolveCurrent(false)}>
						{request.cancelLabel ?? 'Cancelar'}
					</button>
					<button
						type="button"
						class="btn rounded-full border-none {request.variant === 'error'
							? 'btn-error'
							: 'bg-[var(--color-primary)] text-[var(--color-primary-content)]'}"
						onclick={() => resolveCurrent(true)}
					>
						{request.confirmLabel ?? 'Confirmar'}
					</button>
				{:else}
					<button
						type="button"
						class="btn rounded-full border-none bg-[var(--color-primary)] text-[var(--color-primary-content)]"
						onclick={() => resolveCurrent(true)}
					>
						OK
					</button>
				{/if}
			</div>
		</div>
	</div>
{/if}

<script lang="ts">
	import { onMount } from 'svelte';
	import { getCurrentRequest, resolveCurrent } from '$lib/alerts.svelte';

	let dialogEl: HTMLDivElement | undefined = $state();
	const request = $derived(getCurrentRequest());

	onMount(() => {
		const handler = (e: KeyboardEvent) => {
			if (e.key === 'Escape' && getCurrentRequest()) resolveCurrent(false);
		};
		window.addEventListener('keydown', handler);
		return () => window.removeEventListener('keydown', handler);
	});

	$effect(() => {
		if (request) dialogEl?.focus();
	});
</script>
