from django.conf.urls import url, include

from . views import *

api_patterns = [
    url(r"^remove_from_cart/$", ajax_remove_from_cart, name="ajax_remove_from_cart"),
    url(r"^add_to_cart/$", ajax_add_to_cart, name="ajax_add_to_cart"),
    url(r"^show_cart/$", ajax_show_cart, name="ajax_show_cart"),
    url(
        r"^product_change_quantity/$",
        ajax_product_change_quantity,
        name="ajax_product_change_quantity",
    ),
    url(
        r"^product_increment_quantity/$",
        ajax_product_increment_quantity,
        name="ajax_product_increment_quantity",
    ),
    url(
        r"^product_decrement_quantity/$",
        ajax_product_decrement_quantity,
        name="ajax_product_decrement_quantity",
    ),
    url(r"^calculate_fp_hash/$", ajax_calculate_fp_hash, name="ajax_calculate_fp_hash"),
    url(r"^send_donate_form/$", ajax_send_donate_form, name="ajax_send_donate_form"),

    url(
        r"^send_sponsorship_form/$",
        ajax_send_sponsorship_form,
        name="ajax_send_sponsorship_form",
    ),

    url(r"^send_contact_form/$", ajax_send_contact_form, name="ajax_send_contact_form"),
    url(r"^send_donate_form/$", ajax_send_donate_form, name="ajax_send_donate_form"),
    url(
        r"^send_checkout_form/$",
        ajax_send_checkout_form,
        name="ajax_send_checkout_form",
    ),
    url(r"send_drop_value/$",ajax_dropdown, name='ajaxdropdown'),
    url(r"send_drop_list_value/$",ajax_dropdown_list, name='ajaxdropdown_list'),
]

urlpatterns = [
    url(r"^api/", include(api_patterns)),
    url(r"^redactor/", include("redactor.urls")),
    url(r"^accounts/register/$", RegisterView.as_view(), name="register"),
    url(r"^accounts/", include("authtools.urls")),
    url(r"^ckeditor/", include("ckeditor_uploader.urls")),


#view urls
    url(r"^$", NewIndexView.as_view(), name="newindex"),
    url(r"^setlang/$", setlang_view, name="setlang"),
    url(
        r"^login/$",
        UserLogInView.as_view(),
        name="login",
    ),
     url(
        r"^register/$",
        RegisterView.as_view(),
        name="register",
    ),
    url('logout',LogoutView.as_view(next_page='newindex'),name='logout'),

#catelogue
    url(
        r"^catalogue/$",
        CatalogueView.as_view(),
        name="catalogue",
    ),

#cart
    url(r"^cart/$", CartView.as_view(), name="cart"),

#checkout
    url(r"^checkout/$", CheckoutView.as_view(), name="checkout"),
    url(r"^silentpost/$", SilentPostView.as_view(), name="silent_post"),

#donate
    url(r"^donate/$", DonateView.as_view(), name="donate"),

#media
    url(r"^aoj-media/$", MediaView.as_view(), name="media"),

#contact us
    url(
        r"^contact-us/$",
        ContactUsView,
        name="contact_us",
    ),

#children urls
    url(r"^children/$", ChildrenView.as_view(), name="children"),
    url(
        r"^children/(?P<slug>[-\w]+)/$",
        ChildrenDetailView.as_view(),
        name="children_detail",
    ),

#Director's Blog
    url(r"^blogs/$", BlogView.as_view(), name="blog"),
    url(
        r"^blogs/(?P<slug>[-\w]+)/$",
        BlogDetailView.as_view(),
        name="blog_detail",
    ),
    
#magazine    
    url(r"^magazine/$", MagazineView.as_view(), name="magazine"),
    url(
        r"^magazine/(?P<slug>[-\w]+)/$",
        MagazineDetailView.as_view(),
        name="magazine_detail",
    ),

# ABOUT
    
    url(
        r"^about/staff/$",
        AboutStaffView.as_view(),
        name="staff",
    ),
    url(
        r"^about/behave/$",
        AboutbehaveView.as_view(),
        name="behave",
    ),
    url(
        r"^about/fund-policy/$",
        AboutFundPolicyView.as_view(),
        name="fund_policy",
    ),
    url(
        r"^about/history/$",
        HistoryView.as_view(),
        name="history",
    ),
    url(
        r"^about/mission/$",
        MissionView.as_view(),
        name="mission",
    ),
    url(
        r"^about_us/(?P<slug>[-\w]+)/$",
        AboutPageDetailView.as_view(),
        name="aboutpage_detail",
    ),
    
#Mission Pages
    url(
        r"^mission/(?P<slug>[-\w]+)/$",
        MissionDetailView.as_view(),
        name="mission_detail",
    ),
    url(
        r"^missions/haiti/$",
        MissionHaitiView.as_view(template_name="aoj_app/demo/mission/mission_haiti.html"),
        name="mission_haiti",
    ),
    url(
        r"^missions/kenya/$",
        MissionKenyaView.as_view(template_name="aoj_app/demo/mission/mission_kenya.html"),
        name="mission_kenya",
    ),
    url(
        r"^missions/guatemala/$",
        MissionGuatemalaView.as_view(template_name="aoj_app/demo/mission/guatemala_mission.html"),
        name="guatemala_mission",
    ),

# TEAMS
    url(
        r"^consider-serving/$",
        TeamsConsiderView.as_view(),
        name="t_consider",
    ),
    url(
        r"^training/$",
        TeamsTrainingView.as_view(),
        name="t_training",
    ),
    url(
        r"^calendar/$",
        TeamsCalenderView.as_view(template_name="aoj_app/demo/teams/teams_calender.html"),
        name="t_calender",
    ),
    url(
        r"^resources/$",
        TeamsResourceView.as_view(),
        name="t_resource",
    ),
    url(
        r"^team-blogs/$",
        TeamsBlogView.as_view(),
        name="t_blog",
    ),

#latest news detail pages
    url(
        r"^latestnews/(?P<slug>[-\w]+)/$",
        LatestNewsPageDetailView.as_view(),
        name="latest_news",
    ),
    url(
        r"^school-official-dedication/$",
        TemplateView.as_view(
            template_name="aoj_app/demo/school_official_dedication.html"
        ),
        name="school_official_dedication",
    ),

#new nav bar items
    url(
        r"^navbar/(?P<slug>[-\w]+)/$",
        HeaderPageDetailView.as_view(),
        name="navbar_items",
    ),
    url(
        r"^subnavbar/(?P<slug>[-\w]+)/$",
        SubHeaderPageDetailView.as_view(),
        name="sub_navbar_items",
    ),
]