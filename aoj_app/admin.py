from django.contrib import admin

from authtools.models import User
from authtools.admin import NamedUserAdmin, BASE_FIELDS
from solo.admin import SingletonModelAdmin

from .models import *

admin.site.unregister(User)


class CheckoutRequestInline(admin.TabularInline):
    model = CheckoutRequest
    fields = ["amount", "created_at", "typ", "description", "paid"]
    readonly_fields = ["amount", "created_at", "typ", "description", "paid"]
    show_change_link = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class NamedUserAdminReplaced(NamedUserAdmin):
    inlines = [CheckoutRequestInline]
    fieldsets = (BASE_FIELDS,)


class ChildrenAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class MagazineAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class BlogEntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CheckoutRequestAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "amount", "typ", "paid")
    readonly_fields = ("typ", "user", "timestamp", "fp_sequence", "save_address")


admin.site.register(Product)
admin.site.register(Country)
admin.site.register(Media)
admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(Magazine, MagazineAdmin)
admin.site.register(Children, ChildrenAdmin)
admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(CheckoutRequest, CheckoutRequestAdmin)


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    exclude = ["slug"]

    class Media:
        css = {
            'all': ('admin/ckeditor_admin.css',)
        }


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    exclude = ["slug"]

    class Media:
        css = {
            'all': ('admin/ckeditor_admin.css',)
        }

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display= ['staff_image','staff_name','staff_position']

@admin.register(WhatWeBelieve)
class StaffAdmin(admin.ModelAdmin):
    list_display= ['title','body']

@admin.register(FundPolicy)
class StaffAdmin(admin.ModelAdmin):
    list_display= ['title','body','foot']
