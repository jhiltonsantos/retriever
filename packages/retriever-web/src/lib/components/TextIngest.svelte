<section class="flex flex-col gap-4">
	<header class="flex items-start gap-3">
		<span
			class="flex size-12 shrink-0 items-center justify-center rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
		>
			<FileText size={20} />
		</span>
		<div>
			<h2 class="m-0 text-lg font-semibold text-[var(--color-on-surface)]">Texto</h2>
			<p class="mt-1 text-sm text-[var(--color-outline)]">Cole anotações direto na interface</p>
		</div>
	</header>

	<form class="flex flex-col gap-3" onsubmit={onSubmit}>
		<input
			type="text"
			class="input w-full bg-[var(--color-surface-container-lowest)]"
			placeholder="Título"
			bind:value={title}
			disabled={submitting}
		/>
		<textarea
			class="textarea min-h-64 w-full bg-[var(--color-surface-container-lowest)]"
			placeholder="Cole ou digite o texto aqui..."
			bind:value={text}
			disabled={submitting}
		></textarea>
		<span class="self-end text-xs text-[var(--color-outline)]">{text.length} caracteres</span>
		<button
			type="submit"
			class="btn self-start rounded-full border-none bg-[var(--color-primary)] text-[var(--color-primary-content)]"
			disabled={submitting || !title.trim() || !text.trim()}
		>
			{submitting ? 'Indexando…' : 'Indexar texto'}
		</button>
	</form>

	{#if submitting}
		<div role="status" class="alert alert-info text-sm">
			<span class="loading loading-spinner loading-sm"></span>
			<span>Gerando embeddings — pode levar alguns minutos.</span>
		</div>
	{/if}

	{#if error}
		<div role="alert" class="alert alert-error text-sm">
			<span>{error}</span>
		</div>
	{/if}

	{#if result}
		<div role="status" class="alert alert-success text-sm">
			<div>
				<p class="m-0">{result.message}</p>
				<p class="mt-2 m-0 text-sm opacity-80">
					<strong>{result.source}</strong> · {result.chunks_indexed} trechos indexados
				</p>
			</div>
		</div>
	{/if}
</section>

<script lang="ts">
	import { FileText } from '@lucide/svelte';
	import { ingestText } from '$lib/api/ingest';
	import type { IngestTextResponse } from '$lib/api/types';

	let title = $state('');
	let text = $state('');
	let submitting = $state(false);
	let result = $state<IngestTextResponse | null>(null);
	let error = $state<string | null>(null);

	async function onSubmit(event: SubmitEvent) {
		event.preventDefault();
		if (!title.trim() || !text.trim()) {
			error = 'Preencha o título e o texto.';
			return;
		}

		submitting = true;
		error = null;
		result = null;

		try {
			result = await ingestText(title, text);
			title = '';
			text = '';
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao indexar o texto.';
		} finally {
			submitting = false;
		}
	}
</script>
