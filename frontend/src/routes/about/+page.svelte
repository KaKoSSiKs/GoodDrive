<script>
  import SeoHead from '$lib/components/SeoHead.svelte';
  import { generateOrganizationJsonLd } from '$lib/utils/seo.js';
  
  // SEO данные
  const seoData = {
    title: 'О компании GoodDrive - Интернет-магазин автозапчастей',
    description: 'GoodDrive - надежный поставщик автозапчастей с 10-летним опытом. Широкий ассортимент, быстрая доставка, гарантия качества.',
    keywords: 'о компании, GoodDrive, автозапчасти, история, команда, гарантии',
    image: '/images/about-og.jpg',
    type: 'website'
  };

  // JSON-LD для организации
  const organizationJsonLd = generateOrganizationJsonLd();
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
<section class="relative bg-gradient-to-br from-primary-500 via-primary-600 to-primary-700 text-white overflow-hidden">
  <div class="absolute inset-0 bg-black/10"></div>
  <div class="absolute top-0 left-0 w-full h-full">
    <div class="absolute top-20 left-10 w-72 h-72 bg-white/10 rounded-full blur-3xl"></div>
    <div class="absolute bottom-20 right-10 w-96 h-96 bg-accent-400/20 rounded-full blur-3xl"></div>
  </div>
  
  <div class="relative container-custom section-padding">
    <div class="max-w-4xl mx-auto text-center">
      <h1 class="text-5xl md:text-7xl font-bold mb-8 animate-fade-in leading-tight">
        <span class="text-gradient bg-gradient-to-r from-white to-primary-100 bg-clip-text text-transparent">
          О компании
        </span>
        <br>
        <span class="text-white">GoodDrive</span>
      </h1>
      <p class="text-xl md:text-2xl mb-12 text-primary-100 animate-slide-up max-w-3xl mx-auto leading-relaxed">
        Ваш надежный партнер в мире автозапчастей уже более 10 лет
      </p>
    </div>
  </div>
</section>

<!-- История компании -->
<section class="section-padding bg-white">
  <div class="container-custom">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-secondary-900 mb-6">Наша история</h2>
        <p class="text-xl text-secondary-600 leading-relaxed">
          GoodDrive начал свою деятельность в 2014 году как небольшой магазин автозапчастей в Москве. 
          Сегодня мы — один из ведущих интернет-магазинов автозапчастей в России.
        </p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <div>
          <h3 class="text-2xl font-bold text-secondary-900 mb-6">От маленького магазина до лидера рынка</h3>
          <div class="space-y-4 text-secondary-600">
            <p>
              Начав с небольшого склада и команды из 5 человек, мы постепенно расширяли ассортимент 
              и улучшали качество обслуживания. Наш успех основан на глубоком понимании потребностей 
              автовладельцев и стремлении предоставить лучший сервис.
            </p>
            <p>
              Сегодня в нашем каталоге более 100,000 наименований автозапчастей от ведущих мировых 
              производителей. Мы работаем с официальными дистрибьюторами и гарантируем подлинность 
              всех товаров.
            </p>
          </div>
        </div>
        <div class="card p-8">
          <div class="grid grid-cols-2 gap-6">
            <div class="text-center">
              <div class="text-3xl font-bold text-primary-600 mb-2">10+</div>
              <div class="text-secondary-600">лет опыта</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-primary-600 mb-2">100K+</div>
              <div class="text-secondary-600">товаров</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-primary-600 mb-2">50K+</div>
              <div class="text-secondary-600">клиентов</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-primary-600 mb-2">24/7</div>
              <div class="text-secondary-600">поддержка</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Наши ценности -->
<section class="section-padding bg-gradient-to-br from-secondary-50 to-white">
  <div class="container-custom">
    <div class="text-center mb-16">
      <h2 class="text-4xl font-bold text-secondary-900 mb-6">Наши ценности</h2>
      <p class="text-xl text-secondary-600 max-w-3xl mx-auto">
        Мы строим долгосрочные отношения с клиентами, основываясь на принципах честности, 
        профессионализма и стремления к совершенству.
      </p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="card p-8 text-center group">
        <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="text-xl font-bold text-secondary-900 mb-4">Качество</h3>
        <p class="text-secondary-600">
          Мы работаем только с проверенными поставщиками и гарантируем подлинность 
          всех автозапчастей в нашем каталоге.
        </p>
      </div>
      
      <div class="card p-8 text-center group">
        <div class="w-16 h-16 bg-gradient-to-br from-accent-500 to-accent-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h3 class="text-xl font-bold text-secondary-900 mb-4">Скорость</h3>
        <p class="text-secondary-600">
          Быстрая обработка заказов и доставка по всей России. Большинство заказов 
          отправляются в день оформления.
        </p>
      </div>
      
      <div class="card p-8 text-center group">
        <div class="w-16 h-16 bg-gradient-to-br from-success-500 to-success-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </div>
        <h3 class="text-xl font-bold text-secondary-900 mb-4">Забота о клиентах</h3>
        <p class="text-secondary-600">
          Наша команда экспертов всегда готова помочь с выбором запчастей 
          и ответить на любые вопросы.
        </p>
      </div>
    </div>
  </div>
</section>

<!-- Команда -->
<section class="section-padding bg-white">
  <div class="container-custom">
    <div class="text-center mb-16">
      <h2 class="text-4xl font-bold text-secondary-900 mb-6">Наша команда</h2>
      <p class="text-xl text-secondary-600 max-w-3xl mx-auto">
        Профессиональная команда экспертов, которые знают все об автозапчастях 
        и готовы помочь вам с выбором.
      </p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="card p-8 text-center group">
        <div class="w-24 h-24 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
          <span class="text-2xl font-bold text-white">АС</span>
        </div>
        <h3 class="text-xl font-bold text-secondary-900 mb-2">Алексей Смирнов</h3>
        <p class="text-primary-600 font-medium mb-4">Генеральный директор</p>
        <p class="text-secondary-600">
          15 лет опыта в автомобильной индустрии. Эксперт по подбору автозапчастей 
          для европейских и японских автомобилей.
        </p>
      </div>
      
      <div class="card p-8 text-center group">
        <div class="w-24 h-24 bg-gradient-to-br from-accent-500 to-accent-600 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
          <span class="text-2xl font-bold text-white">МП</span>
        </div>
        <h3 class="text-xl font-bold text-secondary-900 mb-2">Мария Петрова</h3>
        <p class="text-primary-600 font-medium mb-4">Руководитель отдела качества</p>
        <p class="text-secondary-600">
          Отвечает за контроль качества всех поступающих автозапчастей. 
          Сертифицированный специалист по автомобильным системам.
        </p>
      </div>
      
      <div class="card p-8 text-center group">
        <div class="w-24 h-24 bg-gradient-to-br from-success-500 to-success-600 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
          <span class="text-2xl font-bold text-white">ДК</span>
        </div>
        <h3 class="text-xl font-bold text-secondary-900 mb-2">Дмитрий Козлов</h3>
        <p class="text-primary-600 font-medium mb-4">Технический консультант</p>
        <p class="text-secondary-600">
          Помогает клиентам с техническими вопросами и подбором совместимых 
          автозапчастей. 12 лет в автомобильной сфере.
        </p>
      </div>
    </div>
  </div>
</section>

<!-- Контакты -->
<section class="section-padding bg-gradient-to-br from-primary-500 to-primary-700 text-white">
  <div class="container-custom">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-4xl font-bold mb-8">Свяжитесь с нами</h2>
      <p class="text-xl text-primary-100 mb-12">
        Есть вопросы? Наша команда готова помочь вам с выбором автозапчастей
      </p>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="card glass p-6">
          <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
          </div>
          <h3 class="text-lg font-bold mb-2">Телефон</h3>
          <p class="text-primary-100">+7 (800) 555-35-35</p>
        </div>
        
        <div class="card glass p-6">
          <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-bold mb-2">Email</h3>
          <p class="text-primary-100">info@gooddrive.ru</p>
        </div>
        
        <div class="card glass p-6">
          <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-bold mb-2">Адрес</h3>
          <p class="text-primary-100">Москва, ул. Автозаводская, 23</p>
        </div>
      </div>
    </div>
  </div>
</section>
