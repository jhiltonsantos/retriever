<section class="flex flex-col gap-4">
	<header class="flex items-start gap-3">
		<span
			class="flex size-12 shrink-0 items-center justify-center rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
		>
			<Info size={20} />
		</span>
		<div>
			<h2 class="m-0 text-lg font-semibold text-[var(--color-on-surface)]">Sobre</h2>
			<p class="mt-1 text-sm text-[var(--color-outline)]">Informações sobre o Retriever</p>
		</div>
	</header>

	<dl class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-sm">
		<dt class="text-[var(--color-outline)]">Versão</dt>
		<dd>0.0.1</dd>
		<dt class="text-[var(--color-outline)]">Descrição</dt>
		<dd>Assistente de estudos e documentação pessoal</dd>
	</dl>

	<div class="flex flex-col gap-2 text-sm text-[var(--color-outline)]">
		<p>
			O Retriever é um tutor RAG que roda localmente. Seus documentos são indexados em um banco
			vetorial e as respostas são geradas por um modelo de linguagem escolhido por você.
		</p>
		<p>
			Documentação completa está disponível no repositório:
			<a
				href="https://github.com/jhiltonsantos/retriever"
				target="_blank"
				rel="noopener noreferrer"
				class="text-[var(--color-primary)] underline"
			>
				github.com/jhiltonsantos/retriever
			</a>
			.
		</p>
	</div>
</section>

<script lang="ts">
	import { Info } from '@lucide/svelte';
</script>
