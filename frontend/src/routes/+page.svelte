<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { partsApi, brandsApi, seoApi } from '$lib/utils/api.js';
  import PartCard from '$lib/components/PartCard.svelte';
  import SeoHead from '$lib/components/SeoHead.svelte';
  import { generateOrganizationJsonLd } from '$lib/utils/seo.js';

  // SEO данные
  const seoData = $state({
    title: 'GoodDrive - Интернет-магазин автозапчастей | Быстрая доставка по России',
    description: 'Магазин автозапчастей GoodDrive. Широкий ассортимент оригинальных и совместимых запчастей. Быстрая доставка, гарантия качества, консультации специалистов.',
    keywords: 'автозапчасти, запчасти для авто, интернет магазин запчастей, доставка запчастей, оригинальные запчасти',
    image: '/images/home-og.jpg',
    type: 'website'
  });

  // JSON-LD для организации
  const organizationJsonLd = generateOrganizationJsonLd();

  // Реактивное состояние
  let featuredParts = $state([]);
  let loading = $state(true);
  let stats = $state({
    totalParts: 0,
    brands: 0,
    customers: 50000
  });
  let consultationForm = $state({
    vin: '',
    name: '',
    phone: ''
  });

  // Загрузка данных
  async function loadData() {
    try {
      loading = true;
      
      // Загружаем популярные товары
      const partsResponse = await partsApi.getParts({
        page_size: 8,
        ordering: '-created_at'
      });
      featuredParts = partsResponse.results;
      stats.totalParts = partsResponse.count;

      // Загружаем статистику брендов
      const brandsResponse = await brandsApi.getBrands({
        page_size: 1
      });
      stats.brands = brandsResponse.count;
      
      loading = false;
    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
      loading = false;
    }
  }

  function handleConsultationSubmit(event) {
    event.preventDefault();
    // Пока просто показываем сообщение
    alert('Спасибо! Наш специалист свяжется с вами в ближайшее время.');
    consultationForm = { vin: '', name: '', phone: '' };
  }

  function goToCatalogWithFilter(filter) {
    goto(`/catalog?${filter}=`);
  }

  onMount(() => {
    loadData();
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
<section class="relative bg-gradient-to-br from-dark-500 via-gray-800 to-dark-500 text-white overflow-hidden">
  <!-- Декоративные элементы -->
  <div class="absolute inset-0 bg-black/40"></div>
  <div class="absolute top-0 left-0 w-full h-full">
    <div class="absolute top-20 left-10 w-72 h-72 bg-red-600/10 rounded-full blur-3xl"></div>
    <div class="absolute bottom-20 right-10 w-96 h-96 bg-primary-600/10 rounded-full blur-3xl"></div>
  </div>
  
  <div class="relative container-custom section-padding">
    <div class="max-w-5xl mx-auto text-center">
      <h1 class="text-5xl md:text-7xl font-bold mb-6 leading-tight">
        <span class="bg-gradient-to-r from-white via-white to-gray-300 bg-clip-text text-transparent">
          Автозапчасти
        </span>
        <br>
        <span class="text-white">для вашего автомобиля</span>
      </h1>
      <p class="text-xl md:text-2xl mb-12 text-gray-300 max-w-3xl mx-auto leading-relaxed">
        Широкий выбор оригинальных и совместимых запчастей от ведущих производителей. 
        Быстрая доставка по всей России. Консультации специалистов.
      </p>
      <div class="flex flex-col sm:flex-row gap-6 justify-center items-center">
        <a href="/catalog" class="btn-primary text-lg px-8 py-4 shadow-2xl">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Перейти в каталог
        </a>
        <a href="/about" class="btn-outline border-white text-black hover:bg-white hover:text-dark-500 text-lg px-8 py-4">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          О компании
        </a>
      </div>
    </div>
  </div>
</section>

<!-- Категории товаров -->
<section class="section-padding bg-white">
  <div class="container-custom">
    <h2 class="text-4xl font-bold text-dark-500 mb-12 text-center">Категории запчастей</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <a href="/catalog?brand=" class="card group hover:border-primary-500 transition-all duration-300">
        <div class="p-6 text-center">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-primary-500 group-hover:scale-110 transition-all">
            <svg class="w-8 h-8 text-primary-600 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
            </svg>
          </div>
          <h3 class="font-bold text-dark-500 mb-2">Электроника</h3>
          <p class="text-sm text-gray-600">Датчики, модули, провода</p>
        </div>
      </a>
      
      <a href="/catalog?warehouse=" class="card group hover:border-primary-500 transition-all duration-300">
        <div class="p-6 text-center">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-primary-500 group-hover:scale-110 transition-all">
            <svg class="w-8 h-8 text-primary-600 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
            </svg>
          </div>
          <h3 class="font-bold text-dark-500 mb-2">Двигатель</h3>
          <p class="text-sm text-gray-600">Фильтры, масла, ремни</p>
        </div>
      </a>
      
      <a href="/catalog?brand=" class="card group hover:border-primary-500 transition-all duration-300">
        <div class="p-6 text-center">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-primary-500 group-hover:scale-110 transition-all">
            <svg class="w-8 h-8 text-primary-600 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h3 class="font-bold text-dark-500 mb-2">Подвеска</h3>
          <p class="text-sm text-gray-600">Стойки, амортизаторы, пружины</p>
        </div>
      </a>
      
      <a href="/catalog?warehouse=" class="card group hover:border-primary-500 transition-all duration-300">
        <div class="p-6 text-center">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-primary-500 group-hover:scale-110 transition-all">
            <svg class="w-8 h-8 text-primary-600 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
            </svg>
          </div>
          <h3 class="font-bold text-dark-500 mb-2">Тормоза</h3>
          <p class="text-sm text-gray-600">Колодки, диски, суппорты</p>
        </div>
      </a>
    </div>
  </div>
</section>

<!-- Популярные товары -->
<section class="section-padding bg-gray-50">
  <div class="container-custom">
    <div class="flex items-center justify-between mb-12">
      <div>
        <h2 class="text-4xl font-bold text-dark-500 mb-2">Популярные товары</h2>
        <p class="text-gray-600">Выбирают большинство покупателей</p>
      </div>
      <a href="/catalog" class="btn-outline">
        Смотреть все
        <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </a>
    </div>
    
    {#if loading}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {#each Array(4) as _}
          <div class="card p-6 animate-pulse">
            <div class="aspect-square bg-gray-200 rounded-lg mb-4"></div>
            <div class="h-4 bg-gray-200 rounded mb-2"></div>
            <div class="h-4 bg-gray-200 rounded w-2/3"></div>
          </div>
        {/each}
      </div>
    {:else if featuredParts.length > 0}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {#each featuredParts as part}
          <PartCard {part} />
        {/each}
      </div>
    {/if}
  </div>
</section>

<!-- Онлайн-помощь специалиста -->
<section class="section-padding bg-gradient-to-br from-dark-500 to-gray-800 text-white">
  <div class="container-custom">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold mb-4">Онлайн-помощь специалиста</h2>
        <p class="text-xl text-gray-300">
          Более 10 специалистов прямо сейчас готовы вас проконсультировать
        </p>
        <p class="text-sm text-gray-400 mt-2">
          Примерное время ожидания ответа на Ваш запрос 3-10 минут
        </p>
      </div>

      <form onsubmit={handleConsultationSubmit} class="card bg-white/10 backdrop-blur-sm p-8">
        <div class="mb-6">
          <label for="consultation-vin" class="block text-sm font-medium text-gray-300 mb-2">
            VIN-код вашего автомобиля
          </label>
          <input
            id="consultation-vin"
            type="text"
            bind:value={consultationForm.vin}
            placeholder="Например: WVWZZZ1KZAW123456"
            class="input bg-white/20 border-white/30 text-white placeholder-gray-400 focus:border-white focus:ring-white/50"
            required
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label for="consultation-name" class="block text-sm font-medium text-gray-300 mb-2">
              Ваше имя
            </label>
            <input
              id="consultation-name"
              type="text"
              bind:value={consultationForm.name}
              placeholder="Иван"
              class="input bg-white/20 border-white/30 text-white placeholder-gray-400 focus:border-white focus:ring-white/50"
              required
            />
          </div>
          <div>
            <label for="consultation-phone" class="block text-sm font-medium text-gray-300 mb-2">
              Телефон
            </label>
            <input
              id="consultation-phone"
              type="tel"
              bind:value={consultationForm.phone}
              placeholder="+7 (999) 123-45-67"
              class="input bg-white/20 border-white/30 text-white placeholder-gray-400 focus:border-white focus:ring-white/50"
              required
            />
          </div>
        </div>

        <button type="submit" class="w-full btn-primary bg-red-600 hover:bg-red-700">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          Получить консультацию
        </button>
      </form>
    </div>
  </div>
</section>

<!-- Подбор по автомобилю -->
<section class="section-padding bg-white">
  <div class="container-custom">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-dark-500 mb-4">Подбор по автомобилю</h2>
        <p class="text-xl text-gray-600">
          Найдите запчасти для вашего автомобиля за несколько минут
        </p>
      </div>

      <div class="card p-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="vehicle-year" class="block text-sm font-medium text-dark-500 mb-2">
              Год выпуска
            </label>
            <select id="vehicle-year" class="input">
              <option value="">Выберите год</option>
              {#each Array(30).fill(0).map((_, i) => 2024 - i) as year}
                <option value={year}>{year}</option>
              {/each}
            </select>
          </div>

          <div>
            <label for="vehicle-brand" class="block text-sm font-medium text-dark-500 mb-2">
              Марка
            </label>
            <select id="vehicle-brand" class="input">
              <option value="">Выберите марку</option>
              <option value="audi">Audi</option>
              <option value="bmw">BMW</option>
              <option value="mercedes">Mercedes-Benz</option>
              <option value="volkswagen">Volkswagen</option>
              <option value="toyota">Toyota</option>
              <option value="honda">Honda</option>
            </select>
          </div>

          <div>
            <label for="vehicle-model" class="block text-sm font-medium text-dark-500 mb-2">
              Модель
            </label>
            <select id="vehicle-model" class="input">
              <option value="">Сначала выберите марку</option>
            </select>
          </div>

          <div>
            <label for="vehicle-modification" class="block text-sm font-medium text-dark-500 mb-2">
              Модификация
            </label>
            <select id="vehicle-modification" class="input">
              <option value="">Сначала выберите модель</option>
            </select>
          </div>
        </div>

        <button class="w-full btn-primary mt-6">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Найти запчасти
        </button>
      </div>
    </div>
  </div>
</section>

<!-- Почему выбирают нас -->
<section class="section-padding bg-gradient-to-br from-gray-50 to-white">
  <div class="container-custom">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-dark-500 mb-4">Почему выбирают нас</h2>
        <p class="text-xl text-gray-600">
          Мы работаем, чтобы вы были довольны
        </p>
      </div>

      <!-- Статистика -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
        <div class="card p-8 text-center group hover:border-primary-500 transition-all">
          <div class="w-20 h-20 bg-red-100 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-primary-500 group-hover:scale-110 transition-all">
            <svg class="w-10 h-10 text-primary-600 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <div class="text-5xl font-bold text-primary-600 mb-3">{stats.totalParts.toLocaleString()}</div>
          <h3 class="font-bold text-dark-500 mb-3 text-lg">Товаров в каталоге</h3>
          <p class="text-sm text-gray-600">
            Гарантия качества. Все товары проходят многоуровневую проверку
          </p>
        </div>

        <div class="card p-8 text-center group hover:border-primary-500 transition-all">
          <div class="w-20 h-20 bg-red-100 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-primary-500 group-hover:scale-110 transition-all">
            <svg class="w-10 h-10 text-primary-600 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
          </div>
          <div class="text-5xl font-bold text-primary-600 mb-3">1-3</div>
          <h3 class="font-bold text-dark-500 mb-3 text-lg">Дней доставка</h3>
          <p class="text-sm text-gray-600">
            Быстрая доставка. Доставляем заказы по всей России
          </p>
        </div>

        <div class="card p-8 text-center group hover:border-primary-500 transition-all">
          <div class="w-20 h-20 bg-red-100 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-primary-500 group-hover:scale-110 transition-all">
            <svg class="w-10 h-10 text-primary-600 group-hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <div class="text-5xl font-bold text-primary-600 mb-3">{stats.brands}</div>
          <h3 class="font-bold text-dark-500 mb-3 text-lg">Брендов</h3>
          <p class="text-sm text-gray-600">
            Опытные специалисты. Команда готова помочь с выбором
          </p>
        </div>
      </div>

      <!-- Дополнительные преимущества -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="flex items-start p-6 bg-white rounded-xl border border-gray-200 hover:border-primary-500 transition-all">
          <div class="flex-shrink-0">
            <div class="w-14 h-14 bg-red-100 rounded-xl flex items-center justify-center">
              <svg class="w-7 h-7 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="font-bold text-dark-500 mb-2">Доступные цены</h3>
            <p class="text-sm text-gray-600">Конкурентные цены на весь ассортимент</p>
          </div>
        </div>

        <div class="flex items-start p-6 bg-white rounded-xl border border-gray-200 hover:border-primary-500 transition-all">
          <div class="flex-shrink-0">
            <div class="w-14 h-14 bg-red-100 rounded-xl flex items-center justify-center">
              <svg class="w-7 h-7 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="font-bold text-dark-500 mb-2">Гарантия качества</h3>
            <p class="text-sm text-gray-600">Гарантия качества на все товары</p>
          </div>
        </div>

        <div class="flex items-start p-6 bg-white rounded-xl border border-gray-200 hover:border-primary-500 transition-all">
          <div class="flex-shrink-0">
            <div class="w-14 h-14 bg-red-100 rounded-xl flex items-center justify-center">
              <svg class="w-7 h-7 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="font-bold text-dark-500 mb-2">Быстрая доставка</h3>
            <p class="text-sm text-gray-600">Доставляем в кратчайшие сроки</p>
          </div>
        </div>

        <div class="flex items-start p-6 bg-white rounded-xl border border-gray-200 hover:border-primary-500 transition-all">
          <div class="flex-shrink-0">
            <div class="w-14 h-14 bg-red-100 rounded-xl flex items-center justify-center">
              <svg class="w-7 h-7 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="font-bold text-dark-500 mb-2">Поддержка 24/7</h3>
            <p class="text-sm text-gray-600">Круглосуточная поддержка клиентов</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>