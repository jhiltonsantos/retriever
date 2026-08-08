<svelte:head>
	<link rel="icon" href={favicon} />
	<title>Retriever · Tutor RAG</title>
	<meta name="description" content="Assistente de estudos pessoal para Engenharia de Software e Inglês" />
</svelte:head>

<div class="flex h-screen bg-[var(--color-base-100)] text-[var(--color-base-content)]">
	<SideNav />
	<div class="relative flex-1 overflow-hidden">
		{#if isModalRoute(page.url.pathname)}
			{#if getBackgroundPath() === '/chat'}
				<ChatCanvas />
			{:else}
				<HomeCanvas />
			{/if}
			<RouteModal
				onClose={() => goto(getBackgroundPath())}
				size={page.url.pathname.startsWith('/history') ? 'lg' : 'md'}
			>
				{@render children()}
			</RouteModal>
		{:else}
			{@render children()}
		{/if}
	</div>
</div>
<AlertModal />

<script lang="ts">
	import { onMount } from 'svelte';
	import { afterNavigate, goto } from '$app/navigation';
	import { page } from '$app/state';
	import favicon from '$lib/assets/favicon.svg';
	import SideNav from '$lib/components/SideNav.svelte';
	import RouteModal from '$lib/components/RouteModal.svelte';
	import AlertModal from '$lib/components/AlertModal.svelte';
	import HomeCanvas from '$lib/components/HomeCanvas.svelte';
	import ChatCanvas from '$lib/components/ChatCanvas.svelte';
	import { isModalRoute, getBackgroundPath, setBackgroundPath } from '$lib/nav/background.svelte';
	import { initTheme } from '$lib/theme.svelte';
	import type { LayoutProps } from './$types';
	import '../app.css';

	let { children }: LayoutProps = $props();

	onMount(initTheme);
	afterNavigate(({ to }) => setBackgroundPath(to?.url.pathname ?? '/'));
</script>
