from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Dish, Drink, Cart, CartContent
from django.core.exceptions import ObjectDoesNotExist
from .forms import SearchForm, LoginForm, RegisterForm, EditForm, EditsForm
from django.views import View
from django.contrib.postgres.search import SearchVector

def view_dishes(request):
    all_dishes = Dish.objects.all()
    name = ''
    if request.method == 'POST':
        form = SearchForm(request.POST)
        search = request.POST.get('search')
        if form.is_valid() and search:
            all_dishes = all_dishes.filter(title__contains=search)
    else:
        form = SearchForm()

    return render(request, 'index.html', {'dishes': all_dishes,'rop': form, 'user': request.user})

def view_drinkers(request):
    all_drinkers=Drink.objects.all()
    name = ''
    if request.method=='POST':
        form = SearchForm(request.POST)
        search =request.POST.get('search')
        if form.is_valid() and search:
            all_drinkers=all_drinkers.filter(title__contains=search)
    else:
        form=SearchForm()

    return render(request, 'index.html', {'dishes': all_drinkers,'rop':form,'user':request.user})
# def view_drinkers(request):
#     all_drinkers = Drink.objects.all()
#     return render(request, 'index.html', {'drinkers': all_drinkers})



def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # if request.GET and 'next' in request.GET:
                #     return redirect(request.GET['next'])
                return redirect('/')
            else:
                form.add_error('login', 'Bad login or password')
                form.add_error('password', 'Bad login or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('/')



def mypol(request):
    if request.method == 'POST':
        form = EditsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EditsForm(instance=request.user)
    return render(request,'my_p.html',{'form': form, 'submit_text': 'Изменить', 'auth_header': 'Изменение профиля'})

def edit_dish(request, dish_id):
    dish = Dish.objects.get(id=dish_id)

    if request.method == 'POST':
        dish_form = EditForm(request.POST, instance=dish)
        if dish_form.is_valid():
            dish_form.save()
            return redirect('/')
    else:
        dish_form = EditForm(instance=dish)
    return render(request, 'do.html', {'form': dish_form})






class MasterView(View):

    def get_cart_records(self, cart=None, response=None):
        cart = self.get_cart() if cart is None else cart
        if cart is not None:
            cart_records = CartContent.objects.filter(cart_id=cart.id)
        else:
            cart_records = []

        if response:
            response.set_cookie('cart_count', len(cart_records))
            return response

        return cart_records

    def get_cart(self):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except ObjectDoesNotExist:
                cart = Cart(user_id=user_id,
                            total_cost=0)
                cart.save()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            try:
                cart = Cart.objects.get(session_key=session_key)
            except ObjectDoesNotExist:
                cart = Cart(session_key=session_key,
                            total_cost=0)
                cart.save()
        return cart


class HomeView(MasterView):
    all_dishes = Dish.objects.all()

    def get(self, request):
        form = SearchForm()
        return render(request, 'index.html',
                      {'dishes': self.all_dishes, 'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        search = request.POST.get('search')
        if form.is_valid() and search:
            search_vector = SearchVector('title',
                                         'description',
                                         'categories__title',
                                         'company__title', )
            self.all_dishes = self.all_dishes.annotate(search=search_vector).filter(search=search)
        else:
            form = SearchForm()
        return render(request, 'index.html',
                      {'dishes': self.all_dishes, 'form': form, 'user': request.user})
class CartView(MasterView):
    def get(self, request):
        cart = self.get_cart()
        cart_records = self.get_cart_records(cart)
        cart_total = cart.get_total() if cart else 0

        context = {
            'cart_records': cart_records,
            'cart_total': cart_total,
        }
        return render(request, 'cart.html', context)

    def post(self, request):
        dish = Dish.objects.get(id=request.POST.get('dish_id'))
        cart = self.get_cart()
        quantity = request.POST.get('qty')
        # get_or_create - найдет обьект, если его нет в базе, то создаст
        # первый параметр - обьект, второй - булевое значение которое сообщает создан ли обьект
        # если обьект создан, то True, если он уже имеется в базе, то False
        cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=dish)
        cart_content.qty = quantity
        cart_content.save()
        response = self.get_cart_records(cart, redirect('/#dish-{}'.format(dish.id)))
        return response
