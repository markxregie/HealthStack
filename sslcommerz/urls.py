from unicodedata import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


urlpatterns = [
    path('', views.payment_home, name='payment_home'),

    # SSLCommerz (Appointment / Medicine only)
    path('ssl-payment-request/<int:pk>/<int:id>/', views.ssl_payment_request, name='ssl-payment-request'),
    path('ssl-payment-success/', views.ssl_payment_success, name='ssl-payment-success'),
    path('ssl-payment-fail/', views.ssl_payment_fail, name='ssl-payment-fail'),
    path('ssl-payment-cancel/', views.ssl_payment_cancel, name='ssl-payment-cancel'),
    path('ssl-payment-request-medicine/<int:pk>/<int:id>/', views.ssl_payment_request_medicine, name='ssl-payment-request-medicine'),

    # Test Payment (Paymongo)
    path('payment-testing/<int:pk>/', views.payment_testing, name='payment-testing'),
    path("paymongo/test-payment/<int:pk>/<int:id>/<int:pk2>/", views.paymongo_test_payment_request, name="paymongo-test-payment"),
    path("paymongo/test/success/<int:testorder_id>/", views.paymongo_test_success, name="paymongo-test-success"),
    path("paymongo/test/failed/<int:testorder_id>/", views.paymongo_test_failed, name="paymongo-test-failed"),

    # Appointment Payment (Paymongo)
    path('paymongo/appointment/<int:appointment_id>/', views.create_paymongo_appointment_payment, name='create-paymongo-appointment-payment'),
    path("paymongo/success/<int:appointment_id>/", views.paymongo_payment_success, name="paymongo-payment-success"),
    path("paymongo/cancel/", views.paymongo_payment_cancel, name="paymongo-payment-cancel"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)