// GET /api/parts - List parts with pagination and filtering
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { prisma } from '$lib/server/db';
import type { PaginatedResponse, ApiResponse } from '$lib/types';

export const GET: RequestHandler = async ({ url }) => {
	try {
		const page = parseInt(url.searchParams.get('page') || '1');
		const pageSize = parseInt(url.searchParams.get('page_size') || '20');
		const search = url.searchParams.get('search') || '';
		const brandId = url.searchParams.get('brand');
		const warehouseId = url.searchParams.get('warehouse');
		const ordering = url.searchParams.get('ordering') || '-created_at';

	// Build where clause
	const where: any = { isActive: true };
	
	if (search) {
		where.OR = [
			{ title: { contains: search, mode: 'insensitive' } },
			{ originalNumber: { contains: search, mode: 'insensitive' } },
			{ manufacturerNumber: { contains: search, mode: 'insensitive' } }
		];
	}

	if (brandId) {
		where.brandId = parseInt(brandId);
	}

	if (warehouseId) {
		where.warehouseId = parseInt(warehouseId);
	}

	// Фильтр по низкому остатку
	const lowStock = url.searchParams.get('low_stock');
	if (lowStock === 'true') {
		where.available = {
			lte: 5,
			gt: 0
		};
	}

	// Фильтр по максимальному количеству
	const availableMax = url.searchParams.get('available_max');
	if (availableMax) {
		where.available = {
			...where.available,
			lte: parseInt(availableMax)
		};
	}

	// Фильтр по цене
	const priceMin = url.searchParams.get('price_min');
	const priceMax = url.searchParams.get('price_max');
	if (priceMin || priceMax) {
		where.priceOpt = {};
		if (priceMin) {
			where.priceOpt.gte = parseFloat(priceMin);
		}
		if (priceMax) {
			where.priceOpt.lte = parseFloat(priceMax);
		}
	}

		// Build orderBy
		const orderBy: any = [];
		if (ordering) {
			const isDesc = ordering.startsWith('-');
			const field = isDesc ? ordering.substring(1) : ordering;
			const direction = isDesc ? 'desc' : 'asc';
			
			if (field === 'created_at') {
				orderBy.push({ createdAt: direction });
			} else if (field === 'price_opt') {
				orderBy.push({ priceOpt: direction });
			} else if (field === 'title') {
				orderBy.push({ title: direction });
			}
		}

		// Get total count
		const total = await prisma.part.count({ where });

		// Get parts
		const parts = await prisma.part.findMany({
			where,
			skip: (page - 1) * pageSize,
			take: pageSize,
			orderBy,
			include: {
				brand: {
					select: {
						id: true,
						name: true,
						country: true,
						site: true
					}
				},
				warehouse: {
					select: {
						id: true,
						name: true,
						address: true
					}
				},
				images: {
					orderBy: { orderIndex: 'asc' },
					select: {
						id: true,
						imageUrl: true,
						altText: true,
						orderIndex: true
					}
				}
			}
		});

		const results = parts.map(part => ({
			id: part.id,
			is_active: part.isActive,
			title: part.title,
			label: part.label,
			original_number: part.originalNumber,
			manufacturer_number: part.manufacturerNumber,
			brand: part.brand,
			brand_name: part.brand?.name || '',
			warehouse: part.warehouse,
			warehouse_name: part.warehouse?.name || '',
			quantity: part.quantity,
			stock: part.stock,
			reserve: part.reserve,
			available: part.available,
			price_opt: part.priceOpt.toFixed(2),
			cost_price: part.costPrice.toFixed(2),
			description: part.description,
			images: part.images.map(img => ({
				id: img.id,
				image_url: img.imageUrl,
				alt_text: img.altText || part.title,
				order_index: img.orderIndex
			})),
			created_at: part.createdAt.toISOString(),
			updated_at: part.updatedAt.toISOString()
		}));

		const totalPages = Math.ceil(total / pageSize);

		return json<PaginatedResponse<typeof results[0]>>({
			count: total,
			next: page < totalPages ? `/api/parts?page=${page + 1}&page_size=${pageSize}` : null,
			previous: page > 1 ? `/api/parts?page=${page - 1}&page_size=${pageSize}` : null,
			results
		});
	} catch (error) {
		console.error('Parts fetch error:', error);
		return json<ApiResponse>({
			success: false,
			error: 'Failed to fetch parts'
		}, { status: 500 });
	}
};

