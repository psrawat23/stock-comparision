from django.contrib import admin
from django.urls import path, include
from front import views

app_name = "front"

urlpatterns = [
    path('', views.index,name="home"),
    # path('', views.index,name="top_stocks"),
    # path('', views.index,name="trending_stocks"),
    path('compare', views.CompareStocks,name="compare_stocks"),
    path('', views.index,name="all_stocks"),
    path('api/compare_stocks/',views.ReturnComparision),
    path('detail/<str:stock>',views.StockDetail,name="stock_detail"),
    path('returnCompare/',views.returnCompare,name="returnCompare"),

]
