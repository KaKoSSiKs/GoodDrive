<script>
  // Импортируем глобальные стили с Tailwind CSS
  import '../app.css';
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';
  
  // Получаем children snippet в Svelte 5
  let { children } = $props();
</script>

<div class="min-h-screen flex flex-col">
  <Header />
  
  <main class="flex-1">
    {@render children()}
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

