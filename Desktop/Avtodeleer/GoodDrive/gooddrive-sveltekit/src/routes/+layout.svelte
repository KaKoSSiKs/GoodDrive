<script>
  // Импортируем глобальные стили с Tailwind CSS
  import '../app.css';
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import { page } from '$app/stores';
  
  // Получаем children snippet в Svelte 5
  let { children } = $props();
  
  // Проверяем, находимся ли мы в админ-панели
  const isAdminRoute = $derived($page.url.pathname.startsWith('/admin'));
</script>

{#if isAdminRoute}
  <!-- Админ-панель без основного header/footer -->
  {@render children()}
{:else}
  <!-- Обычный сайт с header/footer -->
  <div class="min-h-screen flex flex-col">
    <Header />
    
    <main class="flex-1">
      {@render children()}
    </main>
    
    <Footer />
  </div>
{/if}

<style>
  :global(html) {
    scroll-behavior: smooth;
  }
  
  :global(body) {
    font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
  }
</style>

