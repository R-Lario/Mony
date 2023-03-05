from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username}"
    
    def save(self, *args, **kwargs):
        is_new_user = self.pk is None

        super().save()
        #add default categories to the user
        if is_new_user:
            default_categories = [
                "Food",
                "Transportation",
                "Housing",
                "Utilities",
                "Clothing",
                "Healthcare",
                "Entertainment",
                "Personal Care",
                "Savings",
                "Miscellaneous",
            ]
            for category in default_categories:
                SpendingCategories.objects.create(user_id=self.id, category=category)
        


class Banks(models.Model):
    user_id = models.IntegerField()
    requisition_id = models.CharField(max_length=64)
    bank_name = models.CharField(max_length=64)
    image_url = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.bank_name} by {self.user_id}"

class Agreements(models.Model):
    user_id = models.IntegerField(null=True)
    agreement_id = models.CharField(max_length=64)
    requisition_id = models.CharField(max_length=64, null=True)
    bank_name = models.CharField(max_length=64)
    image_url = models.CharField(max_length=256)

    def __str__(self):
        return f"uid: {self.user_id}, req_id: {self.requisition_id}, agr_id: {self.agreement_id}"

class Transactions(models.Model):
    user_id = models.IntegerField(null=True)
    requisition_id = models.CharField(max_length=64)
    transaction_id = models.CharField(max_length=128)
    date = models.DateField()
    transaction_amount = models.DecimalField(max_digits=7, decimal_places=2)
    currency = models.CharField(max_length=4)
    description = models.CharField(max_length=256)
    category = models.ForeignKey("SpendingCategories", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.date} / {self.transaction_amount} {self.currency} / {self.description}"

class SpendingCategories(models.Model):
    user_id = models.IntegerField(null=True)
    category = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.user_id}: {self.category}"