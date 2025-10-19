<script>
  import { onMount } from 'svelte';
  import { partsApi, brandsApi } from '$lib/utils/api.js';
  import SeoHead from '$lib/components/SeoHead.svelte';
  import { generateOrganizationJsonLd } from '$lib/utils/seo.js';
  
  // Реактивное состояние
  let featuredParts = $state([]);
  let brands = $state([]);
  let isLoading = $state(true);
  let stats = $state({
    totalParts: 0,
    brands: 0,
    customers: 0
  });
  
  // Производные значения
  const hasFeaturedParts = $derived(featuredParts.length > 0);
  
  // SEO данные
  const seoData = $derived({
    title: 'GoodDrive - Интернет-магазин автозапчастей',
    description: 'Широкий выбор автозапчастей от ведущих производителей. Быстрая доставка по всей России. Гарантия качества.',
    keywords: 'автозапчасти, интернет-магазин, автомобильные детали, доставка, гарантия',
    image: '/images/home-og.jpg',
    type: 'website'
  });

  // JSON-LD для организации
  const organizationJsonLd = $derived(generateOrganizationJsonLd());
  
  // Загрузка данных при монтировании компонента
  onMount(async () => {
    try {
      // Загружаем популярные товары
      const partsData = await partsApi.getParts({
        ordering: '-created_at',
        page_size: 6
      });
      featuredParts = partsData.results || [];
      
      // Загружаем бренды
      const brandsData = await brandsApi.getBrands({ page_size: 8 });
      brands = brandsData.results || brandsData;
      
      // Обновляем статистику
      stats = {
        totalParts: partsData.count || 0,
        brands: brands.length,
        customers: 1500 // Примерное количество клиентов
      };
    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
    } finally {
      isLoading = false;
    }
  });
</script>

<SeoHead
  title={seoData.title}
  description={seoData.description}
  keywords={seoData.keywords}
  image={seoData.image}
  type={seoData.type}
  jsonLd={organizationJsonLd}
/>

<!-- Hero секция -->
<section class="bg-gradient-to-r from-primary-500 to-primary-600 text-white">
  <div class="container-custom py-20">
    <div class="max-w-3xl mx-auto text-center">
      <h1 class="text-4xl md:text-6xl font-bold mb-6 animate-fade-in">
        Автозапчасти для вашего автомобиля
      </h1>
      <p class="text-xl md:text-2xl mb-8 text-primary-100 animate-slide-up">
        Широкий выбор оригинальных и совместимых запчастей от ведущих производителей
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="/catalog" class="btn-primary bg-white text-primary-600 hover:bg-primary-50 text-lg px-8 py-3">
          Перейти в каталог
        </a>
        <a href="/about" class="btn-outline border-white text-white hover:bg-white hover:text-primary-600 text-lg px-8 py-3">
          О компании
        </a>
      </div>
    </div>
  </div>
</section>

<!-- Статистика -->
<section class="py-16 bg-white">
  <div class="container-custom">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="text-center">
        <div class="text-4xl font-bold text-primary-500 mb-2">{stats.totalParts.toLocaleString()}</div>
        <div class="text-neutral-600">Товаров в каталоге</div>
      </div>
      <div class="text-center">
        <div class="text-4xl font-bold text-primary-500 mb-2">{stats.brands}</div>
        <div class="text-neutral-600">Брендов</div>
      </div>
      <div class="text-center">
        <div class="text-4xl font-bold text-primary-500 mb-2">{stats.customers.toLocaleString()}</div>
        <div class="text-neutral-600">Довольных клиентов</div>
      </div>
    </div>
  </div>
</section>

<!-- Популярные товары -->
<section class="py-16 bg-neutral-50">
  <div class="container-custom">
    <div class="text-center mb-12">
      <h2 class="text-3xl font-bold text-neutral-900 mb-4">Популярные товары</h2>
      <p class="text-neutral-600 max-w-2xl mx-auto">
        Самые востребованные автозапчасти, которые выбирают наши клиенты
      </p>
    </div>
    
    {#if isLoading}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each Array(6) as _}
          <div class="card p-6 animate-pulse">
            <div class="bg-neutral-200 h-48 rounded-lg mb-4"></div>
            <div class="bg-neutral-200 h-4 rounded mb-2"></div>
            <div class="bg-neutral-200 h-4 rounded w-3/4 mb-4"></div>
            <div class="bg-neutral-200 h-6 rounded w-1/2"></div>
          </div>
        {/each}
      </div>
    {:else if hasFeaturedParts}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each featuredParts as part}
          <div class="card p-6 hover:shadow-md transition-shadow">
            <div class="aspect-square bg-neutral-100 rounded-lg mb-4 flex items-center justify-center">
              {#if part.main_image}
                <img 
                  src={part.main_image.url} 
                  alt={part.main_image.alt || part.title}
                  class="w-full h-full object-cover rounded-lg"
                />
              {:else}
                <svg class="w-16 h-16 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              {/if}
            </div>
            <h3 class="font-semibold text-neutral-900 mb-2 line-clamp-2">{part.title}</h3>
            <p class="text-neutral-600 text-sm mb-4">{part.brand_name}</p>
            <div class="flex items-center justify-between">
              <span class="text-lg font-bold text-primary-500">{part.price_opt.toLocaleString()} ₽</span>
              <span class="text-sm text-neutral-500">В наличии: {part.available}</span>
            </div>
            <a 
              href="/product/{part.id}" 
              class="btn-primary w-full mt-4"
            >
              Подробнее
            </a>
          </div>
        {/each}
      </div>
      <div class="text-center mt-8">
        <a href="/catalog" class="btn-outline">
          Смотреть все товары
        </a>
      </div>
    {:else}
      <div class="text-center py-12">
        <svg class="w-16 h-16 text-neutral-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
        <p class="text-neutral-600">Товары временно недоступны</p>
      </div>
    {/if}
  </div>
</section>

<!-- Преимущества -->
<section class="py-16 bg-white">
  <div class="container-custom">
    <div class="text-center mb-12">
      <h2 class="text-3xl font-bold text-neutral-900 mb-4">Почему выбирают нас</h2>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
      <div class="text-center">
        <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="font-semibold text-neutral-900 mb-2">Гарантия качества</h3>
        <p class="text-neutral-600 text-sm">Только оригинальные и сертифицированные запчасти</p>
      </div>
      
      <div class="text-center">
        <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h3 class="font-semibold text-neutral-900 mb-2">Быстрая доставка</h3>
        <p class="text-neutral-600 text-sm">Доставка по всей России в кратчайшие сроки</p>
      </div>
      
      <div class="text-center">
        <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M12 2.25a9.75 9.75 0 100 19.5 9.75 9.75 0 000-19.5z" />
          </svg>
        </div>
        <h3 class="font-semibold text-neutral-900 mb-2">Широкий ассортимент</h3>
        <p class="text-neutral-600 text-sm">Более {stats.totalParts.toLocaleString()} товаров от ведущих брендов</p>
      </div>
      
      <div class="text-center">
        <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728L5.636 5.636m12.728 12.728L18.364 5.636M5.636 18.364l12.728-12.728" />
          </svg>
        </div>
        <h3 class="font-semibold text-neutral-900 mb-2">Техподдержка 24/7</h3>
        <p class="text-neutral-600 text-sm">Круглосуточная поддержка наших специалистов</p>
      </div>
    </div>
  </div>
</section>
