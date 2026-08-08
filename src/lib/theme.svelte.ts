const STORAGE_KEY = 'retriever:theme';

export type Theme = 'retriever' | 'retriever-dark';

let theme = $state<Theme>('retriever-dark');

export function getTheme(): Theme {
	return theme;
}

export function setTheme(next: Theme): void {
	theme = next;
	if (typeof document !== 'undefined') {
		document.documentElement.setAttribute('data-theme', next);
	}
	if (typeof localStorage !== 'undefined') {
		localStorage.setItem(STORAGE_KEY, next);
	}
}

export function toggleTheme(): void {
	setTheme(theme === 'retriever-dark' ? 'retriever' : 'retriever-dark');
}

export function initTheme(): void {
	if (typeof window === 'undefined') {
		return;
	}

	const stored = localStorage.getItem(STORAGE_KEY) as Theme | null;
	const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches;
	theme = stored ?? (prefersDark ? 'retriever-dark' : 'retriever');
}
