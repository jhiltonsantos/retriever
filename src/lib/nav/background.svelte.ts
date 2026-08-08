const MODAL_ROUTES = ['/ingest', '/settings', '/library', '/info', '/history'];

let backgroundPath = $state('/');

export function isModalRoute(pathname: string): boolean {
	return MODAL_ROUTES.some((route) => pathname === route || pathname.startsWith(route + '/'));
}

export function getBackgroundPath(): string {
	return backgroundPath;
}

export function setBackgroundPath(pathname: string): void {
	if (!isModalRoute(pathname)) {
		backgroundPath = pathname;
	}
}
