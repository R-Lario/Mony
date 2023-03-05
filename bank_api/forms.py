from django import forms
from mony.models import Banks, Transactions, SpendingCategories
from rest_framework import serializers



class RequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banks
        fields=['user_id', 'requisition_id', 'bank_name', 'image_url']


class SpendingCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpendingCategories
        fields=['category', 'user_id']

class TransactionSerializer(serializers.ModelSerializer):
    category = SpendingCategoriesSerializer()
    class Meta:
        model=Transactions
        fields=['transaction_id', 'date', 'transaction_amount', 'currency', 'description', 'category']

class TransactionCategorySerializer(TransactionSerializer):
    category = serializers.CharField(source='category.category')

    user_id = None
    update_successful = False

    class Meta:
        model = Transactions
        fields = ['transaction_id', 'category']
    
    def save(self):
        transaction_id = self.data.get('transaction_id')
        try:
            transaction_obj = Transactions.objects.get(transaction_id=transaction_id)
        except:
            return

        category_text =  self.data.get('category')
        try:
            category_obj = SpendingCategories.objects.get(user_id=self.user_id, category=category_text)
        except:
            return
        
        transaction_obj.category = category_obj
        transaction_obj.save()
        self.update_successful = True



