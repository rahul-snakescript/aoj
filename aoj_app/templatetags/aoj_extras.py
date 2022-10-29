from email.header import Header
from re import sub
from django import template

from carton.cart import Cart
from aoj_app.models import ExistingPageSubLink
from aoj_app.models import ExistingPageLink
from aoj_app.models import HeaderLinks, Subheader

from aoj_app.models import SiteConfiguration, Mission, AboutPage

register = template.Library()


@register.simple_tag()
def get_site_config():
    config = SiteConfiguration.objects.first()
    return config


@register.simple_tag(takes_context=True)
def get_product_count_in_cart(context, product):
    req = context['request']
    cart = Cart(req.session, session_key=None)
    _item = None
    for item in cart.items:
        if item.product == product:
            _item = item
    return _item.quantity

# @register.inclusion_tag('aoj_app/nav_desktop.html', takes_context=True)
# @register.inclusion_tag('aoj_app/demo/footer.html', takes_context=True)


@register.inclusion_tag('aoj_app/demo/header.html', takes_context=True)
def get_desktop_nav(context):
    req = context['request']
    cart = Cart(req.session, session_key=None)
    curr_page = req.resolver_match.url_name
    drop_dict={}
    header_list=[]
    header=HeaderLinks.objects.all()
    for data in header:
        try:
            subheader=Subheader.objects.filter(mainLink=data)
            if subheader:
                drop_dict[data]=subheader
            else:
                header_list.append(data)
        except:
            header_list.append(data)
    
    drop_new_dict={}
    header_new_list=[]
    header=ExistingPageLink.objects.all()
    for data in header:
        try:
            subheader=ExistingPageSubLink.objects.filter(existingpage=data)
            if subheader:
                drop_new_dict[data]=subheader
            else:
                drop_new_dict[data]=None
        except:
            drop_new_dict[data]=None

    print(drop_dict)
    print(curr_page)
    print(drop_new_dict)
    return {'curr_page': curr_page, 'path': req.path, 'items_count': cart.count, 'user': req.user,
            'missions': Mission.objects.all(), 'aboutpages': AboutPage.objects.all(),'drop_dict':drop_dict,'header_list':header_list,'header_new_list':header_new_list,'drop_new_dict':drop_new_dict,'headers_links':header}

# @register.inclusion_tag('aoj_app/demo/footer.html', takes_context=True)


@register.inclusion_tag('aoj_app/demo/header.html', takes_context=True)
# @register.inclusion_tag('aoj_app/nav_mobile.html', takes_context=True)
def get_mobile_nav(context):
    req = context['request']
    cart = Cart(req.session, session_key=None)
    curr_page = req.resolver_match.url_name
    return {'curr_page': curr_page, 'path': req.path, 'items_count': cart.count, 'user': req.user,
            'missions': Mission.objects.all(), 'aboutpages': AboutPage.objects.all()}
