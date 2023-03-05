from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotFound
from django.core import serializers
from django.urls import reverse
from django.db.models.functions import ExtractMonth, TruncMonth

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt

from mony.models import Banks, Agreements, Transactions, SpendingCategories
from .forms import RequisitionSerializer, TransactionSerializer, SpendingCategoriesSerializer, TransactionCategorySerializer

import json, requests, os, sys



if not (
    (secret_id := os.environ.get('secret_id')) and 
    (secret_key := os.environ.get('secret_key'))
):
    sys.exit("No Nordigen secret_id and/or secret_key could be found in the environment variables.")


############## API NORDIGEN ################
urls = {
    "new-token": "https://ob.nordigen.com/api/v2/token/new/",
    "refresh-token": "https://ob.nordigen.com/api/v2/token/refresh/",
    "get-banks": "https://ob.nordigen.com/api/v2/institutions?country=",
    "create-user-agreement": "https://ob.nordigen.com/api/v2/agreements/enduser/",
    "requisitions": "https://ob.nordigen.com/api/v2/requisitions/",
    "accounts": "https://ob.nordigen.com/api/v2/accounts/",
}

def generate_access_token(request):
    url = urls["new-token"]

    payload = json.dumps({
    "secret_id": secret_id,
    "secret_key": secret_key
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    return JsonResponse(response.json())

def refresh_access_token(request):
    if request.method != "POST":
        return JsonResponse({"Error": "Incorrect method"}, status=400)

    if not (refresh_token := json.loads(request.body.decode("utf-8")).get("refreshToken")):
        return JsonResponse({"Error": "Couldn't find refresh token"}, status=401)

    url = urls["refresh-token"]
    payload = {"refresh": f"{refresh_token}"}

    response = requests.request("POST", url, data=payload)

    return JsonResponse(response.json(), status=response.status_code)

def get_banks(request, country_code):
    auth_token = request.headers.get("Authorization")
    url = urls["get-banks"] + country_code

    headers = {
    'Authorization': f'Bearer {auth_token}',
    'content-type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)
    
    return JsonResponse(response.json(), safe=False)

def create_user_agreement(request):
    if request.method != "POST":
        return JsonResponse({"Error": "Invalid method"}, status=400)

    institution_id = json.loads(request.body.decode('utf-8')).get('institution_id')
    
    if not institution_id:
        return JsonResponse({"Error": "No institution id found"}, status=400)
    
    auth_token = request.headers.get("Authorization")

    url = urls["create-user-agreement"]

    payload = json.dumps({
    "institution_id": f"{institution_id}"
    })

    headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return JsonResponse(response.json())

def build_link(request):
    if request.method != "POST":
        return JsonResponse({"Error": "Invalid method"}, status=400)

    body = json.loads(request.body.decode('utf-8'))

    if ( not (
        (redirect_link := body.get("redirect")) and 
        (institution_id := body.get("institution_id")) and 
        (agreement_id := body.get("agreement")))
    ):
        return JsonResponse({"Error": "Invalid body"}, status=400)

    url = urls["requisitions"]

    if not (auth_token := request.headers.get("Authorization")):
        return JsonResponse({"Error": "No auth token"}, status=400)



    payload = json.dumps({
    "redirect": redirect_link,
    "institution_id": institution_id,
    "agreement": agreement_id
    })
    headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return JsonResponse(response.json())

def list_accounts(request):
    if request.method != "POST":
        return JsonResponse({"Error": "Invalid method"})

    body = json.loads(request.body.decode('utf-8'))

    if not (auth_token := request.headers.get("Authorization")):
        return JsonResponse({"Error": "No auth token"}, status=400)

    if not (requisition_id := body.get("requisitionId")):
        return JsonResponse({"Error": "No requisition id"}, status=404)

    url = urls["requisitions"] + requisition_id
    headers = {
    'Authorization': f'Bearer {auth_token}'
    }

    response = requests.request("GET", url, headers=headers)
    return JsonResponse(response.json())

def get_bank_transactions(request, account_number):
    if not (auth_token := request.headers.get("Authorization")):
        return JsonResponse({"Error": "No auth token"}, status=400)
    
    url = urls["accounts"] + account_number + "/transactions"

    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    response = requests.request("GET", url, headers=headers)

    return JsonResponse(response.json())

############## END API NORDIGEN #############




# REQUISITION HANDLERS

# this validates requisition id's
def validate_requisition(client_access_token, requisition_id):
    url = urls["requisitions"] + requisition_id
    headers = {
        'Authorization': f'Bearer {client_access_token}'
    }
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False

#this sets an agreement id, so a requisition id can be bound to it later
@api_view(["POST"])
def set_agreement_id(request):
    if request.method == "POST" and request.user.is_authenticated:
        if (
            (agreement_id := request.data.get("agreement_id")) and 
            (bank_name := request.data.get("bank_name")) and
            (image_url := request.data.get("image_url"))
            ):
            agreement = Agreements(user_id=request.user.id, agreement_id=agreement_id, bank_name=bank_name, image_url=image_url)
            agreement.save()
            return JsonResponse({"Message": "Agreement setup succesfully."}, status=200)
    return JsonResponse({"Error": "Some error occured while setting up the agreement."}, status=400)

#this binds a requisition id to the previously set agreement id
@api_view(["POST"])
def bind_requisition(request):
    if request.method == "POST" and request.user.is_authenticated:
        if (
            (agreement_id := request.data.get("agreement_id")) and 
            (requisition_id := request.data.get("requisition_id")) and
            (client_access_token := request.COOKIES.get("accessToken"))
            ):
            
            agreement = Agreements.objects.get(user_id=request.user.id, agreement_id=agreement_id)
            if agreement and validate_requisition(client_access_token, requisition_id):
                agreement.requisition_id = requisition_id
                agreement.save()
                return JsonResponse({"Message": "Bound requisition succesfully."}, status=200)

    return JsonResponse({"Error": "Some error occured while binding requisition."}, status=400)

#this is the confirmation link when visited, the requisition gets added to the user.
def confirm_agreement(request, agreement_id):
    if request.method == "GET" and request.user.is_authenticated:
        agreement = Agreements.objects.get(user_id=request.user.id, agreement_id=agreement_id)
        if agreement:
            requisition_id = agreement.requisition_id
            bank_name = agreement.bank_name
            image_url = agreement.image_url
            if requisition_id and bank_name and image_url:
                new_connected_bank = Banks(user_id=request.user.id, requisition_id=requisition_id, bank_name=bank_name, image_url=image_url)
                new_connected_bank.save()
                return redirect('mony:index')
    return JsonResponse({"Error": "Some error occured while confirming requisition."}, status=400)

#END REQUISITION HANDLERS


@api_view(['GET'])
def requisitions(request):
    if not request.user.is_authenticated:
        return JsonResponse({"Error": "You need to be logged in to access this endpoint"}, status=401)
    
    user_id = request.user.id

    queryset = Banks.objects.filter(user_id=user_id)
    serializer = RequisitionSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def requisition_delete(request, requisition_id):
    if not request.user.is_authenticated:
        return JsonResponse({"Error": "You need to be logged in to access this endpoint"}, status=401)
    
    if request.method != "DELETE":
        return JsonResponse({"Error": "Invalid method"}, status=400)

    user_id = request.user.id
    try:
        queryset = Banks.objects.get(user_id=user_id, requisition_id=requisition_id)
        queryset.delete()
        transactions_to_delete = Transactions.objects.filter(user_id=user_id, requisition_id=requisition_id)
        print(transactions_to_delete)
        transactions_to_delete.delete()
        return JsonResponse({"Message": "Requisition including it's transactions have been succesfully deleted."}, status=200)
    except:
        return JsonResponse({"Error": "Some error occured while deleting the requisition and/or the transactions associated with it."}, status=400)
    

def get_transactions(request):
    if not request.user.is_authenticated:
        return JsonResponse({"Error": "User not logged in"}, status=400)

    if not (auth_token := request.headers.get("Authorization")):
        return JsonResponse({"Error": "No auth token"}, status=400)

    def get_accounts(requisition_id):
        url = urls["requisitions"] + requisition_id
        headers = {
        'Authorization': f'Bearer {auth_token}'
        }
        response = requests.request("GET", url, headers=headers)
        accounts = response.json().get("accounts")

        return [{account: requisition_id} for account in accounts]
    
    def get_transactions(accounts):
        account_id = list(accounts.keys())[0]
        requisition_id = list(accounts.values())[0]

        url = urls["accounts"] + account_id + "/transactions"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        response = requests.request("GET", url, headers=headers)
        data = response.json().get("transactions").get("booked")
        for transaction in data:
            transaction['requisitionId'] = requisition_id

        return data
    
    def add_transactions(transactions): #to database
        for transaction in transactions:
            requisition_id = transaction.get('requisitionId')
            transaction_id = transaction.get("transactionId")
            date = transaction.get("bookingDate")
            transaction_amount = transaction.get("transactionAmount").get("amount")
            currency = transaction.get("transactionAmount").get("currency")
            transaction_comment = transaction.get("remittanceInformationUnstructuredArray")
            description = f"{transaction.get('creditorName') + ' -' if transaction.get('creditorName') else ''}{transaction.get('debtorName') + ' -' if transaction.get('debtorName') else ''} {'' if transaction_comment == None else transaction_comment[0]}"
            
            existing_transaction = Transactions.objects.filter(
                user_id=request.user.id,
                requisition_id=requisition_id,
                transaction_id=transaction_id,
                date=date,
                transaction_amount=transaction_amount,
                currency=currency,
                description=description           
                ).first()

            if not existing_transaction:
                new_transaction = Transactions(
                user_id=request.user.id,
                requisition_id=requisition_id,
                transaction_id=transaction_id,
                date=date,
                transaction_amount=transaction_amount,
                currency=currency,
                description=description           
                )
                new_transaction.save()

    def get_db_transactions():
        queryset = Transactions.objects.filter(user_id=request.user.id).order_by("-date")
        if queryset:
            serializer = TransactionSerializer(queryset, many=True)
            return serializer.data
        
        return []
        

    user_id = request.user.id
    banks = Banks.objects.filter(user_id=user_id)

    #if no banks connected to the user
    if not banks:
        return JsonResponse({}, status=200)
    
    bank_accounts = sum([get_accounts(bank.requisition_id) for bank in banks], [])
    transactions = sum([get_transactions(accounts) for accounts in bank_accounts], [])

    add_transactions(transactions)
    transactions = get_db_transactions()
    if transactions:
        return JsonResponse(transactions, status=200, safe=False)


    return JsonResponse({"Error": "Some error occured"}, status=400)

@api_view(['GET', 'POST', 'DELETE'])
def category(request):
    if not request.user.is_authenticated:
        return JsonResponse({"Error": "not authenticated"}, status=400)
    
    user_id = request.user.id
    
    if request.method == "POST":
        request.data['user_id'] = user_id
        serializer = SpendingCategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Message": "Category added successfully"}, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)
        
    if request.method == "DELETE":
        if not (category := request.data.get("category")):
            return Response({"Error": "Needs a category to delete"}, status=400)
        
        try:
            queryset = SpendingCategories.objects.get(user_id=user_id, category=category)
            queryset.delete()
            return Response({"Message": "Category deleted successfully."}, status=200)
        except:
            return Response({"Error": "Category couldn't be removed"}, status=400)
        

    queryset = SpendingCategories.objects.filter(user_id=user_id)
    serializer = SpendingCategoriesSerializer(queryset, many=True)

    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['POST'])
def set_transaction_category(request):
    if request.method != "POST":
        return JsonResponse({"Error": "Invalid mehod"}, status=400)
    
    serializer = TransactionCategorySerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    
    serializer.user_id = request.user.id
    
    serializer.save()

    return JsonResponse({"Message": "Succesfully updated transaction category"}, status=200)

@api_view(['GET'])
def get_category_spending_per_month(request):
    if not request.user.is_authenticated:
        return Response({}, status=400)
    user_id = request.user.id
    transactions = Transactions.objects.filter(user_id=user_id).exclude(transaction_amount__gte=0).order_by(ExtractMonth('date')).annotate(month=TruncMonth("date"))

    transactions_by_month = {}
    for transaction in transactions:
        month_str = transaction.month.strftime('%B %Y')
        category = "Undefined" if not transaction.category else transaction.category.category
        transaction_amount = abs(transaction.transaction_amount)

        if month_str not in transactions_by_month:
            transactions_by_month[month_str] = {}
        
        if category not in transactions_by_month[month_str]:
            transactions_by_month[month_str][category] = transaction_amount
        else:
            transactions_by_month[month_str][category] += transaction_amount

    return Response(transactions_by_month, status=200)