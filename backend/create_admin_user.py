#!/usr/bin/env python
"""Создание администратора и настроек уведомлений"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gooddrive_backend.settings')
django.setup()

from django.contrib.auth.models import User
from notifications.models import NotificationSettings

# Создаём/обновляем пользователя
user, created = User.objects.get_or_create(
    id=1,
    defaults={
        'username': 'admin',
        'email': '89227081553@mail.ru',
        'is_staff': True,
        'is_superuser': True
    }
)

if created:
    user.set_password('admin')
    user.save()
    print(f'✓ Создан пользователь: {user.username}')
else:
    print(f'✓ Пользователь уже существует: {user.username}')

# Создаём настройки уведомлений
settings, settings_created = NotificationSettings.objects.get_or_create(
    user=user,
    defaults={'notification_email': '89227081553@mail.ru'}
)

if settings_created:
    print(f'✓ Созданы настройки уведомлений для {user.username}')
else:
    print(f'✓ Настройки уведомлений уже существуют')

print('\nГотово!')

