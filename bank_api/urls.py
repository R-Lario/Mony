from django.urls import path
from . import views

app_name = "bank_api"

urlpatterns = [
    path("get-new-access-token", views.generate_access_token, name="get_new_access_token"),
    path("refresh-access-token", views.refresh_access_token, name="refresh_access_token"),
    path("get-banks/<str:country_code>", views.get_banks, name="get_banks"),
    path("create-user-agreement", views.create_user_agreement, name="create_user_agreement"),
    path("build-link", views.build_link, name="build_link"),

    path("requisitions", views.requisitions, name="requisitions"),
    path("requisitions/<str:requisition_id>", views.requisition_delete, name="requisition_delete"),
    
    #OPTIONAL
    path("handle-requisition-confirmation/set-agreement-id", views.set_agreement_id, name="set_agreement_id"),
    path("handle-requisition-confirmation/bind-requisition", views.bind_requisition, name="bind_requisition"),
    path("handle-requisition-confirmation/confirm-agreement/<str:agreement_id>", views.confirm_agreement, name="confirm_agreement"),
    #END OPTIONAL

    #path("confirm-requisition/<str:requisition_id>", views.confirm_requisition, name="confirm_requisition"),
    
    path("get-transactions", views.get_transactions, name="get_transaction"),
    path("set-transaction-category", views.set_transaction_category, name="set_transaction_category"),
    path("category", views.category, name="category"),

    path("data/category-spending", views.get_category_spending_per_month, name="get_category_spending_per_month"),
]
