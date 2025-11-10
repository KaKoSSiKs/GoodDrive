from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Order
import io


@api_view(['GET'])
@permission_classes([AllowAny])
def print_invoice(request, order_id):
    """Печать накладной"""
    try:
        order = Order.objects.prefetch_related('items__part').get(id=order_id)
        
        # HTML для печати
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Накладная №{order.order_number}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #333; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .header {{ margin-bottom: 30px; }}
                .total {{ font-weight: bold; font-size: 18px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Накладная №{order.order_number}</h1>
                <p>Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}</p>
                <p>Клиент: {order.customer_name}</p>
                <p>Телефон: {order.customer_phone}</p>
                <p>Адрес доставки: {order.delivery_city}, {order.delivery_address}</p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>№</th>
                        <th>Наименование</th>
                        <th>Артикул</th>
                        <th>Кол-во</th>
                        <th>Цена</th>
                        <th>Сумма</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for idx, item in enumerate(order.items.all(), 1):
            html_content += f"""
                    <tr>
                        <td>{idx}</td>
                        <td>{item.part.title}</td>
                        <td>{item.part.manufacturer_number or '-'}</td>
                        <td>{item.quantity}</td>
                        <td>{item.unit_price} ₽</td>
                        <td>{item.total_price} ₽</td>
                    </tr>
            """
        
        html_content += f"""
                </tbody>
            </table>
            
            <div class="total">
                <p>Итого: {order.total_amount} ₽</p>
            </div>
            
            <p style="margin-top: 40px;">Подпись: _________________</p>
        </body>
        </html>
        """
        
        return HttpResponse(html_content, content_type='text/html')
        
    except Order.DoesNotExist:
        return HttpResponse('Заказ не найден', status=404)


@api_view(['GET'])
@permission_classes([AllowAny])
def print_receipt(request, order_id):
    """Печать чека"""
    try:
        order = Order.objects.prefetch_related('items__part').get(id=order_id)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Чек №{order.order_number}</title>
            <style>
                body {{ font-family: 'Courier New', monospace; width: 300px; margin: 20px auto; }}
                .center {{ text-align: center; }}
                .line {{ border-top: 1px dashed #000; margin: 10px 0; }}
                .item {{ display: flex; justify-content: space-between; }}
            </style>
        </head>
        <body>
            <div class="center">
                <h2>GoodDrive</h2>
                <p>Автозапчасти</p>
                <p>г.Челябинск, ул.Артиллерийская, 15/2</p>
                <p>Тел: +7 (922) 708-15-53</p>
            </div>
            
            <div class="line"></div>
            
            <p>Чек №{order.order_number}</p>
            <p>{order.created_at.strftime('%d.%m.%Y %H:%M')}</p>
            
            <div class="line"></div>
        """
        
        for item in order.items.all():
            html_content += f"""
            <div class="item">
                <span>{item.part.title[:30]}</span>
            </div>
            <div class="item">
                <span>{item.quantity} x {item.unit_price} ₽</span>
                <span>{item.total_price} ₽</span>
            </div>
            """
        
        html_content += f"""
            <div class="line"></div>
            
            <div class="item" style="font-weight: bold; font-size: 16px;">
                <span>ИТОГО:</span>
                <span>{order.total_amount} ₽</span>
            </div>
            
            <div class="line"></div>
            
            <div class="center">
                <p>Спасибо за покупку!</p>
                <p>gooddrive-shop.ru</p>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html_content, content_type='text/html')
        
    except Order.DoesNotExist:
        return HttpResponse('Заказ не найден', status=404)


@api_view(['GET'])
@permission_classes([AllowAny])
def export_to_1c(request):
    """Экспорт заказов в формате для 1С"""
    from datetime import datetime, timedelta
    
    # Экспорт заказов за последние 7 дней
    date_from = datetime.now() - timedelta(days=7)
    orders = Order.objects.filter(created_at__gte=date_from).prefetch_related('items__part')
    
    # Простой CSV формат для 1С
    csv_content = "Номер заказа;Дата;Клиент;Телефон;Сумма;Статус\n"
    
    for order in orders:
        csv_content += f"{order.order_number};{order.created_at.strftime('%d.%m.%Y')};{order.customer_name};{order.customer_phone};{order.total_amount};{order.get_status_display()}\n"
    
    response = HttpResponse(csv_content, content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="orders_1c_{datetime.now().strftime("%Y%m%d")}.csv"'
    return response

