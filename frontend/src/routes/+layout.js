import '../app.css';
import Layout from '$lib/components/Layout.svelte';

/** @type {import('./$types').LayoutLoad} */
export function load() {
	return {
		title: 'GoodDrive'
	};
}

export default Layout;
