from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# from . --> same directory
# Views functions and urls must be linked. # of views == # of urls
# App URL file - urls related to hospital


urlpatterns = [
    path('product-single/<int:pk>/', views.pharmacy_single_product, name='product-single'),
    path('pharmacy/shop/', views.pharmacy_shop, name='pharmacy-shop'),
    path('cart/', views.cart_view, name='pharmacy-cart'),
    path('remove-item/<int:pk>/', views.remove_from_cart, name='remove-item'),
   
    path('add-to-cart/<int:pk>', views.add_to_cart, name='add-to-cart'),
    path('increase-item/<int:pk>/', views.increase_cart, name='increase-item'),
    path('decrease-item/<int:pk>/', views.decrease_cart, name='decrease-item'),
    # URL para simulan ang payment process. Ang <int:order_id> ay galing sa cart.
    path('paymongo/checkout/<int:order_id>/', views.create_paymongo_payment, name='create-paymongo-payment'),

    # URL kung saan babalik ang user pagkatapos ng successful na bayad
    path('payment/success/', views.payment_success, name='payment-success'),
    
    # URL kung saan babalik ang user kung nag-fail o kinancel ang bayad
    path('payment/failed/', views.payment_failed, name='payment-failed'),
]
    


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
