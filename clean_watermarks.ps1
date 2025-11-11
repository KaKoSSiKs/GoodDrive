# PowerShell скрипт для автоматического удаления водяных знаков
# Запуск: .\clean_watermarks.ps1

Write-Host "🧹 Автоматическое удаление водяных знаков с изображений товаров" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

# Переходим в backend
Set-Location -Path "backend"

Write-Host "📦 Шаг 1: Установка зависимостей..." -ForegroundColor Yellow
pip install Pillow numpy requests beautifulsoup4

Write-Host ""
Write-Host "🧹 Шаг 2: Скачивание и очистка изображений..." -ForegroundColor Yellow
Write-Host "Метод: Комбинированный (обрезка + размытие + закрашивание)" -ForegroundColor Cyan
Write-Host ""

# Спрашиваем количество изображений
$limit = Read-Host "Сколько изображений обработать? (Рекомендуется начать с 50)"

if ([string]::IsNullOrWhiteSpace($limit)) {
    $limit = 50
}

Write-Host ""
Write-Host "⏳ Обработка $limit изображений..." -ForegroundColor Yellow
Write-Host "Это может занять несколько минут. Пожалуйста, подождите..." -ForegroundColor Gray
Write-Host ""

# Запускаем команду
python manage.py download_and_clean_images --limit $limit --method all

Write-Host ""
Write-Host "✅ Готово!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Проверьте результаты:" -ForegroundColor Yellow
Write-Host "  1. Админка Django: http://localhost:8000/admin/catalog/partimage/" -ForegroundColor Cyan
Write-Host "  2. Frontend: http://localhost:3000/catalog" -ForegroundColor Cyan
Write-Host "  3. Папка: backend\media\parts\" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Если водяные знаки остались, попробуйте AI метод:" -ForegroundColor Yellow
Write-Host "  pip install opencv-python opencv-contrib-python" -ForegroundColor Gray
Write-Host "  python manage.py ai_remove_watermarks --limit $limit" -ForegroundColor Gray
Write-Host ""

# Возвращаемся назад
Set-Location -Path ".."

# Пауза
Read-Host "Нажмите Enter для выхода..."


