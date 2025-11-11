// POST /api/auth/login
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { prisma } from '$lib/server/db';
import { verifyPassword, generateToken } from '$lib/server/auth';
import type { ApiResponse } from '$lib/types';

export const POST: RequestHandler = async ({ request, cookies }) => {
	try {
		const { email, password } = await request.json();

		if (!email || !password) {
			return json<ApiResponse>({
				success: false,
				error: 'Email and password are required'
			}, { status: 400 });
		}

		// Find user
		const user = await prisma.user.findUnique({
			where: { email }
		});

		if (!user || !user.isActive) {
			return json<ApiResponse>({
				success: false,
				error: 'Invalid credentials'
			}, { status: 401 });
		}

		// Verify password
		const isValid = await verifyPassword(password, user.password);
		if (!isValid) {
			return json<ApiResponse>({
				success: false,
				error: 'Invalid credentials'
			}, { status: 401 });
		}

		// Generate token
		const token = generateToken({
			id: user.id,
			email: user.email,
			isAdmin: user.isAdmin
		});

		// Set cookie
		cookies.set('auth_token', token, {
			path: '/',
			httpOnly: true,
			secure: process.env.NODE_ENV === 'production',
			sameSite: 'lax',
			maxAge: 60 * 60 * 24 * 7 // 7 days
		});

		return json<ApiResponse>({
			success: true,
			data: {
				id: user.id,
				email: user.email,
				firstName: user.firstName,
				lastName: user.lastName,
				isAdmin: user.isAdmin,
				token
			}
		});
	} catch (error) {
		console.error('Login error:', error);
		return json<ApiResponse>({
			success: false,
			error: 'Internal server error'
		}, { status: 500 });
	}
};

