# 🚀 Быстрый старт GoodDrive

## ✅ Проблема решена!

Backend и админ-панель теперь работают!

---

## 🔐 Данные для входа в админ-панель

**Логин:** `admin`  
**Пароль:** `12345678`

**URL:** http://localhost:3000/admin

---

## 🚀 Запуск проекта

### Простой способ (все сервисы сразу):

```powershell
docker-compose -f docker-compose.dev.yml up -d
```

### После запуска откройте:

- **Сайт:** http://localhost:3000
- **Админ-панель:** http://localhost:3000/admin
- **Django API:** http://localhost:8000/api
- **Django Admin:** http://localhost:8000/admin

---

## 📊 Проверка статуса

```powershell
docker-compose -f docker-compose.dev.yml ps
```

**Должны работать:**
- ✅ gooddrive-backend-1
- ✅ gooddrive-frontend-1
- ✅ gooddrive-db-1

---

## 🛑 Остановка проекта

```powershell
docker-compose -f docker-compose.dev.yml down
```

---

## 🔧 Что было исправлено

1. ✅ Добавлен недостающий модуль `python-decouple`
2. ✅ Пересобран Docker контейнер
3. ✅ Создан администратор с логином `admin` и паролем `12345678`
4. ✅ Запущен backend сервер на порту 8000

---

## 📝 Полезные команды

### Просмотр логов:

```powershell
# Все сервисы
docker-compose -f docker-compose.dev.yml logs

# Только backend
docker-compose -f docker-compose.dev.yml logs backend

# Только frontend
docker-compose -f docker-compose.dev.yml logs frontend

# С отслеживанием (live)
docker-compose -f docker-compose.dev.yml logs -f backend
```

### Перезапуск сервиса:

```powershell
docker-compose -f docker-compose.dev.yml restart backend
docker-compose -f docker-compose.dev.yml restart frontend
```

### Пересборка и запуск:

```powershell
docker-compose -f docker-compose.dev.yml up -d --build
```

---

## 🎯 Следующие шаги

1. ✅ Откройте http://localhost:3000
2. ✅ Перейдите в админ-панель: http://localhost:3000/admin
3. ✅ Войдите с логином `admin` и паролем `12345678`
4. ✅ Начните работать с каталогом и заказами!

---

**Готово! Проект запущен и готов к использованию!** 🎉

