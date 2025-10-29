# Скрипт для импорта данных
Write-Host "=== Импорт данных в GoodDrive ===" -ForegroundColor Cyan

# Проверяем наличие CSV файла
if (-not (Test-Path "parts.csv")) {
    Write-Host "ОШИБКА: Файл parts.csv не найден!" -ForegroundColor Red
    Write-Host "Создайте CSV файл из Excel и поместите в корень проекта" -ForegroundColor Yellow
    exit 1
}

Write-Host "Файл найден, начинаем импорт..." -ForegroundColor Green

# Импорт первых 100 запчастей
docker-compose -f docker-compose.dev.yml exec backend python manage.py import_from_csv parts.csv --limit 100

Write-Host "`nИмпорт завершен!" -ForegroundColor Green
Write-Host "Проверьте данные: http://localhost:8000/api/catalog/parts/" -ForegroundColor Cyan

