<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { partsApi, brandsApi, cartUtils } from '$lib/utils/api.js';
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
  let heroImageFailed = $state(false);
  
  function handleAddToCart(event) {
    const { part } = event.detail;
    cartUtils.addToCart(part);
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
    notification.textContent = `Добавлено в корзину: ${part.title}`;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
  }

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
<section class="relative bg-gradient-to-br from-dark-800 via-dark-900 to-black text-white overflow-hidden" style="min-height: 70vh;">
  <!-- Декоративные элементы -->
  {#if !heroImageFailed}
    <img
      src="/images/img_car.jpg"
      alt="Быстрая доставка автозапчастей"
      class="absolute inset-0 w-full h-full object-cover object-center opacity-30"
      onerror={() => heroImageFailed = true}
    />
  {/if}
  <div class="absolute inset-0 bg-gradient-to-br from-primary-900/60 via-brand-900/40 to-black/60"></div>
  <div class="absolute top-0 left-0 w-full h-full">
    <div class="absolute top-20 left-10 w-72 h-72 bg-primary-500/20 rounded-full blur-3xl"></div>
    <div class="absolute bottom-20 right-10 w-96 h-96 bg-brand-600/20 rounded-full blur-3xl"></div>
  </div>
  
  <div class="relative container-custom py-20 lg:py-28">
    <div class="max-w-5xl mx-auto text-center">
      <h1 class="text-5xl md:text-7xl font-bold mb-6 leading-tight">
        <span class="bg-gradient-to-r from-primary-200 via-primary-100 to-white bg-clip-text text-transparent">
          Автозапчасти
        </span>
        <br>
        <span class="text-white drop-shadow-lg">для вашего автомобиля</span>
      </h1>
      <p class="text-xl md:text-2xl mb-12 text-gray-200 max-w-3xl mx-auto leading-relaxed">
        Широкий выбор оригинальных и совместимых запчастей от ведущих производителей. 
        Быстрая доставка по всей России. Консультации специалистов.
      </p>
      <div class="flex flex-col sm:flex-row gap-6 justify-center items-center">
        <a href="/catalog" class="btn-primary text-lg px-10 py-4 shadow-2xl">
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Перейти в каталог
        </a>
        <a href="/#contacts" class="btn-outline text-lg px-10 py-4 shadow-xl border-white/30 text-white hover:bg-white/10">
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
          Связаться с нами
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
      <a href="/catalog?search=датчик%20модуль%20электроника" class="card group hover:border-primary-500 hover:shadow-xl transition-all duration-300">
        <div class="p-6 text-center">
          <div class="w-20 h-20 bg-primary-50 rounded-2xl flex items-center justify-center mx-auto mb-4 overflow-hidden group-hover:bg-primary-600 group-hover:scale-110 transition-all shadow-md">
            <img src="/icons/electronics_ic.png" alt="Электроника" class="w-12 h-12 object-contain icon-primary" />
          </div>
          <h3 class="font-bold text-dark-800 mb-2 text-lg">Электроника</h3>
          <p class="text-sm text-gray-600">Датчики, модули, провода</p>
        </div>
      </a>
      
      <a href="/catalog?search=двигатель%20фильтр%20масло%20ремень" class="card group hover:border-primary-500 hover:shadow-xl transition-all duration-300">
        <div class="p-6 text-center">
          <div class="w-20 h-20 bg-primary-50 rounded-2xl flex items-center justify-center mx-auto mb-4 overflow-hidden group-hover:bg-primary-600 group-hover:scale-110 transition-all shadow-md">
            <img src="/icons/engine_ic.png" alt="Двигатель" class="w-12 h-12 object-contain icon-primary" />
          </div>
          <h3 class="font-bold text-dark-800 mb-2 text-lg">Двигатель</h3>
          <p class="text-sm text-gray-600">Фильтры, масла, ремни</p>
        </div>
      </a>
      
      <a href="/catalog?search=подвеска%20стойка%20амортизатор" class="card group hover:border-primary-500 hover:shadow-xl transition-all duration-300">
        <div class="p-6 text-center">
          <div class="w-20 h-20 bg-primary-50 rounded-2xl flex items-center justify-center mx-auto mb-4 overflow-hidden group-hover:bg-primary-600 group-hover:scale-110 transition-all shadow-md">
            <img src="/icons/suspension_ic.png" alt="Подвеска" class="w-12 h-12 object-contain icon-primary" />
          </div>
          <h3 class="font-bold text-dark-800 mb-2 text-lg">Подвеска</h3>
          <p class="text-sm text-gray-600">Стойки, амортизаторы, пружины</p>
        </div>
      </a>
      
      <a href="/catalog?search=тормоз%20колодки%20диск" class="card group hover:border-primary-500 hover:shadow-xl transition-all duration-300">
        <div class="p-6 text-center">
          <div class="w-20 h-20 bg-primary-50 rounded-2xl flex items-center justify-center mx-auto mb-4 overflow-hidden group-hover:bg-primary-600 group-hover:scale-110 transition-all shadow-md">
            <img src="/icons/brake_ic.png" alt="Тормоза" class="w-12 h-12 object-contain icon-primary" />
          </div>
          <h3 class="font-bold text-dark-800 mb-2 text-lg">Тормоза</h3>
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
          <PartCard {part} on:addToCart={handleAddToCart} />
        {/each}
      </div>
    {/if}
  </div>
</section>

<!-- Онлайн-помощь специалиста -->
<section class="section-padding bg-gradient-to-br from-brand-800 via-primary-800 to-brand-900 text-white">
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

        <button type="submit" class="w-full btn-primary">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          Получить консультацию
        </button>
      </form>
    </div>
  </div>
</section>

<!-- Контакты и карта -->
<section id="contacts" class="section-padding bg-white">
  <div class="container-custom">
    <div class="text-center mb-12">
      <h2 class="text-4xl font-bold text-dark-500 mb-4">Контакты</h2>
      <p class="text-xl text-gray-600">Приезжайте к нам или свяжитесь удобным способом</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Информация о контактах -->
      <div class="space-y-6">
        <div class="card p-6">
          <div class="flex items-start space-x-4">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-bold text-dark-500 mb-2">Адрес магазина</h3>
              <p class="text-gray-600">г. Челябинск</p>
              <p class="text-gray-600">ул. Артиллерийская, дом 15, корпус 2</p>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-start space-x-4">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
              </div>
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-bold text-dark-500 mb-2">Телефон</h3>
              <a href="tel:+79227081553" class="text-primary-600 hover:text-primary-700 font-medium">+7 (922) 708-15-53</a>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-start space-x-4">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-bold text-dark-500 mb-2">Время работы</h3>
              <p class="text-gray-600">Пн-Пт: 09:00 - 18:00</p>
              <p class="text-gray-600">Сб: 10:00 - 16:00</p>
              <p class="text-red-600 font-medium">Вс: Выходной</p>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-start space-x-4">
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-bold text-dark-500 mb-2">Email</h3>
              <a href="mailto:89227081553@mail.ru" class="text-primary-600 hover:text-primary-700 font-medium">89227081553@mail.ru</a>
            </div>
          </div>
        </div>
      </div>

      <!-- Яндекс карта -->
      <div class="card overflow-hidden h-[600px]">
        <div style="position:relative;overflow:hidden;height:100%;">
          <iframe 
            src="https://yandex.ru/map-widget/v1/?ll=61.424401%2C55.187617&z=17&l=map&pt=61.424401,55.187617,pm2rdm" 
            width="100%" 
            height="100%" 
            frameborder="0" 
            allowfullscreen="true" 
            style="position:relative;"
            title="Карта расположения магазина GoodDrive"
          ></iframe>
        </div>
      </div>
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
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="card p-8 text-center group hover:border-primary-500 hover:shadow-2xl transition-all">
          <div class="w-20 h-20 bg-primary-50 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-primary-600 group-hover:scale-110 transition-all shadow-md">
            <svg class="w-10 h-10 text-primary-600 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="font-bold text-dark-800 mb-3 text-2xl">Доступные цены</h3>
          <p class="text-gray-600">
            Конкурентные цены на весь ассортимент. Работаем напрямую с поставщиками
          </p>
        </div>

        <div class="card p-8 text-center group hover:border-primary-500 hover:shadow-2xl transition-all">
          <div class="w-20 h-20 bg-primary-50 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-primary-600 group-hover:scale-110 transition-all shadow-md">
            <svg class="w-10 h-10 text-primary-600 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="font-bold text-dark-800 mb-3 text-2xl">Быстрая доставка</h3>
          <p class="text-gray-600">
            Доставляем заказы в кратчайшие сроки по всей России
          </p>
        </div>

        <div class="card p-8 text-center group hover:border-primary-500 hover:shadow-2xl transition-all">
          <div class="w-20 h-20 bg-primary-50 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:bg-primary-600 group-hover:scale-110 transition-all shadow-md">
            <svg class="w-10 h-10 text-primary-600 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 class="font-bold text-dark-800 mb-3 text-2xl">Гарантия качества</h3>
          <p class="text-gray-600">
            Все товары сертифицированы и проходят проверку качества
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Отзывы клиентов с Яндекс.Карт -->
<section class="section-padding bg-gray-50">
  <div class="container-custom">
    <div class="text-center mb-12">
      <h2 class="text-4xl font-bold text-dark-500 mb-4">Отзывы наших клиентов</h2>
      <p class="text-xl text-gray-600">
        Нам доверяют тысячи автовладельцев
      </p>
    </div>

    <!-- Виджет отзывов Яндекс.Карт -->
    <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
      <div style="min-height:500px;">
        <iframe 
          src="https://yandex.ru/maps-reviews-widget/229678936575?comments" 
          style="width:100%;height:600px;border:none;display:block;"
          title="Отзывы клиентов на Яндекс.Картах"
        ></iframe>
      </div>
      <div class="p-6 bg-gray-50 border-t border-gray-200">
        <div class="flex flex-col md:flex-row items-center justify-between gap-4">
          <p class="text-gray-600 flex items-center justify-center">
            <svg class="w-5 h-5 mr-2 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            Реальные отзывы с Яндекс.Карт
          </p>
          <a 
            href="https://yandex.ru/maps/56/chelyabinsk/?ll=61.424521%2C55.187700&mode=poi&poi%5Bpoint%5D=61.424401%2C55.187617&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D229678936575&tab=reviews&z=20" 
            target="_blank" 
            rel="noopener noreferrer"
            class="btn-outline text-sm flex items-center"
          >
            Посмотреть все отзывы
            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>
        </div>
      </div>
    </div>

    <!-- Призыв к действию -->
    <div class="mt-8 text-center">
      <p class="text-gray-600 mb-4 text-lg">Оставьте свой отзыв о нашей работе</p>
      <a 
        href="https://yandex.ru/maps/56/chelyabinsk/?ll=61.424521%2C55.187700&mode=poi&poi%5Bpoint%5D=61.424401%2C55.187617&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D229678936575&tab=reviews&z=20" 
        target="_blank" 
        rel="noopener noreferrer"
        class="btn-primary inline-flex items-center justify-center"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
        Написать отзыв
      </a>
    </div>
  </div>
</section>