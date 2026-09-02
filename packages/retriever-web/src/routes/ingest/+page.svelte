<div role="tablist" class="tabs tabs-border mb-4">
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

<script lang="ts">
	import PdfUpload from '$lib/components/PdfUpload.svelte';
	import TextIngest from '$lib/components/TextIngest.svelte';

	let activeTab = $state<'file' | 'text'>('file');
</script>
