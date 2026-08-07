<section class="card bg-base-200 border border-base-300">
	<div class="card-body gap-4">
		<header class="flex items-start gap-3">
			<span class="badge badge-secondary font-mono">Aa</span>
			<div>
				<h2 class="card-title text-lg m-0">Texto</h2>
				<p class="text-sm text-base-content/60 mt-1">Cole anotações direto na interface</p>
			</div>
		</header>

		<form class="flex flex-col gap-3" onsubmit={onSubmit}>
			<input
				type="text"
				class="input input-bordered w-full bg-base-100"
				placeholder="Título"
				bind:value={title}
				disabled={submitting}
			/>
			<textarea
				class="textarea textarea-bordered w-full min-h-64 bg-base-100"
				placeholder="Cole ou digite o texto aqui..."
				bind:value={text}
				disabled={submitting}
			></textarea>
			<span class="text-xs text-base-content/60 self-end">{text.length} caracteres</span>
			<button
				type="submit"
				class="btn btn-primary self-start"
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
					<p class="text-base-content/60 text-sm mt-2 m-0">
						<strong>{result.source}</strong> · {result.chunks_indexed} trechos indexados
					</p>
				</div>
			</div>
		{/if}
	</div>
</section>

<script lang="ts">
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
