from django.db import models

class TelegramUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    telegram_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username or str(self.telegram_id)

    class Meta:
        db_table = 'users'