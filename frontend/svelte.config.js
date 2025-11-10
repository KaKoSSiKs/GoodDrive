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
		// Включаем runes mode только для нашего кода (не для библиотек)
		runes: true
	},
	
	// Настройка плагина для правильной обработки библиотек
	vitePlugin: {
		// Динамическая настройка компилятора для разных файлов
		dynamicCompileOptions({ filename }) {
			// Для файлов из node_modules отключаем runes mode
			if (filename?.includes('node_modules')) {
				return {
					runes: false
				};
			}
			// Для остальных файлов используем runes mode
			return {
				runes: true
			};
		}
	}
};

export default config;