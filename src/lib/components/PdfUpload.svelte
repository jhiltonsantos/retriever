<section class="flex flex-col gap-4">
	<header class="flex items-start gap-3">
		<span
			class="flex size-12 shrink-0 items-center justify-center rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
		>
			<Database size={20} />
		</span>
		<div>
			<h2 class="m-0 text-lg font-semibold text-[var(--color-on-surface)]">Materiais de estudo</h2>
			<p class="mt-1 text-sm text-[var(--color-outline)]">PDF · Programação &amp; Inglês</p>
		</div>
	</header>

	<form class="flex flex-col gap-3" onsubmit={onSubmit}>
		<input
			type="file"
			class="file-input w-full bg-[var(--color-surface-container-lowest)]"
			accept=".pdf,application/pdf"
			onchange={onFileChange}
			disabled={uploading}
		/>
		<button
			type="submit"
			class="btn self-start rounded-full border-none bg-[var(--color-primary)] text-[var(--color-primary-content)]"
			disabled={uploading || !selectedFile}
		>
			{uploading ? 'Indexando…' : 'Enviar PDF'}
		</button>
	</form>

	{#if uploading}
		<div role="status" class="alert alert-info text-sm">
			<span class="loading loading-spinner loading-sm"></span>
			<span>Extraindo texto e gerando embeddings — pode levar alguns minutos.</span>
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
					<strong>{result.filename}</strong> · {result.chunks_indexed} trechos indexados
				</p>
			</div>
		</div>
	{/if}
</section>

<script lang="ts">
	import { Database } from '@lucide/svelte';
	import { uploadPdf } from '$lib/api/upload';
	import type { UploadResponse } from '$lib/api/types';

	let selectedFile = $state<File | null>(null);
	let uploading = $state(false);
	let result = $state<UploadResponse | null>(null);
	let error = $state<string | null>(null);

	function onFileChange(event: Event) {
		const input = event.currentTarget as HTMLInputElement;
		selectedFile = input.files?.[0] ?? null;
		result = null;
		error = null;
	}

	async function onSubmit(event: SubmitEvent) {
		event.preventDefault();
		if (!selectedFile) {
			error = 'Selecione um arquivo PDF.';
			return;
		}

		uploading = true;
		error = null;
		result = null;

		try {
			result = await uploadPdf(selectedFile);
		} catch (err) {
			error = err instanceof Error ? err.message : 'Erro ao enviar o PDF.';
		} finally {
			uploading = false;
		}
	}
</script>
