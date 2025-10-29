import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Используем vitePreprocess для поддержки PostCSS/Tailwind
	preprocess: vitePreprocess(),
	
	kit: {
		adapter: adapter(),
		
		// Алиасы для удобного импорта
		alias: {
			$lib: './src/lib',
			$components: './src/lib/components',
			$utils: './src/lib/utils'
		}
	},
	
	// Конфигурация для Svelte 5
	compilerOptions: {
		// Включаем runes mode для Svelte 5
		runes: true
	}
};

export default config;