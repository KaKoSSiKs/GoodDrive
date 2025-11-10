#!/usr/bin/env python
"""Создание стандартных категорий расходов"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gooddrive_backend.settings')
django.setup()

from finance.models import ExpenseCategory

categories = [
    {'name': 'Зарплата', 'description': 'Заработная плата сотрудников'},
    {'name': 'Аренда', 'description': 'Аренда помещений'},
    {'name': 'Коммунальные услуги', 'description': 'Электричество, вода, отопление'},
    {'name': 'Транспорт и доставка', 'description': 'Расходы на доставку и транспорт'},
    {'name': 'Реклама и маркетинг', 'description': 'Рекламные расходы'},
    {'name': 'Налоги и сборы', 'description': 'Налоговые платежи'},
    {'name': 'Офисные расходы', 'description': 'Канцелярия, мебель и прочее'},
    {'name': 'Ремонт и обслуживание', 'description': 'Ремонтные работы'},
    {'name': 'Закупка товаров', 'description': 'Закупка автозапчастей у поставщиков'},
    {'name': 'Прочие расходы', 'description': 'Другие операционные расходы'},
]

print('Создание категорий расходов...')
for cat_data in categories:
    category, created = ExpenseCategory.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        print(f'  ✓ Создана: {category.name}')
    else:
        print(f'  - Уже существует: {category.name}')

print(f'\nГотово! Всего категорий: {ExpenseCategory.objects.count()}')

