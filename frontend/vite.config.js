import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		sveltekit({
			// Отключаем runes mode для внешних библиотек
			compilerOptions: {
				// Используем функцию для определения, нужен ли runes mode
				// для конкретного файла
			},
			// Игнорируем предупреждения от библиотек в node_modules
			onwarn: (warning, handler) => {
				// Игнорируем ошибки legacy_props_invalid из node_modules
				if (warning.code === 'legacy_props_invalid' && warning.filename?.includes('node_modules')) {
					return;
				}
				handler(warning);
			}
		})
	],
	
	server: {
		port: 3000,
		host: true,
		watch: {
			// Следим за изменениями в tailwind.config.js
			usePolling: true
		}
	},
	
	css: {
		postcss: './postcss.config.js'
	},
	
	// Оптимизация для dev сервера
	optimizeDeps: {
		include: ['tailwindcss', 'autoprefixer', 'lucide-svelte']
	}
});

