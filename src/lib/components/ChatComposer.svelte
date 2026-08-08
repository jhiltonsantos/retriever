<form class="flex flex-col gap-3 shrink-0" onsubmit={handleSubmit}>
	<textarea
		class="textarea textarea-bordered w-full min-h-20 resize-y bg-base-100"
		bind:value
		onkeydown={onKeydown}
		placeholder="Ex.: Quais são os padrões de projeto mais usados?"
		rows="3"
		disabled={submitting}
		required
	></textarea>
	<button type="submit" class="btn btn-primary self-start" disabled={submitting || !value.trim()}>
		{submitting ? 'Pensando…' : 'Enviar pergunta'}
	</button>
</form>

<script lang="ts">
	type Props = {
		value: string;
		submitting: boolean;
		onSubmit: () => void;
	};

	let { value = $bindable(''), submitting, onSubmit }: Props = $props();

	function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		if (!value.trim() || submitting) return;
		onSubmit();
	}

	function onKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			if (!value.trim() || submitting) return;
			onSubmit();
		}
	}
</script>
