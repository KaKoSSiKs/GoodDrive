<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { 
    generateMetaTags, 
    generatePageTitle, 
    generatePageDescription, 
    generateKeywords,
    generateCanonicalUrl 
  } from '$lib/utils/seo.js';
  
  // Пропсы компонента
  export let title = '';
  export let description = '';
  export let keywords = '';
  export let image = '';
  export let type = 'website';
  export let product = null;
  export let breadcrumbs = [];
  export let jsonLd = null;
  
  // Реактивное состояние
  let metaTags = $state([]);
  let canonicalUrl = $state('');
  
  // Производные значения
  const pageTitle = $derived(generatePageTitle(title));
  const pageDescription = $derived(description || generatePageDescription(type, { product }));
  const pageKeywords = $derived(keywords || generateKeywords(type, { product }));
  
  // Обновление метатегов
  function updateMetaTags() {
    const baseUrl = 'https://gooddrive.com'; // В продакшене должен быть из переменных окружения
    const currentUrl = `${baseUrl}${page.url.pathname}`;
    
    canonicalUrl = generateCanonicalUrl(baseUrl, page.url.pathname);
    
    metaTags = generateMetaTags({
      title: pageTitle,
      description: pageDescription,
      keywords: pageKeywords,
      image: image,
      url: currentUrl,
      type: type,
      product: product
    });
  }
  
  // Инициализация
  onMount(() => {
    updateMetaTags();
  });
  
  // Обновление при изменении пропсов
  $effect(() => {
    updateMetaTags();
  });
</script>

<svelte:head>
  <!-- Основные метатеги -->
  <title>{pageTitle}</title>
  <meta name="description" content={pageDescription} />
  <meta name="keywords" content={pageKeywords} />
  
  <!-- Канонический URL -->
  <link rel="canonical" href={canonicalUrl} />
  
  <!-- Динамические метатеги -->
  {#each metaTags as tag}
    {#if tag.property}
      <meta property={tag.property} content={tag.content} />
    {:else if tag.name}
      <meta name={tag.name} content={tag.content} />
    {/if}
  {/each}
  
  <!-- Дополнительные метатеги -->
  <meta name="robots" content="index, follow" />
  <meta name="author" content="GoodDrive" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  
  <!-- Favicon -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
  
  <!-- JSON-LD структурированные данные -->
  {#if jsonLd}
    {@html `<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>`}
  {/if}
  
  <!-- Хлебные крошки JSON-LD -->
  {#if breadcrumbs.length > 0}
    {@html `<script type="application/ld+json">${JSON.stringify({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": breadcrumbs.map((crumb, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "name": crumb.name,
        "item": crumb.url
      }))
    })}</script>`}
  {/if}
</svelte:head>

