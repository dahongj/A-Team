from django.urls import path
from shop import views

urlpatterns = [
    path('',views.shop, name='shop'),
    path('buy/<item_id>', views.buy, name='buy'),
]