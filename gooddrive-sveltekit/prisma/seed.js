// Seed script for initial data
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
	console.log('🌱 Seeding database...\n');

	// Create admin user
	const hashedPassword = await bcrypt.hash('admin123', 10);
	
	const admin = await prisma.user.upsert({
		where: { email: 'admin@gooddrive.com' },
		update: {},
		create: {
			email: 'admin@gooddrive.com',
			password: hashedPassword,
			firstName: 'Admin',
			lastName: 'User',
			isAdmin: true,
			isStaff: true,
			isActive: true
		}
	});

	console.log('✓ Created admin user:', admin.email);
	console.log('  Password: admin123');

	// Create expense categories
	const categories = await prisma.expenseCategory.createMany({
		data: [
			{ name: 'Аренда', description: 'Аренда помещений и складов' },
			{ name: 'Зарплата', description: 'Заработная плата сотрудников' },
			{ name: 'Закупка товаров', description: 'Закупка автозапчастей' },
			{ name: 'Реклама', description: 'Маркетинг и реклама' },
			{ name: 'Коммунальные услуги', description: 'Электричество, вода, интернет' }
		],
		skipDuplicates: true
	});

	console.log('✓ Created expense categories');

	// Create SEO metadata
	await prisma.seoMetadata.createMany({
		data: [
			{
				page: 'home',
				title: 'GoodDrive - Автозапчасти с доставкой',
				description: 'Интернет-магазин автозапчастей. Большой ассортимент, выгодные цены, быстрая доставка по всей России.',
				keywords: 'автозапчасти, запчасти, автомагазин, доставка запчастей'
			},
			{
				page: 'catalog',
				title: 'Каталог автозапчастей - GoodDrive',
				description: 'Каталог автозапчастей более чем на 100 наименований. Подбор по марке, модели и VIN.',
				keywords: 'каталог запчастей, купить запчасти, автозапчасти онлайн'
			}
		],
		skipDuplicates: true
	});

	console.log('✓ Created SEO metadata');

	console.log('\n✅ Seeding completed!\n');
	console.log('Login credentials:');
	console.log('  Email: admin@gooddrive.com');
	console.log('  Password: admin123');
}

main()
	.catch((e) => {
		console.error(e);
		process.exit(1);
	})
	.finally(async () => {
		await prisma.$disconnect();
	});

