from django.urls import path
from myfiles.views import *

urlpatterns = [
    path('products', ProductApiView.as_view()),
    path('sell', SellApiView.as_view()),
    path('selled', SelledApiView.as_view()),
    path('users', UserApiView.as_view())
]