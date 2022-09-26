from django import template

from carton.cart import Cart

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
    try:
        req = context['request']
        cart = Cart(req.session, session_key=None)
        curr_page = req.resolver_match.url_name
    except:
        return {'missions': Mission.objects.all(), 'aboutpages': AboutPage.objects.all()}
    return {'curr_page': curr_page, 'path': req.path, 'items_count': cart.count, 'user': req.user,
            'missions': Mission.objects.all(), 'aboutpages': AboutPage.objects.all()}

# @register.inclusion_tag('aoj_app/demo/footer.html', takes_context=True)


@register.inclusion_tag('aoj_app/demo/header.html', takes_context=True)
# @register.inclusion_tag('aoj_app/nav_mobile.html', takes_context=True)
def get_mobile_nav(context):
    req = context['request']
    cart = Cart(req.session, session_key=None)
    curr_page = req.resolver_match.url_name
    print(curr_page)
    return {'curr_page': curr_page, 'path': req.path, 'items_count': cart.count, 'user': req.user,
            'missions': Mission.objects.all(), 'aboutpages': AboutPage.objects.all()}
