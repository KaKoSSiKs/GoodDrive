from django.contrib.auth.models import User

# Удаляем существующего админа если есть
User.objects.filter(username='admin').delete()

# Создаем нового суперпользователя
user = User.objects.create_superuser('admin', 'admin@gooddrive.com', '12345678')

print('✅ Администратор создан!')
print('   Логин: admin')
print('   Пароль: 12345678')

