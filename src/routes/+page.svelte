<header class="text-center mb-8">
	<h1 class="text-3xl font-bold tracking-tight m-0">Retriever</h1>
	<p class="mt-2 mx-auto max-w-xl text-base-content/70">
		Assistente de estudos pessoal · RAG para Engenharia de Software e Inglês
	</p>
</header>

<main class="grid grid-cols-1 md:grid-cols-2 gap-5">
	<ActionCard
		href="/upload"
		title="Enviar PDF"
		description="Indexe materiais de programação e inglês no ChromaDB para consultas futuras."
		badge={'{ }'}
		badgeVariant="code"
		cta="Abrir →"
	/>
	<ActionCard
		href="/chat"
		title="Conversar com o tutor"
		description="Faça perguntas com base nos documentos que você já enviou."
		badge="Aa"
		badgeVariant="lang"
		cta="Iniciar →"
	/>
	<ActionCard
		href="/settings"
		title="Configurações"
		description="Escolha o provedor e o modelo de LLM usados nas respostas."
		badge="cfg"
		badgeVariant="code"
		cta="Ajustar →"
	/>
</main>

<script lang="ts">
	import ActionCard from '$lib/components/ActionCard.svelte';
</script>
