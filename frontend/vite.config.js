import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	
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
		include: ['tailwindcss', 'autoprefixer']
	}
});

