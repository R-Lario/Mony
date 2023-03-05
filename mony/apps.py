from django.apps import AppConfig


class MonyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mony'

    def ready(self):
        from .models import SpendingCategories
        if not SpendingCategories.objects.exists():
            SpendingCategories.objects.create(user_id=None, category="Default Category 1")
            SpendingCategories.objects.create(user_id=None, category="Default Category 2")
            # Add more default SpendingCategories objects as needed.

