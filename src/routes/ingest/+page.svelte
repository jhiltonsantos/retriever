<PageNav title="Materiais de estudo" />

<main class="w-full max-w-lg mx-auto flex flex-col gap-4">
	<div role="tablist" class="tabs tabs-border">
		<button
			role="tab"
			class="tab {activeTab === 'file' ? 'tab-active' : ''}"
			onclick={() => (activeTab = 'file')}
		>
			Arquivo
		</button>
		<button
			role="tab"
			class="tab {activeTab === 'text' ? 'tab-active' : ''}"
			onclick={() => (activeTab = 'text')}
		>
			Texto
		</button>
	</div>

	{#if activeTab === 'file'}
		<PdfUpload />
	{:else}
		<TextIngest />
	{/if}
</main>

<script lang="ts">
	import PageNav from '$lib/components/PageNav.svelte';
	import PdfUpload from '$lib/components/PdfUpload.svelte';
	import TextIngest from '$lib/components/TextIngest.svelte';

	let activeTab = $state<'file' | 'text'>('file');
</script>
