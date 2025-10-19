<script>
  // Пропсы компонента
  export let min = 0;
  export let max = 100000;
  export let step = 100;
  export let value = { min: min, max: max };
  export let onInput = () => {};
  export let disabled = false;
  
  // Реактивное состояние
  let minValue = $state(value.min);
  let maxValue = $state(value.max);
  let isDragging = $state(false);
  
  // Производные значения
  const range = $derived(max - min);
  const minPercent = $derived(((minValue - min) / range) * 100);
  const maxPercent = $derived(((maxValue - min) / range) * 100);
  
  // Обработчики
  function handleMinInput(event) {
    const newValue = Math.min(Number(event.target.value), maxValue - step);
    minValue = Math.max(min, newValue);
    updateValue();
  }
  
  function handleMaxInput(event) {
    const newValue = Math.max(Number(event.target.value), minValue + step);
    maxValue = Math.min(max, newValue);
    updateValue();
  }
  
  function handleMinMouseDown() {
    isDragging = true;
  }
  
  function handleMaxMouseDown() {
    isDragging = true;
  }
  
  function handleMouseMove(event) {
    if (!isDragging) return;
    
    const rect = event.currentTarget.getBoundingClientRect();
    const percent = ((event.clientX - rect.left) / rect.width) * 100;
    const newValue = min + (percent / 100) * range;
    
    if (event.target.classList.contains('min-slider')) {
      minValue = Math.max(min, Math.min(newValue, maxValue - step));
    } else {
      maxValue = Math.min(max, Math.max(newValue, minValue + step));
    }
    
    updateValue();
  }
  
  function handleMouseUp() {
    isDragging = false;
  }
  
  function updateValue() {
    const newValue = { min: minValue, max: maxValue };
    onInput(newValue);
  }
  
  function resetRange() {
    minValue = min;
    maxValue = max;
    updateValue();
  }
  
  // Форматирование значения для отображения
  function formatValue(val) {
    return new Intl.NumberFormat('ru-RU').format(val);
  }
</script>

<div class="w-full">
  <!-- Заголовок и сброс -->
  <div class="flex items-center justify-between mb-4">
    <label class="text-sm font-medium text-neutral-700">Цена, ₽</label>
    {#if minValue !== min || maxValue !== max}
      <button
        on:click={resetRange}
        class="text-xs text-primary-500 hover:text-primary-600 font-medium"
        disabled={disabled}
      >
        Сбросить
      </button>
    {/if}
  </div>
  
  <!-- Слайдер -->
  <div class="relative">
    <!-- Трек -->
    <div class="relative h-2 bg-neutral-200 rounded-lg">
      <!-- Активный диапазон -->
      <div 
        class="absolute h-2 bg-primary-500 rounded-lg"
        style="left: {minPercent}%; width: {maxPercent - minPercent}%;"
      ></div>
      
      <!-- Минимальный слайдер -->
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        bind:value={minValue}
        on:input={handleMinInput}
        on:mousedown={handleMinMouseDown}
        on:mousemove={handleMouseMove}
        on:mouseup={handleMouseUp}
        class="absolute w-full h-2 bg-transparent appearance-none cursor-pointer min-slider"
        style="z-index: 2;"
        disabled={disabled}
      />
      
      <!-- Максимальный слайдер -->
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        bind:value={maxValue}
        on:input={handleMaxInput}
        on:mousedown={handleMaxMouseDown}
        on:mousemove={handleMouseMove}
        on:mouseup={handleMouseUp}
        class="absolute w-full h-2 bg-transparent appearance-none cursor-pointer max-slider"
        style="z-index: 2;"
        disabled={disabled}
      />
      
      <!-- Кастомные ползунки -->
      <div 
        class="absolute w-4 h-4 bg-white border-2 border-primary-500 rounded-full shadow-md transform -translate-y-1 cursor-pointer"
        style="left: {minPercent}%; z-index: 3;"
        on:mousedown={handleMinMouseDown}
      ></div>
      
      <div 
        class="absolute w-4 h-4 bg-white border-2 border-primary-500 rounded-full shadow-md transform -translate-y-1 cursor-pointer"
        style="left: {maxPercent}%; z-index: 3;"
        on:mousedown={handleMaxMouseDown}
      ></div>
    </div>
  </div>
  
  <!-- Поля ввода -->
  <div class="flex items-center space-x-2 mt-4">
    <div class="flex-1">
      <label class="block text-xs text-neutral-500 mb-1">От</label>
      <input
        type="number"
        min={min}
        max={max}
        step={step}
        bind:value={minValue}
        on:input={handleMinInput}
        class="input text-sm py-1 px-2"
        disabled={disabled}
      />
    </div>
    
    <div class="flex-1">
      <label class="block text-xs text-neutral-500 mb-1">До</label>
      <input
        type="number"
        min={min}
        max={max}
        step={step}
        bind:value={maxValue}
        on:input={handleMaxInput}
        class="input text-sm py-1 px-2"
        disabled={disabled}
      />
    </div>
  </div>
  
  <!-- Отображение диапазона -->
  <div class="text-center mt-2 text-sm text-neutral-600">
    {formatValue(minValue)} - {formatValue(maxValue)} ₽
  </div>
</div>

<style>
  /* Скрываем стандартные ползунки */
  input[type="range"] {
    -webkit-appearance: none;
    appearance: none;
  }
  
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 0;
    height: 0;
    background: transparent;
  }
  
  input[type="range"]::-moz-range-thumb {
    width: 0;
    height: 0;
    background: transparent;
    border: none;
  }
  
  /* Стили для отключенного состояния */
  input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>

