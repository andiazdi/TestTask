from django.utils.html import format_html_join
from django.contrib import admin
from .models import Order, OrderItem
import openpyxl
from django.http import HttpResponse
import logging

LOG_FORMAT = "[%(asctime)s] %(levelname)s | %(name)s | %(message)s"

logging.basicConfig(
    level=logging.INFO, filemode="a", filename="bot.logs", format=LOG_FORMAT
)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.action(description="Export selected orders to Excel")
def export_orders_to_excel(modeladmin, request, queryset):
    logging.info("Export selected orders to Excel")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Orders"

    headers = ['Order ID', 'User', 'Address', 'Products']
    ws.append(headers)

    for order in queryset:
        products = "; ".join(
            f"Product {item.product_id} x{item.quantity} (${item.price})"
            for item in order.items.all()
        )
        ws.append([order.id, str(order.user), order.address, products])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=orders.xlsx'
    wb.save(response)
    logging.info("Orders exported successfully")
    return response


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'formatted_items')
    search_fields = ('user__telegram_id', 'address')
    inlines = [OrderItemInline]
    actions = [export_orders_to_excel]

    def formatted_items(self, obj):
        items = obj.items.all()
        if not items:
            return "-"

        return format_html_join(
            '\n',
            '<div>{} {}шт. — <strong>${}</strong></div>',
            ((item.product.title, item.quantity, item.price) for item in items)
        )
    formatted_items.short_description = "Order Items"
