from django.conf.urls import url, include

from . views import *

api_patterns = [
    url(r"^add_to_cart/$", ajax_add_to_cart, name="ajax_add_to_cart"),
    url(r"^remove_from_cart/$", ajax_remove_from_cart, name="ajax_remove_from_cart"),
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
]

urlpatterns = [
    url(r"^$", IndexView.as_view(), name="index"),
    url(r"^setlang/$", setlang_view, name="setlang"),
    url(
        r"^contact/$",
        TemplateView.as_view(template_name="aoj_app/pages/contact.html"),
        name="contact",
    ),
    url(r"^aoj-media/$", MediaView.as_view(), name="media"),
    url(r"^donate/$", DonateView.as_view(), name="donate"),
    url(r"^catalogue/$", CatalogueView.as_view(), name="catalogue"),
    url(r"^cart/$", CartView.as_view(), name="cart"),
    url(r"^checkout/$", CheckoutView.as_view(), name="checkout"),
    url(r"^silentpost/$", SilentPostView.as_view(), name="silent_post"),
    url(r"^directors-blog/$", BlogView.as_view(), name="blog"),
    url(
        r"^directors-blog/(?P<slug>[-\w]+)/$",
        BlogDetailView.as_view(),
        name="blog_detail",
    ),
    
    url(r"^children/$", ChildrenView.as_view(), name="children"),
    url(
        r"^children/(?P<slug>[-\w]+)/$",
        ChildrenDetailView.as_view(),
        name="children_detail",
    ),
    url(r"^magazine/$", MagazineView.as_view(), name="magazine"),
    url(
        r"^magazine/(?P<slug>[-\w]+)/$",
        MagazineDetailView.as_view(),
        name="magazine_detail",
    ),
    # MISSIONS
    url(
        r"^missions/(?P<slug>[-\w]+)/$",
        MissionDetailView.as_view(),
        name="mission_detail",
    ),
    # ABOUT PAGES
    url(
        r"^about/(?P<slug>[-\w]+)/$",
        AboutPageDetailView.as_view(),
        name="aboutpage_detail",
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
        TemplateView.as_view(template_name="aoj_app/demo/teams_calender.html"),
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
    # ABOUT
    url(
        r"^mission-statement/$",
        TemplateView.as_view(
            template_name="aoj_app/pages/about/mission_statement.html"
        ),
        name="mission_statement",
    ),
    url(
        r"^what-we-believe/$",
        TemplateView.as_view(template_name="aoj_app/pages/about/what_we_believe.html"),
        name="what_we_believe",
    ),
    url(
        r"^funds-policy/$",
        TemplateView.as_view(template_name="aoj_app/pages/about/funds_policy.html"),
        name="funds_policy",
    ),
    url(
        r"^our-history/$",
        TemplateView.as_view(template_name="aoj_app/pages/about/our_history.html"),
        name="our_history",
    ),
    url(
        r"^staff/$",
        TemplateView.as_view(template_name="aoj_app/pages/about/staff.html"),
        name="staff",
    ),
    url(
        r"^school-official-dedication/$",
        TemplateView.as_view(
            template_name="aoj_app/pages/school_official_dedication.html"
        ),
        name="school_official_dedication",
    ),
    url(r"^api/", include(api_patterns)),
    url(r"^redactor/", include("redactor.urls")),
    url(r"^accounts/register/$", RegisterView.as_view(), name="register"),
    url(r"^accounts/", include("authtools.urls")),
    url(r"^ckeditor/", include("ckeditor_uploader.urls")),

#demo urls
    url(r"^demo/$", NewIndexView.as_view(), name="newindex"),
    
    url(
        r"^demo/about/staff/$",
        AboutStaffView.as_view(),
        name="staff",
    ),
    url(
        r"^demo/about/behave/$",
        AboutbehaveView.as_view(),
        name="behave",
    ),
    url(
        r"^demo/about/fund-policy/$",
        AboutFundPolicyView.as_view(),
        name="fund_policy",
    ),
    url(
        r"^demo/contact-us/$",
        ContactUsView.as_view(),
        name="contact_us",
    ),
    url(
        r"^demo/history/$",
        HistoryView.as_view(),
        name="history",
    ),
    url(
        r"^demo/mission/$",
        MissionView.as_view(),
        name="mission",
    ),
     url(
        r"^demo/login/$",
        UserLogInView.as_view(),
        name="login",
    ),
     url(
        r"^demo/register/$",
        RegisterView.as_view(),
        name="register",
    ),
    url('demo/logout',LogoutView.as_view(next_page='newindex'),name='logout'),
    
    url(
        r"^demo/Catalogue/$",
        CatalogueView.as_view(),
        name="Catalogue",
    ),
]