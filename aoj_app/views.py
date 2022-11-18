from itertools import count
from pyexpat import model
from re import L
import urllib
import time
import logging
from django.conf import settings
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.generic import View, TemplateView, ListView, DetailView, FormView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings

from carton.cart import Cart

from aoj.settings import LOGIN_REDIRECT_URL
# from authtools.forms import UserCreationForm
from .forms import UserCreationForm
from .models import *
from .functions import calculate_fp_hash



from django import template

register = template.Library()



logger = logging.getLogger(__name__)


#home page view
class NewIndexView(TemplateView):
    template_name = "aoj_app/demo/home.html"

    def get_context_data(self, **kwargs):
        
        context = super(NewIndexView, self).get_context_data(**kwargs)
        context["latest_magazines"] = Magazine.objects.all()[0:4]
        context["countries"] = Country.objects.all()
        context["latest_news"] = LatestNews.objects.order_by('-created_date')[0:2]       
        context["blog"] = BlogEntry.objects.filter(featured=True).order_by('-created_date')[0:3]
        context['curr_page']=self.request.resolver_match.url_name
        first_country = Country.objects.first()
        video_list = []
        first_country_video = Media.objects.filter(country=first_country)[0:4]
        
        for video in first_country_video:
            video_new=video.video.replace("watch?v=","embed/")
            print(video_new)
            video_list.append(video_new)
        
        context['country_video'] = video_list
        return context

#Login and Register Views
class UserLogInView(LoginView):
    template_name = 'aoj_app/demo/login.html'
    LOGIN_REDIRECT_URL = 'newindex'


class RegisterView(View):
    
    def post(self, request):
        
        form = UserCreationForm(request.POST)
        country = request.POST['country']
        
        if form.is_valid():
            
            user = AuthUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                country=form.cleaned_data['country'],
                zip_code=form.cleaned_data['zip_code'],
                phone_number=form.cleaned_data['phone_number']
            )
            login(request, user)
            return redirect('newindex')
        
        else:
            message = {"error_message": "form data has an error"}
            return render(request, 'aoj_app/demo/register.html', {'form': form})


    def get(self, request):
        form = UserCreationForm()
        return render(request, 'aoj_app/demo/register.html', {'form': form})

#Children Views
class ChildrenView(ListView):
    template_name = "aoj_app/demo/children.html"
    model = Children

    def get_context_data(self, **kwargs):
        context = super(ChildrenView, self).get_context_data(**kwargs)
        children = Children.objects.all()
        data_dict = {}
        for child in children:
            country_name = child.country.name.capitalize()
            if country_name not in data_dict:
                data_dict[country_name] = list()
                data_dict[country_name].append(child)
            else:
                data_dict[country_name].append(child)

            context['child_data'] = data_dict
        return context

#Children Detail view
class ChildrenDetailView(DetailView):
    template_name = "aoj_app/demo/children_detail.html"
    model = Children

    def get(self, *args, **kwargs):
        child = self.get_object()
        if child.checked_out:
            return redirect(reverse("children"))
        return super(ChildrenDetailView, self).get(*args, **kwargs)

#media view 
class MediaView(TemplateView):
    template_name= "aoj_app/demo/media.html"

    def get_context_data(self, **kwargs):    
        context = super(MediaView, self).get_context_data(**kwargs)
        context["countries"] = Country.objects.all()
        first_country = Country.objects.first()
        video_list = []
        first_country_video = Media.objects.filter(country=first_country)
        
        for video in first_country_video:
            video_new=video.video.replace("watch?v=","embed/")
            video_list.append(video_new)
        
        context['country_video'] = video_list
        return context


#contact-us View
# class ContactUsView(TemplateView):
#     template_name = "aoj_app/demo/contact-us.html"


def ContactUsView(request):
    return render(request,'aoj_app/demo/contact-us.html')


#Magazine views
class MagazineView(ListView):
    template_name = "aoj_app/demo/magazine.html"
    model = Magazine


class MagazineDetailView(DetailView):
    template_name = "aoj_app/demo/magazine_detail.html"
    model = Magazine


#Blog views
class BlogView(ListView):
    model = BlogEntry
    template_name = "aoj_app/demo/blog.html"
    paginate_by = 7
    context_object_name= "blogentry"

    def get_queryset(self):
        return BlogEntry.objects.filter(category="DB")


class BlogDetailView(DetailView):
    template_name = "aoj_app/demo/blog_detail.html"
    model = BlogEntry


#Mission views
class MissionDetailView(DetailView):
    template_name = "aoj_app/demo/mission/mission_detail.html"
    model = Mission
    
    def get_context_data(self, **kwargs):
        context=super(MissionDetailView,self).get_context_data(**kwargs)
        mission=context['mission']
        
        try:
            attributes=MissionPageAttributes.objects.filter(country=mission.country)
        except:
            attributes=None
        
        context['attributes']=attributes
        return context

class MissionHaitiView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(MissionHaitiView, self).get_context_data(**kwargs)
        
        try:
            mission = MissionHaiti.objects.first()
            attributes=MissionPageAttributes.objects.filter(country=mission.country)
        except:
            mission = None
            attributes=None
        
        context['mission'] = mission
        context['attributes']=attributes
        return context


class MissionKenyaView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super(MissionKenyaView, self).get_context_data(**kwargs)
        
        try:
            mission = MissionKenya.objects.first()
            attributes=MissionPageAttributes.objects.filter(country=mission.country)
        except:
            mission = None
            attributes=None
        
        context['mission'] = mission
        context['attributes']=attributes
        return context


class MissionGuatemalaView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super(MissionGuatemalaView, self).get_context_data(**kwargs)
        try:
            mission = MissionGuatemala.objects.first()
            attributes=MissionPageAttributes.objects.filter(country=mission.country)
        except:
            mission = None
            attributes=None
        
        context['mission'] = mission 
        context['attributes']=attributes       
        return context



#About page Views
class AboutPageDetailView(DetailView):
    template_name = "aoj_app/demo/about/aboutpage_detail.html"
    model = AboutPage

class AboutStaffView(ListView):
    template_name = "aoj_app/demo/about/about_staff.html"
    model = AboutStaff


class AboutbehaveView(TemplateView):
    template_name = "aoj_app/demo/about/about_behave.html"

    def get_context_data(self, **kwargs):
        context = super(AboutbehaveView, self).get_context_data(**kwargs)
        
        try:
            text = AboutWhatWeBelieve.objects.first()
        except:
            text=None

        context['data'] = text
        return context


class AboutFundPolicyView(TemplateView):
    template_name = "aoj_app/demo/about/about_fund_policy.html"

    def get_context_data(self, **kwargs):
        context = super(AboutFundPolicyView, self).get_context_data(**kwargs)
        
        try:
            text = AboutFundPolicy.objects.first()
        except:
            text=None
        
        context['data'] = text
        return context


class HistoryView(TemplateView):
    template_name = "aoj_app/demo/about/about_histroy.html"

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        
        try:
            text = AboutHistory.objects.first()
        except:
            text=None

        context['data'] = text
        return context


class MissionView(TemplateView):
    template_name = "aoj_app/demo/about/about_mission.html"

    def get_context_data(self, **kwargs):
        context = super(MissionView, self).get_context_data(**kwargs)
        try:
            text = AboutMission.objects.first()
        except:
            text=None
        
        context['data'] = text
        return context



#Team page views
class TeamsBlogView(ListView):
    model = BlogEntry
    template_name = "aoj_app/demo/teams/teams_blog.html"

    def get_context_data(self, **kwargs):
        context = super(TeamsBlogView,self).get_context_data(**kwargs)
        context['blogentry']= BlogEntry.objects.filter(category="TB")
        return context


class TeamsConsiderView(ListView):
    model = TeamsConsider
    template_name = "aoj_app/demo/teams/teams_consider.html"


class TeamsTrainingView(ListView):
    model = TeamsTraining
    template_name = "aoj_app/demo/teams/teams_training.html"


class TeamsResourceView(ListView):
    model = TeamsResources
    template_name = "aoj_app/demo/teams/teams_resources.html"


class TeamsCalenderView(ListView):
    model = TeamsCalenderDate
    template_name = 'aoj_app/demo/teams/teams_calender.html'

    def get_context_data(self, **kwargs):
        context = super(TeamsCalenderView,self).get_context_data(**kwargs)
        data_dict = {}
        dates = TeamsCalenderDate.objects.all()
        for count, date in enumerate(dates):
            data_list = []
            data_list.append(date.starting_date)
            data_list.append(date.ending_date)
            data_list.append(date.mission_trip)
            data_dict[count+1] = data_list
        context['data'] = data_dict
        return context


#Donate view
class DonateView(LoginRequiredMixin, TemplateView):
    template_name = "aoj_app/demo/donate.html"

    def get_context_data(self, **kwargs):
        context = super(DonateView, self).get_context_data(**kwargs)

        try:
            context["latest_cr"] = self.request.user.checkoutrequest_set. \
                filter(save_address=True, typ=CheckoutRequest.DONATE).latest(
                    "created_at")
        except CheckoutRequest.DoesNotExist:
            pass

        x_login = settings.EXACT_X_LOGIN
        x_fp_sequence = 597634
        x_amount = 25.00
        x_currency_code = "CAD"

        context["x_login"] = x_login
        context["x_fp_sequence"] = x_fp_sequence
        context["x_amount"] = x_amount
        context["x_currency_code"] = x_currency_code
        context["x_show_form"] = "PAYMENT_FORM"
        context["x_email_customer"] = "TRUE"

        return context


#Catalogue View
class CatalogueView(ListView):
    model = Product
    template_name = "aoj_app/demo/Catalogue.html"
    # paginate_by= 20

    def get_context_data(self, **kwargs):
        context = super(CatalogueView, self).get_context_data(**kwargs)
        context['object_listt']=context['object_list']
        print(context['object_listt'])
        cart = Cart(self.request.session, session_key=None)
        context["cart"] = cart
        return context


#Cart View
class CartView(TemplateView):
    template_name = "aoj_app/demo/cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        cart = Cart(self.request.session, session_key=None)
        context["cart"] = cart
        return context


#Latest News View
class LatestNewsPageDetailView(DetailView):
    template_name = "aoj_app/demo/latestnews/latestnews_detail.html"
    model = LatestNews


#New pages on Navbar view
class HeaderPageDetailView(DetailView):
    template_name = "aoj_app/demo/header/headers_detail.html"
    model = CreateNewPage

class SubHeaderPageDetailView(DetailView):
    template_name = "aoj_app/demo/subheader/subheaders_detail.html"
    model = CreateNewSubPage


#Checkout view
class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "aoj_app/demo/checkout.html"

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        cart = Cart(self.request.session, session_key=None)
        context["cart"] = cart

        try:
            context["latest_cr"] = self.request.user.checkoutrequest_set. \
                filter(save_address=True, typ=CheckoutRequest.CHECKOUT).latest(
                    "created_at")
        except CheckoutRequest.DoesNotExist:
            pass

        x_login = settings.EXACT_X_LOGIN
        x_fp_sequence = 959804
        x_amount = cart.total
        x_currency_code = "CAD"

        context["x_login"] = x_login
        context["x_fp_sequence"] = x_fp_sequence
        context["x_amount"] = x_amount
        context["x_currency_code"] = x_currency_code
        context["x_show_form"] = "PAYMENT_FORM"
        context["x_email_customer"] = "TRUE"

        line_items = []
        print(cart)
        for item in cart.items:
            line_items.append(
                "%s<|>%s<|>%s<|>%s<|>%s<|>Y"
                % (
                    item.product.id,
                    item.product.name,
                    item.product.name,
                    item.quantity,
                    item.product.price,
                )
            )
        context["line_items"] = line_items
        return context


@method_decorator(csrf_exempt, name="dispatch")
class SilentPostView(View):
    def post(self, request, *args, **kwargs):
        fp_sequence = request.POST.get("x_fp_sequence")
        fp_timestamp = request.POST.get("x_fp_timestamp")
        exact_resp_code = request.POST.get("EXact_Resp_Code")
        # https://support.e-xact.com/hc/en-us/community/posts/114094935414-E-xact-Response-Codes-ETG-Codes-
        if exact_resp_code == "00":
            checkout_request = CheckoutRequest.objects.get(
                fp_sequence=fp_sequence, timestamp=fp_timestamp
            )
            checkout_request.paid = True
            checkout_request.save()

        return HttpResponse()


"""
AJAX
"""


@login_required
def ajax_add_to_cart(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=request.GET.get("product_id"))
    cart.add(product, price=product.price)
    _item = None
    for item in cart.items:
        if item.product == product:
            _item = item
    return JsonResponse(
        {
            "error": 0,
            "message": "Added to cart",
            "count": cart.count,
            "qty": _item.quantity,
        }
    )


def ajax_remove_from_cart(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=request.GET.get("product_id"))
    cart.remove(product)
    return JsonResponse(
        {
            "error": 0,
            "message": "Removed from cart",
            "total": cart.total,
            "count": cart.count,
        }
    )


def ajax_show_cart(request):
    cart = Cart(request.session, session_key=None)
    resp = {}
    products = []
    for item in cart.items:
        products.append(
            {
                "name": item.product.name,
                "id": item.product.id,
                "price": item.product.price,
                "total": item.subtotal,
                "quantity": item.quantity,
            }
        )
    resp["error"] = 0
    resp["total"] = cart.total
    resp["products"] = products
    return JsonResponse(resp, safe=False)


def ajax_product_change_quantity(request):
    try:
        cart = Cart(request.session)
        product = Product.objects.get(id=request.GET.get("product_id"))
        cart.set_quantity(product, quantity=request.GET.get("qty"))
        _item = None
        for item in cart.items:
            if item.product == product:
                _item = item
        return JsonResponse(
            {
                "error": 0,
                "message": "Quantity has been changed",
                "qty": _item.quantity,
                "item_subtotal": _item.subtotal,
                "total": cart.total,
                "count": cart.count,
            }
        )
    except:
        return JsonResponse({"error": 1})


def ajax_product_increment_quantity(request):
    try:
        cart = Cart(request.session)
        product = Product.objects.get(id=request.GET.get("product_id"))
        _item = None
        for item in cart.items:
            if item.product == product:
                qty = item.quantity
                _item = item
        cart.set_quantity(product, quantity=qty + 1)
        return JsonResponse(
            {
                "error": 0,
                "message": "Quantity has been incremented",
                "qty": _item.quantity,
                "item_subtotal": _item.subtotal,
                "total": cart.total,
                "count": cart.count,
            }
        )
    except:
        return JsonResponse({"error": 1})


def ajax_product_decrement_quantity(request):
    try:
        cart = Cart(request.session)
        product = Product.objects.get(id=request.GET.get("product_id"))
        _item = None
        for item in cart.items:
            if item.product == product:
                qty = item.quantity
                _item = item
        if qty>1:
            cart.set_quantity(product, quantity=qty - 1)
        else:
            return JsonResponse({
                "error": 1,
                "message": "Quantity can't be decremented",
                "qty": _item.quantity,
                "item_subtotal": _item.subtotal,
                "total": cart.total,
                "count": cart.count,
            })
        return JsonResponse(
            {
                "error": 0,
                "message": "Quantity has been incremented",
                "qty": _item.quantity,
                "item_subtotal": _item.subtotal,
                "total": cart.total,
                "count": cart.count,
            }
        )
    except:
        return JsonResponse({"error": 1})


def ajax_calculate_fp_hash(request):
    try:
        x_login = request.GET.get("x_login")
        x_fp_sequence = request.GET.get("x_fp_sequence")
        x_amount = request.GET.get("x_amount")
        x_currency_code = request.GET.get("x_currency_code")
        x_fp_timestamp, x_fp_hash = calculate_fp_hash(
            x_login, x_fp_sequence, x_amount, x_currency_code
        )
        return JsonResponse(
            {"error": 0, "message": "", "x_amount": x_amount,
             "x_fp_timestamp": x_fp_timestamp, "x_fp_hash": x_fp_hash}
        )
    except:
        return JsonResponse({"error": 1})


def ajax_send_sponsorship_form(request):
    children_name = request.POST.get("children_name", "")
    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")
    address = request.POST.get("address", "")
    city = request.POST.get("city", "")
    state = request.POST.get("state", "")
    zip_code = request.POST.get("zip", "")
    country = request.POST.get("country", "")
    email = request.POST.get("email", "")
    phone = request.POST.get("phone", "")

    config = SiteConfiguration.get_solo()

    if (
            first_name
            and last_name
            and address
            and city
            and state
            and zip_code
            and country
            and email
            and phone
    ):
        try:
            _message = """
            Children Name: %s
            First Name: %s
            Last Name: %s
            Address: %s
            City: %s
            State: %s
            Zip: %s
            Country: %s
            Email: %s
            Phone: %s
            """ % (
                children_name,
                first_name,
                last_name,
                address,
                city,
                state,
                zip_code,
                country,
                email,
                phone,
            )
            send_mail(
                "Children Sponsorship Form", _message, None, config.get_email_list()
            )
        except:
            return JsonResponse({"error": 1, "message": "Invalid header found."})
        return JsonResponse({"error": 0, "message": "success"})
    else:
        return JsonResponse(
            {"error": 1, "message": "Make sure all fields are entered and valid."}
        )


def ajax_send_contact_form(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")

        config = SiteConfiguration.get_solo()
        email_list= config.get_email_list()
        print(email_list)

        if first_name and last_name and email and message:
            try:
                _message = """
                    First Name: %s
                    Last Name: %s
                    Email: %s
                    Message: %s
                    """ % (
                    first_name,
                    last_name,
                    email,
                    message,
                )
                print(_message)
                send_mail("Children Sponsorship Form", _message,None ,config.get_email_list())

            except Exception as e:
                print(e)
                return JsonResponse({"error": 1, "message": "Invalid header found."})
            return JsonResponse({"error": 0, "message": "success"})
        else:
            print('else')
            return JsonResponse(
                {"error": 1, "message": "Make sure all fields are entered and valid."}
            )


@login_required
def ajax_send_donate_form(request):
    email = request.POST.get("x_email", "")
    first_name = request.POST.get("x_first_name", "")
    last_name = request.POST.get("x_last_name", "")
    address = request.POST.get("x_address", "")
    city = request.POST.get("x_city", "")
    state = request.POST.get("x_state", "")
    zip_code = request.POST.get("x_zip", "")
    country = request.POST.get("x_country", "")
    phone = request.POST.get("x_phone", "")
    amount = request.POST.get("x_amount", "")
    description = request.POST.get("x_description", "")

    fp_sequence = request.POST.get("x_fp_sequence", "")

    save_address = request.POST.get("save_address", "")

    config = SiteConfiguration.get_solo()

    x_login = settings.EXACT_X_LOGIN
    x_fp_sequence = 597634
    x_currency_code = "CAD"
    x_fp_timestamp, x_fp_hash = calculate_fp_hash(
        x_login, x_fp_sequence, amount, x_currency_code
    )

    # Save to DB
    CheckoutRequest.objects.create(
        email=email,
        first_name=first_name,
        last_name=last_name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        country=country,
        phone=phone,
        amount=amount,
        description=description,
        typ=CheckoutRequest.DONATE,
        user=request.user,
        timestamp=x_fp_timestamp,
        fp_sequence=fp_sequence,
        save_address=bool(save_address),
    )

    try:
        _message = """
            Email: %s
            First Name: %s
            Last Name: %s
            Address: %s
            City: %s
            State: %s
            Zip: %s
            Country: %s
            Phone: %s
            Amount: %s
            Description: %s
            """ % (
            email,
            first_name,
            last_name,
            address,
            city,
            state,
            zip_code,
            country,
            phone,
            amount,
            description,
        )
        send_mail("AOJ Donate Form", _message, None, config.get_email_list())
    except:
        return JsonResponse({"error": 1, "message": "Invalid header found."})
    return JsonResponse({"error": 0, "message": "success",
                         "x_fp_timestamp": x_fp_timestamp, "x_fp_hash": x_fp_hash})


@login_required
def ajax_send_checkout_form(request):
    email = request.POST.get("x_email", "")
    first_name = request.POST.get("x_first_name", "")
    last_name = request.POST.get("x_last_name", "")
    address = request.POST.get("x_address", "")
    city = request.POST.get("x_city", "")
    state = request.POST.get("x_state", "")
    zip_code = request.POST.get("x_zip", "")
    country = request.POST.get("x_country", "")
    phone = request.POST.get("x_phone", "")
    amount = request.POST.get("x_amount", "")
    description = request.POST.get("x_description", "")

    fp_timestamp = request.POST.get("x_fp_timestamp", "")
    fp_sequence = request.POST.get("x_fp_sequence", "")

    save_address = request.POST.get("save_address", "")

    items_str = ""
    items = request.POST.getlist("x_line_item")

    try:
        for item in items:
            splitted_item = item.split("<|>")
            pr_id = splitted_item[0]
            pr_name = splitted_item[1]
            pr_qty = splitted_item[3]
            pr_price = splitted_item[4]
            items_str += """
                Product id: %s
                Product name: %s
                Product quantity: %s
                Product price: %s
                ------------------
            """ % (
                pr_id,
                pr_name,
                pr_qty,
                pr_price,
            )
    except:
        pass

    x_login = settings.EXACT_X_LOGIN
    x_fp_sequence = 959804
    x_currency_code = "CAD"
    x_fp_timestamp, x_fp_hash = calculate_fp_hash(
        x_login, x_fp_sequence, amount, x_currency_code
    )

    # Save to DB
    CheckoutRequest.objects.create(
        email=email,
        first_name=first_name,
        last_name=last_name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        country=country,
        phone=phone,
        amount=amount,
        description=description,
        items=items_str,
        typ=CheckoutRequest.CHECKOUT,
        user=request.user,
        timestamp=fp_timestamp,
        fp_sequence=fp_sequence,
        save_address=bool(save_address),
    )

    # Send email
    config = SiteConfiguration.get_solo()

    try:
        _message = """
            Email: %s
            First Name: %s
            Last Name: %s
            Address: %s
            City: %s
            State: %s
            Zip: %s
            Country: %s
            Phone: %s
            Amount: %s
            Description: %s

            """ % (
            email,
            first_name,
            last_name,
            address,
            city,
            state,
            zip_code,
            country,
            phone,
            amount,
            description,
        )
        _message += items_str
        send_mail("AOJ Checkout Form", _message, None, config.get_email_list())
    except:
        return JsonResponse({"error": 1, "message": "Invalid header found."})
    return JsonResponse({"error": 0, "message": "success",
                         "x_fp_timestamp": x_fp_timestamp, "x_fp_hash": x_fp_hash})


def setlang_view(request):
    response = HttpResponseRedirect(request.META.get("HTTP_REFERER", "newindex"))
    print(response)
    lang = request.GET.get("lang", None)
    print(lang)
    if lang == "en":
        response.delete_cookie("googtrans")
        
    else:
        if settings.SESSION_COOKIE_DOMAIN:
            try:
                response.set_cookie("googtrans", urllib.parse.quote_plus("/auto/" + lang),domain=settings.SESSION_COOKIE_DOMAIN)
            except:
                response.set_cookie("googtrans", urllib.quote_plus("/auto/" + lang),domain=settings.SESSION_COOKIE_DOMAIN)
        else:
            try:
                response.set_cookie("googtrans", urllib.parse.quote_plus("/auto/" + lang))
            except:
                response.set_cookie("googtrans", urllib.quote_plus("/auto/" + lang))
    return response


def ajax_dropdown(request):
    if request.method == 'GET':
        country = request.GET['country']
        videos = Media.objects.filter(country=country)[0:4]
        data_list = []
        for video in videos:
            video_new=video.video.replace("watch?v=","embed/")
            data_list.append(video_new)
        data_dict = {'dataresponse': data_list}
        return JsonResponse(data_dict)

def ajax_dropdown_list(request):
    if request.method == 'GET':
        country = request.GET['country']
        videos = Media.objects.filter(country=country)
        data_list = []
        for video in videos:
            video_new=video.video.replace("watch?v=","embed/")
            data_list.append(video_new)
        data_dict = {'dataresponse': data_list}
        return JsonResponse(data_dict)
