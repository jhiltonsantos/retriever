type AlertRequest = { kind: 'alert'; message: string; title?: string };
type ConfirmRequest = {
	kind: 'confirm';
	message: string;
	title?: string;
	confirmLabel?: string;
	cancelLabel?: string;
	variant?: 'default' | 'error';
};
type Request = AlertRequest | ConfirmRequest;

let current = $state<Request | null>(null);
let resolver: ((result: boolean) => void) | null = null;

export function getCurrentRequest(): Request | null {
	return current;
}

export function showAlert(message: string, opts: Omit<AlertRequest, 'kind' | 'message'> = {}): Promise<void> {
	return new Promise((resolve) => {
		current = { kind: 'alert', message, ...opts };
		resolver = () => resolve();
	});
}

export function showConfirm(
	message: string,
	opts: Omit<ConfirmRequest, 'kind' | 'message'> = {}
): Promise<boolean> {
	return new Promise((resolve) => {
		current = { kind: 'confirm', message, ...opts };
		resolver = (result: boolean) => resolve(result);
	});
}

export function resolveCurrent(result: boolean): void {
	const r = resolver;
	current = null;
	resolver = null;
	r?.(result);
}
