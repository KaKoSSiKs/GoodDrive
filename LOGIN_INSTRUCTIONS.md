# 🔐 Вход в админ-панель

## ✅ Проблема решена!

Теперь вы можете войти в админ-панель с учетными данными:

**Логин:** `admin`  
**Пароль:** `12345678`

---

## 🌐 URL для входа

**Через frontend:** http://localhost:3000/admin

**Напрямую Django admin:** http://localhost:8000/admin

---

## 📋 Что было сделано

1. ✅ Добавлен `python-decouple` в `requirements.txt`
2. ✅ Пересобран Docker контейнер backend
3. ✅ Запущен backend сервер (Django)
4. ✅ Применены миграции базы данных
5. ✅ Создан суперпользователь `admin` с паролем `12345678`

---

## 🚀 Как запустить проект в следующий раз

### Запуск всех сервисов:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### Проверка статуса:

```bash
docker-compose -f docker-compose.dev.yml ps
```

### Остановка:

```bash
docker-compose -f docker-compose.dev.yml down
```

---

## 🔍 Проверка доступности

### Backend API:

```bash
# PowerShell
Invoke-WebRequest -Uri "http://localhost:8000/api/" -UseBasicParsing
```

### Frontend:

Откройте: http://localhost:3000

### Админ-панель:

Откройте: http://localhost:3000/admin или http://localhost:8000/admin

---

## 🛠️ Если возникнут проблемы

### Backend не отвечает:

```bash
# Проверьте логи
docker-compose -f docker-compose.dev.yml logs backend

# Перезапустите backend
docker-compose -f docker-compose.dev.yml restart backend
```

### Frontend не подключается к backend:

Убедитесь, что backend запущен:
```bash
docker-compose -f docker-compose.dev.yml ps
```

### Забыли пароль:

```bash
# Создайте нового администратора
docker-compose -f docker-compose.dev.yml exec backend python manage.py shell -c "from django.contrib.auth.models import User; user = User.objects.get(username='admin'); user.set_password('12345678'); user.save(); print('Пароль обновлен!')"
```

---

## 📊 Запущенные сервисы

После запуска `docker-compose up` будут работать:

| Сервис | Порт | URL |
|--------|------|-----|
| Frontend (SvelteKit) | 3000 | http://localhost:3000 |
| Backend (Django) | 8000 | http://localhost:8000 |
| PostgreSQL | 5432 | localhost:5432 |

---

## ✅ Готово!

Теперь вы можете:

1. Открыть http://localhost:3000/admin
2. Ввести логин: `admin`
3. Ввести пароль: `12345678`
4. Нажать "Войти"

**Удачи!** 🚀

