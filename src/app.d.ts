// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces

export interface RetrieverDesktop {
	getApiUrl: () => string;
	checkOllama: () => Promise<boolean>;
	isDesktop: boolean;
}

declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}

	interface Window {
		retriever?: RetrieverDesktop;
	}
}

export {};
