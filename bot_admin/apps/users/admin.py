from django.contrib import messages, admin
from django.shortcuts import render, redirect
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from .models import TelegramUser
from .forms import BroadcastMessageForm
from .utils import send_telegram_message
import logging
import asyncio

LOG_FORMAT = "[%(asctime)s] %(levelname)s | %(name)s | %(message)s"

logging.basicConfig(
    level=logging.INFO, filemode="a", filename="bot.logs", format=LOG_FORMAT
)

async def broadcast_messages(users, message_text):
    tasks = [send_telegram_message(user, message_text) for user in users]
    results = await asyncio.gather(*tasks)
    return sum(results)

@admin.register(TelegramUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'first_name')
    search_fields = ('username', 'telegram_id')

    actions = ['broadcast_message']

    def broadcast_message(self, request, queryset):
        if 'apply' in request.POST:
            form = BroadcastMessageForm(request.POST)
            if form.is_valid():
                message_text = form.cleaned_data['message']
                selected_ids = request.POST.getlist(ACTION_CHECKBOX_NAME)
                users = TelegramUser.objects.filter(pk__in=selected_ids)
                logging.info(f"Broadcasting message: {message_text} for {len(users)} users")
                asyncio.run(broadcast_messages(users, message_text))
                self.message_user(request, f"Успешно отправлено {len(users)} сообщений.", messages.SUCCESS)
                return redirect(request.get_full_path())
        else:
            form = BroadcastMessageForm(initial={'_selected_action': request.POST.getlist(ACTION_CHECKBOX_NAME)})

        return render(request, 'admin/broadcast_message.html', {
            'form': form,
            'title': "Рассылка сообщения",
            'users': queryset,
        })

    broadcast_message.short_description = "📣 Отправить произвольное сообщение"