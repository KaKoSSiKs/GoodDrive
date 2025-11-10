"""
Модуль для авторизации администраторов
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import jwt
from django.conf import settings


# Секретный ключ для JWT (в продакшене использовать из .env)
JWT_SECRET = getattr(settings, 'SECRET_KEY', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """
    Авторизация администратора
    
    POST /api/admin/login/
    {
        "username": "admin",
        "password": "password"
    }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Введите логин и пароль'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Аутентификация через Django
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Неверный логин или пароль'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Проверяем, что пользователь - администратор
    if not user.is_staff:
        return Response(
            {'error': 'Доступ запрещён. Требуются права администратора'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Генерируем JWT токен
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'is_superuser': user.is_superuser,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return Response({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_superuser': user.is_superuser
        }
    })


@api_view(['POST'])
def admin_verify(request):
    """
    Проверка токена администратора
    
    POST /api/admin/verify/
    Headers: Authorization: Bearer <token>
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return Response(
            {'error': 'Токен не предоставлен'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Проверяем существование пользователя
        try:
            user = User.objects.get(id=payload['user_id'])
            if not user.is_staff:
                return Response(
                    {'error': 'Доступ запрещён'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return Response({
                'valid': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_superuser': user.is_superuser
                }
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    except jwt.ExpiredSignatureError:
        return Response(
            {'error': 'Токен истёк'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        return Response(
            {'error': 'Неверный токен'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
def admin_logout(request):
    """
    Выход администратора (на клиенте удаляем токен)
    """
    return Response({'message': 'Выход выполнен успешно'})

