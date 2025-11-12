import { db } from '$lib/server/db';
import type { RequestHandler } from './$types';

export const prerender = false;

export const GET: RequestHandler = async () => {
	try {
		const baseUrl = 'https://gooddrive.com';
		const today = new Date().toISOString().split('T')[0];

		// Получаем все товары
		const parts = await db.part.findMany({
			select: {
				id: true,
				updated_at: true
			},
			where: {
				available: {
					gt: 0
				}
			},
			orderBy: {
				updated_at: 'desc'
			}
		});

		// Получаем бренды для динамических страниц каталога
		const brands = await db.brand.findMany({
			select: {
				id: true,
				name: true
			}
		});

		// Генерируем XML sitemap
		const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
	
	<!-- Главная страница -->
	<url>
		<loc>${baseUrl}/</loc>
		<lastmod>${today}</lastmod>
		<changefreq>daily</changefreq>
		<priority>1.0</priority>
	</url>
	
	<!-- Каталог -->
	<url>
		<loc>${baseUrl}/catalog</loc>
		<lastmod>${today}</lastmod>
		<changefreq>daily</changefreq>
		<priority>0.9</priority>
	</url>
	
	<!-- Корзина -->
	<url>
		<loc>${baseUrl}/cart</loc>
		<lastmod>${today}</lastmod>
		<changefreq>weekly</changefreq>
		<priority>0.7</priority>
	</url>
	
	<!-- Оформление заказа -->
	<url>
		<loc>${baseUrl}/checkout</loc>
		<lastmod>${today}</lastmod>
		<changefreq>weekly</changefreq>
		<priority>0.7</priority>
	</url>
	
	<!-- Страницы брендов в каталоге -->
	${brands
		.map(
			(brand) => `
	<url>
		<loc>${baseUrl}/catalog?brand=${brand.id}</loc>
		<lastmod>${today}</lastmod>
		<changefreq>weekly</changefreq>
		<priority>0.8</priority>
	</url>`
		)
		.join('')}
	
	<!-- Страницы товаров -->
	${parts
		.map(
			(part) => `
	<url>
		<loc>${baseUrl}/product/${part.id}</loc>
		<lastmod>${part.updated_at.toISOString().split('T')[0]}</lastmod>
		<changefreq>weekly</changefreq>
		<priority>0.8</priority>
	</url>`
		)
		.join('')}
	
</urlset>`;

		return new Response(sitemap.trim(), {
			headers: {
				'Content-Type': 'application/xml; charset=utf-8',
				'Cache-Control': 'public, max-age=3600' // Кешируем на 1 час
			}
		});
	} catch (error) {
		console.error('Error generating sitemap:', error);
		return new Response('Error generating sitemap', { status: 500 });
	}
};

