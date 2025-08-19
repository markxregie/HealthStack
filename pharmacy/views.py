import email
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from hospital.models import Patient
from pharmacy.models import Medicine, Cart, Order
from .utils import searchMedicines
import requests
import base64


@csrf_exempt
@login_required(login_url="login")
def pharmacy_single_product(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.get(serial_number=pk)
        orders = Order.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'patient': patient, 'medicines': medicines, 'carts': carts, 'order': order, 'orders': orders}
        else:
            context = {'patient': patient, 'medicines': medicines, 'carts': carts, 'orders': orders}
        return render(request, 'pharmacy/product-single.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')


# ...existing imports...

@csrf_exempt
@login_required(login_url="login")
def pharmacy_shop(request):
    if request.user.is_authenticated and request.user.is_patient:
        patient = Patient.objects.get(user=request.user)
        medicines, search_query = searchMedicines(request)
        orders = Order.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)

        # Normalize category for JS filtering
        for med in medicines:
            raw_cat = med.medicine_category or ""
            normalized = (
                raw_cat.lower()
                .replace(" ", "")
                .replace("/", "")
                .replace("&", "")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
                .replace(".", "")
            )
            # Map some common categories to tab values
            mapping = {
                "fever": "fever",
                "pain": "pain",
                "cough": "cough",
                "cold": "cold",
                "flu": "flu",
                "allergy": "allergy",
                "infection": "infection",
                "stomach": "stomach",
                "hypertension": "hypertension",
                "heart": "hypertension",
                "diabetes": "diabetes",
                "skin": "skin",
                "vitamins": "vitamins",
                "eyeearnose": "eye",
                "respiratoryasthmabronchitis": "respiratory",
                "urinary": "urinary",
                "firstaid": "firstaid",
            }
            med.normalized_category = mapping.get(normalized, normalized)

        context = {
            'patient': patient,
            'medicines': medicines,
            'carts': carts,
            'orders': orders,
            'search_query': search_query
        }
        if orders.exists():
            context['order'] = orders[0]

        return render(request, 'Pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')



@csrf_exempt
@login_required(login_url="login")
def cart_view(request):
    if request.user.is_authenticated and request.user.is_patient:
        patient = Patient.objects.get(user=request.user)
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)

        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'carts': carts, 'order': order, 'patient': patient}
            return render(request, 'Pharmacy/cart.html', context)
        else:
            messages.info(request, "Your cart is empty.")
            return redirect('pharmacy-shop')
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'patient-login.html')


@csrf_exempt
@login_required(login_url="login")
def add_to_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
        item = get_object_or_404(Medicine, pk=pk)
        order_item, created = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} quantity was updated.")
            else:
                order.orderitems.add(order_item)
                messages.success(request, f"{item.name} was added to your cart.")
        else:
            order = Order.objects.create(user=request.user)
            order.orderitems.add(order_item)
            messages.success(request, f"{item.name} was added to your cart.")

        return redirect('pharmacy-cart')
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')


@csrf_exempt
@login_required(login_url="login")
def remove_from_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} was removed from your cart.")
            else:
                messages.info(request, "This item was not in your cart.")
        else:
            messages.info(request, "You don't have an active order.")
        return redirect('pharmacy-cart')
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')


@csrf_exempt
@login_required(login_url="login")
def increase_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated.")
        return redirect('pharmacy-cart')
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')


@csrf_exempt
@login_required(login_url="login")
def decrease_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, f"{item.name} quantity has been updated")
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request, f"{item.name} has been removed from your cart.")
        return redirect('pharmacy-cart')
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')


@login_required(login_url="login")
def create_paymongo_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    patient = get_object_or_404(Patient, user=request.user)

    total_amount = order.get_totals()
    amount_in_cents = int(float(total_amount) * 100)

    if amount_in_cents <= 0:
        messages.error(request, "Cannot process payment for an empty or free cart.")
        return redirect('pharmacy-cart')

    secret_key = settings.PAYMONGO_SECRET_KEY
    auth_header = base64.b64encode(f"{secret_key}:".encode()).decode()

    payload = {
        "data": {
            "attributes": {
                "amount": amount_in_cents,
                "currency": "PHP",
                "type": "gcash",
                "redirect": {
                    "success": request.build_absolute_uri('/pharmacy/payment/success/'),
                    "failed": request.build_absolute_uri('/pharmacy/payment/failed/')
                },
                "billing": {
                    "name": patient.name or request.user.username,
                    "email": request.user.email,
                    "phone": patient.phone_number or "09000000000"
                }
            }
        }
    }

    try:
        response = requests.post(
            "https://api.paymongo.com/v1/sources",
            headers={
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=15
        )
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        messages.error(request, f"Payment gateway error: {e}")
        return redirect('pharmacy-cart')

    if "errors" in data:
        messages.error(request, f"PayMongo error: {data['errors'][0].get('detail', 'Unknown error')}")
        return redirect('pharmacy-cart')

    try:
        source_id = data['data']['id']
        checkout_url = data['data']['attributes']['redirect']['checkout_url']
    except (KeyError, TypeError):
        messages.error(request, "Unexpected response from payment gateway.")
        return redirect('pharmacy-cart')

    order.payment_session_id = source_id
    order.payment_status = "Pending"
    order.save()
    request.session['pending_payment_source'] = source_id

    return redirect(checkout_url)


@login_required(login_url="login")
def payment_success(request):
    source_id = request.GET.get("source_id") or request.session.pop('pending_payment_source', None)

    if not source_id:
        messages.error(request, "Missing payment reference.")
        return redirect('pharmacy-cart')

    try:
        order = Order.objects.get(payment_session_id=source_id, user=request.user, ordered=False)
    except Order.DoesNotExist:
        messages.error(request, "No matching order found for this payment.")
        return redirect('pharmacy-cart')

    secret_key = settings.PAYMONGO_SECRET_KEY
    auth_header = base64.b64encode(f"{secret_key}:".encode()).decode()

    try:
        response = requests.get(
            f"https://api.paymongo.com/v1/sources/{source_id}",
            headers={"Authorization": f"Basic {auth_header}"},
            timeout=15
        )
        data = response.json()
    except requests.RequestException as e:
        messages.error(request, f"Error verifying payment: {e}")
        return redirect('pharmacy-cart')

    status = data.get("data", {}).get("attributes", {}).get("status")
    if status != "chargeable":
        messages.error(request, f"Payment status is '{status}', not completed.")
        return redirect('pharmacy-cart')

    payment_id = None
    try:
        payments_resp = requests.get(
            "https://api.paymongo.com/v1/payments",
            headers={"Authorization": f"Basic {auth_header}"},
            timeout=15
        )
        payments_data = payments_resp.json()
        for payment in payments_data.get("data", []):
            source_info = payment.get("attributes", {}).get("source", {})
            if source_info.get("id") == source_id:
                payment_id = payment.get("id")
                break
    except requests.RequestException as e:
        messages.warning(request, f"Could not fetch payment ID: {e}")

    order.ordered = True
    order.payment_id = payment_id
    order.payment_status = "Paid"
    order.save()

    Cart.objects.filter(user=request.user, purchased=False).delete()

    messages.success(request, "Payment verified and successful! Thank you for your purchase.")
    return redirect('patient-dashboard')


@login_required(login_url="login")
def payment_failed(request):
    source_id = request.session.pop('pending_payment_source', None)
    if source_id:
        Order.objects.filter(payment_session_id=source_id, user=request.user, ordered=False).update(payment_status="Failed")
    messages.error(request, "Payment was cancelled or failed. Please try again.")
    return redirect('pharmacy-cart')
