// Server hooks for authentication
import { verifyToken, type UserSession } from '$lib/server/auth';
import { prisma } from '$lib/server/db';
import type { Handle } from '@sveltejs/kit';

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

	return resolve(event);
};

