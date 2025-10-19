<script>
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import { page } from '$app/stores';
  
  // Реактивное состояние для SEO
  let seoData = $state({
    title: 'GoodDrive - Интернет-магазин автозапчастей',
    description: 'Широкий выбор автозапчастей от ведущих производителей. Быстрая доставка по всей России.',
    keywords: 'автозапчасти, запчасти для авто, интернет-магазин, доставка'
  });
  
  // Производное значение для определения текущей страницы
  const currentPage = $derived(page.url.pathname);
  
  // Функция для обновления SEO данных
  async function updateSEO(slug) {
    try {
      const response = await fetch(`/api/seo/meta/${slug}/`);
      if (response.ok) {
        const data = await response.json();
        seoData = data;
      }
    } catch (error) {
      console.error('Ошибка загрузки SEO данных:', error);
    }
  }
  
  // Обновляем SEO при изменении страницы
  $effect(() => {
    const slug = currentPage === '/' ? 'home' : currentPage.slice(1).split('/')[0];
    updateSEO(slug);
  });
</script>

<svelte:head>
  <title>{seoData.title}</title>
  <meta name="description" content={seoData.description} />
  <meta name="keywords" content={seoData.keywords} />
  
  <!-- Open Graph -->
  <meta property="og:title" content={seoData.og_title || seoData.title} />
  <meta property="og:description" content={seoData.og_description || seoData.description} />
  <meta property="og:type" content="website" />
  <meta property="og:url" content={page.url.href} />
  {#if seoData.og_image_url}
    <meta property="og:image" content={seoData.og_image_url} />
  {/if}
  
  <!-- Canonical URL -->
  {#if seoData.canonical_url}
    <link rel="canonical" href={seoData.canonical_url} />
  {/if}
  
  <!-- Robots -->
  <meta name="robots" content={seoData.robots || 'index, follow'} />
  
  <!-- Яндекс.Вебмастер -->
  {#if seoData.yandex_verification}
    <meta name="yandex-verification" content={seoData.yandex_verification} />
  {/if}
</svelte:head>

<div class="min-h-screen flex flex-col">
  <Header />
  
  <main class="flex-1">
    <slot />
  </main>
  
  <Footer />
</div>

<style>
  :global(html) {
    scroll-behavior: smooth;
  }
  
  :global(body) {
    font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
  }
</style>

