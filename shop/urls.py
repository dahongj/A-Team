from django.urls import path
from shop import views

urlpatterns = [
    path('market',views.shop, name='market'),
    path('buy/<item_id>', views.buy, name='buy'),
]