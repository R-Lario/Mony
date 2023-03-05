from django.contrib import admin
from .models import User, Banks, Agreements, Transactions, SpendingCategories

# Register your models here.
admin.site.register(User)
admin.site.register(Banks)
admin.site.register(Agreements)
admin.site.register(Transactions)
admin.site.register(SpendingCategories)