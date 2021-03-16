from django.urls import path
import shop.views as v
urlpatterns = [

    path('', v.HomeView.as_view(), name="index"),
    path('cart/', v.CartView.as_view(), name='cart'),
    path('',v.view_dishes,name='index'),
    path('w/', v.view_drinkers, name='index'),
    path('login/', v.log_in, name="login"),
    path('register/', v.register, name="register"),
    path('myp/',v.mypol,name='my_p'),
    path('logout/',v.log_out,name='log_out'),
    path('b/',v.edit_dish,name='do'),
    # path('edit_dish/<int:dish_id>/', v.edit_dish, name='do')
]
