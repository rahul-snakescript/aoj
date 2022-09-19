from django.contrib import admin

# from authtools.models import User
# from authtools.admin import NamedUserAdmin, BASE_FIELDS
from solo.admin import SingletonModelAdmin
from .models import AuthUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from aoj.aoj_app.views import HistoryView

from .models import *



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name','address', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','address','city','state','country','zip_code')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(AuthUser, UserAdmin)


class CheckoutRequestInline(admin.TabularInline):
    model = CheckoutRequest
    fields = ["amount", "created_at", "typ", "description", "paid"]
    readonly_fields = ["amount", "created_at", "typ", "description", "paid"]
    show_change_link = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# @admin.register(User)
# class NamedUserAdminReplaced(NamedUserAdmin):
#     inlines = [CheckoutRequestInline]
#     fieldsets = (BASE_FIELDS,)

# @admin.register(AuthUser)
# class UserAdmin(admin.ModelAdmin):
#     list_display= ('email','first_name','country','state','address')


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

@admin.register(AboutHistory)
class StaffAdmin(admin.ModelAdmin):
    list_display= ['title','body']

@admin.register(AboutMission)
class StaffAdmin(admin.ModelAdmin):
    list_display= ['title','body']
