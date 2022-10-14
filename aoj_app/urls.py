# from django.conf.urls import url, include
from django.urls import path,include


from . views import *

api_patterns = [
    path("remove_from_cart/", ajax_remove_from_cart, name="ajax_remove_from_cart"),
    path("add_to_cart/", ajax_add_to_cart, name="ajax_add_to_cart"),
    path("show_cart/", ajax_show_cart, name="ajax_show_cart"),
    path(
        "product_change_quantity/",
        ajax_product_change_quantity,
        name="ajax_product_change_quantity",
    ),
    path(
        "product_increment_quantity/",
        ajax_product_increment_quantity,
        name="ajax_product_increment_quantity",
    ),
    path(
        "product_decrement_quantity/",
        ajax_product_decrement_quantity,
        name="ajax_product_decrement_quantity",
    ),
    path("calculate_fp_hash/", ajax_calculate_fp_hash, name="ajax_calculate_fp_hash"),
    path("send_donate_form/", ajax_send_donate_form, name="ajax_send_donate_form"),

    path(
        "send_sponsorship_form/",
        ajax_send_sponsorship_form,
        name="ajax_send_sponsorship_form",
    ),

    path("send_contact_form/", ajax_send_contact_form, name="ajax_send_contact_form"),
    path("send_donate_form/", ajax_send_donate_form, name="ajax_send_donate_form"),
    path(
        "send_checkout_form/",
        ajax_send_checkout_form,
        name="ajax_send_checkout_form",
    ),
    path(r"send_drop_value/",ajax_dropdown, name='ajaxdropdown'),
]

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("setlang/", setlang_view, name="setlang"),
    path(
        "contact/",
        TemplateView.as_view(template_name="aoj_app/pages/contact.html"),
        name="contact",
    ),
    path("aoj-media/", MediaView.as_view(), name="media"),
    path("donate/", DonateView.as_view(), name="donate"),
    path("catalogue/", CatalogueView.as_view(), name="catalogue"),
    path("cart/", CartView.as_view(), name="cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("silentpost/", SilentPostView.as_view(), name="silent_post"),
    path("directors-blog/", BlogView.as_view(), name="blog"),
    path(
        "directors-blog/(?P<slug>[-\w]+)/",
        BlogDetailView.as_view(),
        name="blog_detail",
    ),
    
    path("children/", ChildrenView.as_view(), name="children"),
    path(
        "children/(?P<slug>[-\w]+)/",
        ChildrenDetailView.as_view(),
        name="children_detail",
    ),
    path("magazine/", MagazineView.as_view(), name="magazine"),
    path(
        "magazine/(?P<slug>[-\w]+)/",
        MagazineDetailView.as_view(),
        name="magazine_detail",
    ),
    # MISSIONS
    path(
        "missions/(?P<slug>[-\w]+)/",
        MissionDetailView.as_view(),
        name="mission_detail",
    ),
    # ABOUT PAGES
    path(
        "about/(?P<slug>[-\w]+)/",
        AboutPageDetailView.as_view(),
        name="aboutpage_detail",
    ),
    
    # TEAMS
    path(
        "consider-serving/",
        TeamsConsiderView.as_view(),
        name="t_consider",
    ),
    path(
        "training/",
        TeamsTrainingView.as_view(),
        name="t_training",
    ),
    path(
        "calendar/",
        TeamsCalenderView.as_view(template_name="aoj_app/demo/teams/teams_calender.html"),
        name="t_calender",
    ),
    path(
        "resources/",
        TeamsResourceView.as_view(),
        name="t_resource",
    ),
    path(
        "team-blogs/",
        TeamsBlogView.as_view(),
        name="t_blog",
    ),
    # ABOUT
    path(
        "mission-statement/",
        TemplateView.as_view(
            template_name="aoj_app/pages/about/mission_statement.html"
        ),
        name="mission_statement",
    ),
    path(
        "what-we-believe/",
        TemplateView.as_view(template_name="aoj_app/pages/about/what_we_believe.html"),
        name="what_we_believe",
    ),
    path(
        "funds-policy/",
        TemplateView.as_view(template_name="aoj_app/pages/about/funds_policy.html"),
        name="funds_policy",
    ),
    path(
        "our-history/",
        TemplateView.as_view(template_name="aoj_app/pages/about/our_history.html"),
        name="our_history",
    ),
    path(
        "staff/",
        TemplateView.as_view(template_name="aoj_app/pages/about/staff.html"),
        name="staff",
    ),
    path(
        "school-official-dedication/",
        TemplateView.as_view(
            template_name="aoj_app/pages/school_official_dedication.html"
        ),
        name="school_official_dedication",
    ),
    path("api/", include(api_patterns)),
    path("redactor/", include("redactor.urls")),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),

#demo paths
    path("demo/", NewIndexView.as_view(), name="newindex"),
    
    path(
        "demo/about/staff/",
        AboutStaffView.as_view(),
        name="staff",
    ),
    path(
        "demo/about/behave/",
        AboutbehaveView.as_view(),
        name="behave",
    ),
    path(
        "demo/about/fund-policy/",
        AboutFundPolicyView.as_view(),
        name="fund_policy",
    ),
    path(
        "demo/contact-us/",
        ContactUsView.as_view(),
        name="contact_us",
    ),
    path(
        "demo/history/",
        HistoryView.as_view(),
        name="history",
    ),
    path(
        "demo/mission/",
        MissionView.as_view(),
        name="mission",
    ),
     path(
        "demo/login/",
        UserLogInView.as_view(),
        name="login",
    ),
     path(
        "demo/register/",
        RegisterView.as_view(),
        name="register",
    ),
    path('demo/logout',LogoutView.as_view(next_page='newindex'),name='logout'),
    
    path(
        "demo/Catalogue/",
        CatalogueView.as_view(),
        name="Catalogue",
    ),
    path(
        "demo/missions/haiti/",
        MissionHaitiView.as_view(template_name="aoj_app/demo/mission/mission_haiti.html"),
        name="mission_haiti",
    ),
    path(
        "demo/missions/kenya/",
        MissionKenyaView.as_view(template_name="aoj_app/demo/mission/mission_kenya.html"),
        name="mission_kenya",
    ),
    path(
        "demo/missions/guatemala/",
        MissionGuatemalaView.as_view(template_name="aoj_app/demo/mission/guatemala_mission.html"),
        name="guatemala_mission",
    ),
]