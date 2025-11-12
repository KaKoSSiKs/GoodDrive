// Authentication utilities
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';
import type { User } from '@prisma/client';

const SALT_ROUNDS = 10;
const JWT_SECRET = process.env.JWT_SECRET || 'supersecretkey12345678901234567890123456789012';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '7d';

export interface JWTPayload {
	userId: number;
	email: string;
	isAdmin: boolean;
}

export interface UserSession {
	id: number;
	email: string;
	firstName: string | null;
	lastName: string | null;
	isAdmin: boolean;
	isStaff: boolean;
}

/**
 * Hash password
 */
export async function hashPassword(password: string): Promise<string> {
	return bcrypt.hash(password, SALT_ROUNDS);
}

/**
 * Verify password
 */
export async function verifyPassword(password: string, hash: string): Promise<boolean> {
	return bcrypt.compare(password, hash);
}

/**
 * Generate JWT token
 */
export function generateToken(user: { id: number; email: string; isAdmin: boolean }): string {
	const payload: JWTPayload = {
		userId: user.id,
		email: user.email,
		isAdmin: user.isAdmin
	};

	return jwt.sign(payload, JWT_SECRET, {
		expiresIn: JWT_EXPIRES_IN || '7d'
	});
}

/**
 * Verify JWT token
 */
export function verifyToken(token: string): JWTPayload | null {
	try {
		return jwt.verify(token, JWT_SECRET) as JWTPayload;
	} catch {
		return null;
	}
}

/**
 * Convert User to UserSession
 */
export function toUserSession(user: User): UserSession {
	return {
		id: user.id,
		email: user.email,
		firstName: user.firstName,
		lastName: user.lastName,
		isAdmin: user.isAdmin,
		isStaff: user.isStaff
	};
}

