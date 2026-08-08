<section class="flex flex-col gap-4">
	<header class="flex items-start gap-3">
		<span
			class="flex size-12 shrink-0 items-center justify-center rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
		>
			<User size={20} />
		</span>
		<div>
			<h2 class="m-0 text-lg font-semibold text-[var(--color-on-surface)]">Perfil</h2>
			<p class="mt-1 text-sm text-[var(--color-outline)]">Como o tutor deve te chamar</p>
		</div>
	</header>

	{#if loading}
		<div role="status" class="alert alert-info text-sm">
			<span class="loading loading-spinner loading-sm"></span>
			<span>Carregando perfil…</span>
		</div>
	{:else}
		<form class="flex flex-col gap-4" onsubmit={onSave}>
			<label class="flex flex-col gap-1">
				<span class="label-text text-sm">Nome de exibição</span>
				<input
					type="text"
					class="input w-full bg-[var(--color-surface-container-lowest)]"
					placeholder="Seu nome"
					bind:value={displayName}
				/>
			</label>

			<button
				type="submit"
				class="btn w-fit rounded-full border-none bg-[var(--color-primary)] text-[var(--color-primary-content)]"
				disabled={saving}
			>
				{saving ? 'Salvando…' : 'Salvar'}
			</button>
		</form>
	{/if}

	{#if saveError}
		<div role="alert" class="alert alert-error text-sm">
			<span>{saveError}</span>
		</div>
	{/if}

	{#if saved}
		<div role="status" class="alert alert-success text-sm">
			<span>Perfil salvo.</span>
		</div>
	{/if}
</section>

<script lang="ts">
	import { onMount } from 'svelte';
	import { User } from '@lucide/svelte';
	import { getProfile, updateProfile } from '$lib/api/profile';

	let displayName = $state('');
	let loading = $state(true);
	let saving = $state(false);
	let saved = $state(false);
	let saveError = $state<string | null>(null);

	onMount(async () => {
		try {
			const profile = await getProfile();
			displayName = profile.display_name ?? '';
		} catch (err) {
			saveError = err instanceof Error ? err.message : 'Erro ao carregar perfil.';
		} finally {
			loading = false;
		}
	});

	async function onSave(event: SubmitEvent) {
		event.preventDefault();
		saving = true;
		saved = false;
		saveError = null;
		try {
			await updateProfile(displayName.trim() || null);
			saved = true;
		} catch (err) {
			saveError = err instanceof Error ? err.message : 'Erro ao salvar perfil.';
		} finally {
			saving = false;
		}
	}
</script>
