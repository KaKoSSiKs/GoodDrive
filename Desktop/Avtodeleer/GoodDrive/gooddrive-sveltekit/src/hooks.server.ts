// Server hooks for authentication and security
import { verifyToken, type UserSession } from '$lib/server/auth';
import { prisma } from '$lib/server/db';
import type { Handle } from '@sveltejs/kit';
import { dev } from '$app/environment';

export const handle: Handle = async ({ event, resolve }) => {
	// Get token from cookie
	const token = event.cookies.get('auth_token');

	if (token) {
		const payload = verifyToken(token);
		if (payload) {
			// Load full user data
			const user = await prisma.user.findUnique({
				where: { id: payload.userId },
				select: {
					id: true,
					email: true,
					firstName: true,
					lastName: true,
					isAdmin: true,
					isStaff: true,
					isActive: true
				}
			});

			if (user && user.isActive) {
				event.locals.user = user as UserSession;
			}
		}
	}

	// Resolve the request
	const response = await resolve(event);

	// Security Headers (только для production)
	if (!dev) {
		// Защита от clickjacking
		response.headers.set('X-Frame-Options', 'DENY');
		
		// Предотвращение MIME type sniffing
		response.headers.set('X-Content-Type-Options', 'nosniff');
		
		// Referrer Policy
		response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
		
		// Permissions Policy
		response.headers.set(
			'Permissions-Policy',
			'geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=()'
		);
		
		// HSTS (HTTP Strict Transport Security)
		response.headers.set(
			'Strict-Transport-Security',
			'max-age=31536000; includeSubDomains; preload'
		);
		
		// Content Security Policy
		const cspDirectives = [
			"default-src 'self'",
			"script-src 'self' 'unsafe-inline' 'unsafe-eval' https://mc.yandex.ru https://yandex.ru https://www.googletagmanager.com https://www.google-analytics.com",
			"style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
			"img-src 'self' data: https: http:",
			"font-src 'self' https://fonts.gstatic.com data:",
			"connect-src 'self' https://mc.yandex.ru https://www.google-analytics.com",
			"frame-src 'self' https://yandex.ru https://yandex.com",
			"object-src 'none'",
			"base-uri 'self'",
			"form-action 'self'",
			"frame-ancestors 'none'",
			"upgrade-insecure-requests"
		];
		response.headers.set('Content-Security-Policy', cspDirectives.join('; '));
		
		// X-XSS-Protection (legacy, но все еще полезен)
		response.headers.set('X-XSS-Protection', '1; mode=block');
	}
	
	// CORS для API endpoints
	if (event.url.pathname.startsWith('/api/')) {
		response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
		response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
		
		// В production указать конкретный origin
		if (dev) {
			response.headers.set('Access-Control-Allow-Origin', '*');
		}
	}

	return response;
};

