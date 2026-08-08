<section class="flex flex-col gap-4">
	<header class="flex items-start gap-3">
		<span
			class="flex size-12 shrink-0 items-center justify-center rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
		>
			<Cpu size={20} />
		</span>
		<div>
			<h2 class="m-0 text-lg font-semibold text-[var(--color-on-surface)]">Provedor de LLM</h2>
			<p class="mt-1 text-sm text-[var(--color-outline)]">Escolha onde as respostas são geradas</p>
		</div>
	</header>

	{#if loading}
		<div role="status" class="alert alert-info text-sm">
			<span class="loading loading-spinner loading-sm"></span>
			<span>Carregando configuração…</span>
		</div>
	{:else}
		<form class="flex flex-col gap-4" onsubmit={onSave}>
			<div class="flex gap-6">
				<label class="label cursor-pointer gap-2">
					<input
						type="radio"
						name="provider"
						class="radio radio-primary"
						value="ollama"
						checked={provider === 'ollama'}
						onchange={() => onProviderChange('ollama')}
					/>
					<span class="label-text">Ollama local</span>
				</label>
				<label class="label cursor-pointer gap-2">
					<input
						type="radio"
						name="provider"
						class="radio radio-primary"
						value="openrouter"
						checked={provider === 'openrouter'}
						onchange={() => onProviderChange('openrouter')}
					/>
					<span class="label-text">OpenRouter</span>
				</label>
				<label class="label cursor-pointer gap-2">
					<input
						type="radio"
						name="provider"
						class="radio radio-primary"
						value="custom"
						checked={provider === 'custom'}
						onchange={() => onProviderChange('custom')}
					/>
					<span class="label-text">Custom</span>
				</label>
			</div>

			<label class="flex flex-col gap-1">
				<span class="label-text text-sm">Modelo</span>
				<select
					class="select w-full bg-[var(--color-surface-container-lowest)]"
					bind:value={model}
					disabled={modelsLoading || models.length === 0}
				>
					{#each models as m (m.id)}
						<option value={m.id}>{m.label}</option>
					{/each}
				</select>
				{#if modelsLoading}
					<span class="text-xs text-[var(--color-outline)]">Carregando modelos…</span>
				{/if}
			</label>

			<label class="flex flex-col gap-1">
				<span class="label-text text-sm">Base URL</span>
				<input
					type="text"
					class="input w-full bg-[var(--color-surface-container-lowest)]"
					placeholder={provider === 'custom' ? 'https://meu-servidor/v1' : ''}
					bind:value={baseUrl}
				/>
			</label>

			{#if provider === 'openrouter' || provider === 'custom'}
				<label class="flex flex-col gap-1">
					<span class="label-text text-sm">
						Chave de API
						{#if apiKeySet}
							<span class="font-normal opacity-70">(atual: {apiKeyMasked})</span>
						{/if}
					</span>
					<input
						type="password"
						class="input w-full bg-[var(--color-surface-container-lowest)]"
						placeholder={apiKeySet
							? 'Deixe em branco para manter a atual'
							: provider === 'custom'
								? 'Opcional'
								: 'sk-or-...'}
						bind:value={apiKey}
					/>
				</label>
			{/if}

			<div class="flex gap-3">
				<button
					type="button"
					class="btn btn-outline rounded-full"
					onclick={onTest}
					disabled={testing || !model || (provider === 'custom' && !baseUrl)}
				>
					{testing ? 'Testando…' : 'Testar conexão'}
				</button>
				<button
					type="submit"
					class="btn rounded-full border-none bg-[var(--color-primary)] text-[var(--color-primary-content)]"
					disabled={saving || !model || (provider === 'custom' && !baseUrl)}
				>
					{saving ? 'Salvando…' : 'Salvar'}
				</button>
			</div>
		</form>
	{/if}

	{#if testResult}
		<div role="status" class="alert {testResult.ok ? 'alert-success' : 'alert-error'} text-sm">
			<span>{testResult.message}</span>
		</div>
	{/if}

	{#if saveError}
		<div role="alert" class="alert alert-error text-sm">
			<span>{saveError}</span>
		</div>
	{/if}

	{#if saved}
		<div role="status" class="alert alert-success text-sm">
			<span>Configuração salva.</span>
		</div>
	{/if}
</section>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Cpu } from '@lucide/svelte';
	import { getLlmModels, getLlmSettings, testLlmConnection, updateLlmSettings } from '$lib/api/settings';
	import type { LlmModel, LlmProviderId, LlmSettings, TestConnectionResult } from '$lib/settings/types';

	let loading = $state(true);
	let settings = $state<LlmSettings | null>(null);
	let provider = $state<LlmProviderId>('ollama');
	let model = $state('');
	let baseUrl = $state('');
	let apiKey = $state('');
	let apiKeyMasked = $state<string | null>(null);
	let apiKeySet = $state(false);

	let models = $state<LlmModel[]>([]);
	let modelsLoading = $state(false);

	let saving = $state(false);
	let saved = $state(false);
	let saveError = $state<string | null>(null);

	let testing = $state(false);
	let testResult = $state<TestConnectionResult | null>(null);

	function applyProviderToForm(p: LlmProviderId) {
		const cfg = settings!.providers[p];
		model = cfg.model ?? '';
		baseUrl = cfg.base_url;
		apiKey = '';
		apiKeyMasked = cfg.api_key_masked;
		apiKeySet = cfg.api_key_set;
	}

	onMount(async () => {
		try {
			settings = await getLlmSettings();
			provider = settings.active_provider;
			applyProviderToForm(provider);
		} finally {
			loading = false;
		}
		await loadModels(provider);
	});

	async function loadModels(target: LlmProviderId) {
		modelsLoading = true;
		try {
			const response = await getLlmModels(target);
			models = response.models;
			if (!models.some((m) => m.id === model)) {
				model = models[0]?.id ?? '';
			}
		} catch {
			models = [];
		} finally {
			modelsLoading = false;
		}
	}

	function onProviderChange(next: LlmProviderId) {
		provider = next;
		applyProviderToForm(next);
		saved = false;
		testResult = null;
		loadModels(next);
	}

	async function onSave(event: SubmitEvent) {
		event.preventDefault();
		saving = true;
		saveError = null;
		saved = false;
		try {
			settings = await updateLlmSettings({
				provider,
				model,
				base_url: baseUrl || null,
				api_key: apiKey || null
			});
			applyProviderToForm(provider);
			saved = true;
		} catch (err) {
			saveError = err instanceof Error ? err.message : 'Erro ao salvar as configurações.';
		} finally {
			saving = false;
		}
	}

	async function onTest() {
		testing = true;
		testResult = null;
		try {
			testResult = await testLlmConnection({
				provider,
				model,
				base_url: baseUrl || null,
				api_key: apiKey || null
			});
		} catch (err) {
			testResult = {
				ok: false,
				reason: null,
				message: err instanceof Error ? err.message : 'Erro ao testar a conexão.'
			};
		} finally {
			testing = false;
		}
	}
</script>
