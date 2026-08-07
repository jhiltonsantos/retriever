<svelte:head>
	<link rel="icon" href={favicon} />
	<title>Retriever · Tutor RAG</title>
	<meta name="description" content="Assistente de estudos pessoal para Engenharia de Software e Inglês" />
</svelte:head>

<div class="h-screen overflow-y-auto max-w-[1100px] mx-auto p-6 flex flex-col">
	<OllamaStatus />
	{@render children()}
</div>

<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import OllamaStatus from '$lib/components/OllamaStatus.svelte';
	import type { LayoutProps } from './$types';
	import '../app.css';

	let { children }: LayoutProps = $props();
</script>
