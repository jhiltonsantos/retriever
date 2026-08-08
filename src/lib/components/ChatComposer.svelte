<div
	class="pointer-events-none absolute inset-x-0 bottom-0 z-10 flex shrink-0 justify-center bg-gradient-to-t from-[var(--color-base-100)] via-[var(--color-base-100)]/80 to-transparent px-16 pt-16 pb-8"
>
	<div class="pointer-events-auto flex w-full max-w-[896px] flex-col gap-2">
		<form
			class="flex w-full items-center gap-2 rounded-full border border-[var(--color-outline-variant)]/40 bg-[var(--color-surface-container-lowest)]/80 p-2 shadow-[0_12px_32px_rgba(0,0,0,0.12)] backdrop-blur-md"
			onsubmit={handleSubmit}
		>
			<a
				href="/ingest"
				class="btn btn-circle btn-ghost size-12 shrink-0"
				aria-label="Indexar materiais"
			>
				<Paperclip size={18} />
			</a>
			<textarea
				class="max-h-32 min-h-0 flex-1 resize-none border-none bg-transparent px-4 py-3 text-sm text-[var(--color-on-surface)] placeholder:text-[var(--color-outline)] focus:outline-none"
				bind:value
				onkeydown={onKeydown}
				placeholder="Escreva sua mensagem aqui..."
				rows="1"
				disabled={submitting}
				required
			></textarea>
			<button
				type="submit"
				class="btn btn-circle size-12 shrink-0 border-none bg-[var(--color-primary)] text-[var(--color-primary-content)]"
				disabled={submitting || !value.trim()}
				aria-label="Enviar"
			>
				{#if submitting}
					<span class="loading loading-spinner loading-sm"></span>
				{:else}
					<ArrowUp size={18} />
				{/if}
			</button>
		</form>
		<p class="text-center text-xs text-[var(--color-outline)]">
			A IA pode cometer erros. Verifique informações importantes.
		</p>
	</div>
</div>

<script lang="ts">
	import { ArrowUp, Paperclip } from '@lucide/svelte';

	type Props = {
		value: string;
		submitting: boolean;
		onSubmit: () => void;
	};

	let { value = $bindable(''), submitting, onSubmit }: Props = $props();

	function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		if (!value.trim() || submitting) return;
		onSubmit();
	}

	function onKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			if (!value.trim() || submitting) return;
			onSubmit();
		}
	}
</script>
