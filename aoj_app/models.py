# from __future__ import unicode_literals
# from email.quoprimime import body_check

from audioop import add
from itertools import count
from unittest.util import _MAX_LENGTH
import uuid
from xml.dom import ValidationErr
try:
    import urlparse
except:
    from urllib.parse import urlparse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.template.defaultfilters import slugify
try:
    from django.core.urlresolvers import reverse
except:
    from django.urls import reverse
# from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from solo.models import SingletonModel
from redactor.fields import RedactorField
from bs4 import BeautifulSoup
from colorful.fields import RGBColorField
from ckeditor_uploader.fields import RichTextUploadingField


def upload_product_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "products/%s" % filename


def upload_children_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "children/%s" % filename


def upload_magazine_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "magazine/%s" % filename


def upload_banner_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "banner/%s" % filename

def upload_staff_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "staff/%s" % filename

def upload_teamblog_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "teamsblog/%s" % filename

def upload_teamconsider_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "teamsconsider/%s" % filename

def upload_teamtraining_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "teamstraining/%s" % filename

def upload_teamresource_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "teamsresource/%s" % filename

def upload_newscover_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "latestnews/%s" % filename

def upload_blogentry_image_to(instance, filename):
    ext = filename.split(".")[-1]
    uuid_hash = str(uuid.uuid4())[:8]
    filename = "{0}.{1}".format(uuid_hash, ext)
    return "blogentry/%s" % filename


"""
MODELS
"""

class AuthUserManager(BaseUserManager):
    def create_user(self, email, first_name,last_name,address,phone_number,city=None,state=None,country=None,zip_code=None,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number
        )
        if city:
                user.city=city
        if state:
                user.state=state
        if country:
                user.country=country
        if zip_code:
                user.zip_code=zip_code

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,first_name,last_name,address,phone_number,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone_number=phone_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class AuthUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # password=models.CharField(max_length=15,attrs={'input_type':'password'})
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    address=models.CharField(max_length=256)
    city=models.CharField(max_length=200,blank=True,null=True)
    state=models.CharField(max_length=200,blank=True,null=True)
    zip_code= models.CharField(max_length=200,blank=True,null=True)
    country=models.CharField(max_length=200,blank=True,null=True)
    phone_number=models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AuthUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','address','phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Product(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=False, null=False, default=0.0
    )
    image = models.ImageField(upload_to=upload_product_image_to, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["-created_date"]


class Country(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)

    # def __unicode__(self):
    #     return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class Media(models.Model):
    country = models.ForeignKey(Country)
    video = models.URLField(
        max_length=201, blank=False, null=False, help_text="Youtube video link"
    )
    created_date = models.DateTimeField(default=timezone.now)

    def get_youtube_embed_url(self):
        embed_url = None
        if "youtube" in self.video:
            par = urlparse.parse_qs(urlparse.urlparse(self.video).query)
            vid = par["v"][0]
            if vid:
                embed_url = "https://www.youtube.com/embed/%s" % vid
        elif "vimeo" in self.video:
            vimeo_vid = self.video.split("/")[-1]
            embed_url = "https://player.vimeo.com/video/%s" % vimeo_vid
        return embed_url

    def __str__(self):
        return self.video

    class Meta:
        verbose_name_plural = "Media"
        ordering = ["-created_date"]

#add

class Magazine(models.Model):
    title = models.CharField(max_length=128, blank=False, null=False)
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    image = models.ImageField(upload_to=upload_magazine_image_to, blank=True, null=True)
    Magazine_detail_seo_title=models.CharField(max_length=256,blank=True,null=True)
    Magazine_detail_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    created_date = models.DateTimeField(default=timezone.now)
    iframe_link = models.URLField(
        max_length=301, blank=True, null=True, help_text="Magazine link"
    )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Magazine, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Magazine"
        ordering = ["-created_date"]


class Children(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    born = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=128, blank=False, null=False)
    detail_page_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    detail_page_seo_title=models.CharField(max_length=256,blank=True,null=True)
    country = models.ForeignKey(Country)
    description = models.TextField(blank=True, null=True, max_length=2000)
    checked_out = models.BooleanField(default=False)
    image1 = models.ImageField(
        upload_to=upload_children_image_to, blank=True, null=True
    )
    image2 = models.ImageField(
        upload_to=upload_children_image_to, blank=True, null=True
    )
    created_date = models.DateTimeField(default=timezone.now)

    def get_avatar(self):
        if self.image1:
            return self.image1.url
        elif self.image2:
            return self.image2.url
        else:
            return "none"

    def get_short_name(self):
        return self.name.split()[0]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Children, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("children_detail", kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Children"
        ordering = ["-created_date"]


class BlogEntry(models.Model):
    Directors_blog = 'DB'
    TeamBlog = 'TB'
    
    BLOG_TYPE = [
        (Directors_blog, "Director's Blog"),
        (TeamBlog, "Team's Blog"),
    ]
    category=models.CharField(max_length=50,choices=BLOG_TYPE,default=Directors_blog)
    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    short_description = models.TextField(blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    cover=models.ImageField(upload_to=upload_blogentry_image_to,blank=True,null=True)
    body = RedactorField(verbose_name="Body", allow_image_upload=True)
    created_date = models.DateTimeField(default=timezone.now)
    featured=models.BooleanField(default=False)

    def get_first_image(self):
        soup = BeautifulSoup(self.body, "html.parser")
        img = soup.find("img")
        if img:
            return img["src"]
        else:
            return None

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Blog Entries"
        ordering = ["-created_date"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogEntry, self).save(*args, **kwargs)


class SiteConfiguration(SingletonModel):
    singleton_instance_id = 24
    email_list = models.CharField(max_length=1000, blank=True, null=True)
    site_phone = models.CharField(max_length=100, blank=True, null=True)
    facebook_page = models.URLField(max_length=201, blank=True, null=True)
    youtube_link = models.URLField(max_length=201, blank=True, null=True)
    twitter_link=models.URLField(max_length=201, blank=True, null=True)
    site_email = models.EmailField(blank=True, null=True)
    home_seo_title=models.CharField(max_length=256,null=True,blank=True)
    banner_image = models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    heading_color = RGBColorField()
    #for director's Blog page
    directors_blog_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    directors_blog_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # directors_blog_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)
    
    Magazine_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    Magazine_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # Magazine_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)
    
    Media_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    Media_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # Media_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)
    
    Latest_news_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    Latest_news_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # Latest_news_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)
    
    children_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    children_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # children_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)

    catalogue_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    catalogue_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # catalogue_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)
    
    contact_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    contact_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # contact_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)

    dashboard_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    dashboard_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # dashboard_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)

    cart_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    cart_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # cart_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)

    checkout_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    checkout_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # checkout_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)

    donate_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    donate_seo_title=models.CharField(max_length=256,blank=True,null=True)
    donate_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)

    sponsor_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    sponsor_seo_title=models.CharField(max_length=256,blank=True,null=True)
    sponsor_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)

    about_staff_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    about_staff_seo_title=models.CharField(max_length=256,blank=True,null=True)
    # about_staff_name_in_navbar=models.CharField(max_length=256,blank=True,null=True)

    login_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    login_seo_title=models.CharField(max_length=256,blank=True,null=True)

    register_banner_image=models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    register_seo_title=models.CharField(max_length=256,blank=True,null=True)


    def __unicode__(self):
        return "Site Configuration"

    def get_email_list(self):
        if self.email_list:
            return [x.strip() for x in self.email_list.split(",")]
        else:
            return []

    class Meta:
        verbose_name = "Site Configuration"


class CheckoutRequest(models.Model):
    CHECKOUT = "CHECKOUT"
    DONATE = "DONATE"
    TYP_CHOICES = ((CHECKOUT, "Checkout"), (DONATE, "Donate"))

    email = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    items = models.TextField(blank=True, null=True)
    typ = models.CharField(max_length=15, choices=TYP_CHOICES, default=CHECKOUT)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(AuthUser, blank=True, null=True)
    # to determine "paid", from silent post
    timestamp = models.CharField(max_length=15)
    fp_sequence = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)

    save_address = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email


class Mission(models.Model):
    name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    # top_section = models.TextField(blank=True)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    body = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now_add=True)
    country=models.ForeignKey(Country,on_delete=models.CASCADE,blank=True,null=True)
    is_active=models.BooleanField(default=True)
    name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Create New Mission Page"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Mission, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("mission_detail", args=[self.slug])

class MissionPageAttributes(models.Model):
    title=models.CharField(max_length=50)
    value=models.CharField(max_length=50)
    country=models.ForeignKey(Country,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title+" of "+str(self.country)
    class Meta:
        verbose_name_plural = "Mission Page Attributes"


class AboutPage(models.Model):
    name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    body = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now_add=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)
    # sno=models.IntegerField(blank=True,null=True)
    # is_active=models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Create New About Page"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(AboutPage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("aboutpage_detail", args=[self.slug])

class AboutStaff(models.Model):
    staff_name = models.CharField(max_length=200, blank=False)
    staff_image = models.ImageField(upload_to="",blank=True)
    staff_position = models.CharField(max_length=200,blank=False)
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)
     
    class Meta:
        verbose_name_plural = "Staff"
        ordering = ["staff_name"]

    def __unicode__(self):
        return self.staff_name

class AboutWhatWeBelieve(models.Model):
    title=models.CharField(max_length=200)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    body=RichTextUploadingField()
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)

    class Meta:
        verbose_name_plural = "What We Believe"

    def __unicode__(self):
        return self.title

class AboutFundPolicy(models.Model):
    title=models.CharField(max_length=200)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    body=RichTextUploadingField()
    Sub_Text=models.CharField(max_length=200,blank=True,null=True)
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "Fund Policy"

    def __unicode__(self):
        return self.title

class AboutHistory(models.Model):
    title=models.CharField(max_length=200)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    body=RichTextUploadingField()
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)

    class Meta:
        verbose_name_plural = "History"

    def __unicode__(self):
        return self.title

class AboutMission(models.Model):
    title=models.CharField(max_length=200)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    body=RichTextUploadingField()
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Mission"

    def __unicode__(self):
        return self.title

class TeamsPage(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)

    class Meta:
        ordering = ["seo_title"]

    def __unicode__(self):
        return self.seo_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.seo_title)
        super(TeamsPage, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("teamspage_detail", args=[self.slug])

# class TeamsBlog(models.Model):
#     # sno = models.IntegerField(null=True,blank=True)
#     # seo_detail=models.OneToOneField(TeamsPage,on_delete=models.DO_NOTHING,blank=True)
#     title=models.CharField(max_length=50)
#     image=models.ImageField(upload_to=upload_teamblog_image_to,blank=True,null=True)
#     description=models.TextField()
#     # is_active=models.BooleanField(default=True)
#     # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)

class TeamsConsider(models.Model):
    # sno = models.IntegerField(null=True,blank=True)
    # seo_detail=models.OneToOneField(TeamsPage,on_delete=models.DO_NOTHING,blank=True)
    title=models.CharField(max_length=50,blank=True,null=True)
    image=models.ImageField(upload_to=upload_teamconsider_image_to)
    description=models.TextField(blank=True,null=True)
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)
    class Meta:
        verbose_name_plural = "Consider Serving"

class TeamsTraining(models.Model):
    # sno = models.IntegerField(null=True,blank=True)
    # seo_detail=models.OneToOneField(TeamsPage,on_delete=models.DO_NOTHING,blank=True)
    title=models.CharField(max_length=50,blank=True,null=True)
    media=models.FileField(upload_to=upload_teamtraining_image_to)
    description=models.TextField(blank=True,null=True)
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)
    class Meta:
        verbose_name_plural = "Training"

class TeamsResources(models.Model):
    # sno = models.IntegerField(null=True,blank=True)
    # seo_detail=models.OneToOneField(TeamsPage,on_delete=models.DO_NOTHING,blank=True)
    title=models.CharField(max_length=50,blank=True,null=True)
    media=models.FileField(upload_to=upload_teamresource_image_to)
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)
    class Meta:
        verbose_name_plural = "Resources"
 
class TeamsCalenderDate(models.Model):
    # sno = models.IntegerField(null=True,blank=True)
    # seo_detail=models.OneToOneField(TeamsPage,on_delete=models.DO_NOTHING,blank=True)
    starting_date=models.DateField(auto_now_add=False,auto_now=False)
    ending_date=models.DateField(auto_now_add=False,auto_now=False)
    mission_trip=models.CharField(max_length=100)
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)
    class Meta:
        verbose_name_plural = "Calendar"

class MissionHaiti(models.Model):
    title=models.CharField(max_length=200)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    body=RichTextUploadingField()
    country=models.ForeignKey(Country,on_delete=models.CASCADE,blank=True,null=True)
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)
    class Meta:
        verbose_name_plural = "Haiti"

class MissionKenya(models.Model):
    title=models.CharField(max_length=200)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    body=RichTextUploadingField()
    country=models.ForeignKey(Country,on_delete=models.CASCADE,blank=True,null=True)
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Kenya"

class MissionGuatemala(models.Model):
    title=models.CharField(max_length=200)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    body=RichTextUploadingField()
    country=models.ForeignKey(Country,on_delete=models.CASCADE,blank=True,null=True)
    # is_active=models.BooleanField(default=True)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Guatemala"

class LatestNews(models.Model):
    title=models.CharField(max_length=200)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    slug = models.SlugField(max_length=200, unique=True,blank=True)
    shortdesc=models.CharField(max_length=500)
    cover=models.ImageField(upload_to=upload_newscover_image_to)
    body=RichTextUploadingField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(LatestNews, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("latest_news", args=[self.slug])

class ExistingPageLink(models.Model):
    title=models.CharField(max_length=256)
    link=models.CharField(max_length=256)
    sno=models.IntegerField() 

    class Meta:
        ordering=['sno']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.link[-1]!="/":
            self.link+="/"
        super(ExistingPageLink, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("navbar_itemss", args=[self.link])
    

class ExistingPageSubLink(models.Model):
    existingpage=models.ForeignKey(ExistingPageLink,on_delete=models.CASCADE)
    title=models.CharField(max_length=256)
    link=models.CharField(max_length=256)
    sno=models.IntegerField() 

    class Meta:
        ordering=['sno']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.link[-1]!="/": 
            self.link+="/"
        super(ExistingPageSubLink, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("navbar_itemss", args=[self.link])

class CreateNewPage(models.Model):
    sno = models.IntegerField()
    title=models.CharField(max_length=256)
    body=RichTextUploadingField(blank=True,null=True)
    slug = models.SlugField(max_length=200, unique=True,blank=True,null=True)
    # link = models.CharField(max_length=256,blank=True,null=True)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    is_active=models.BooleanField(default=False)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Create New Page"
        ordering=['sno']

    def __str__(self):
        return self.title

    def clean(self):
        if not self.body:
            if self.seo_title or self.banner_image:
                raise ValidationError('Header without body has no need for seo_title or banner_image')
        return super(CreateNewPage,self).clean()


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) 
        super(CreateNewPage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("navbar_items", args=[self.slug])


class CreateNewSubPage(models.Model):
    mainLink= models.ForeignKey(CreateNewPage,on_delete=models.CASCADE)
    # link = models.CharField(max_length=256,blank=True,null=True)
    seo_title=models.CharField(max_length=256,blank=True,null=True)
    banner_image=models.ImageField(upload_to=upload_banner_image_to,blank=True,null=True)
    sno = models.IntegerField()
    title=models.CharField(max_length=256)
    body=RichTextUploadingField()
    slug = models.SlugField(max_length=200, unique=True,blank=True)
    is_active=models.BooleanField(default=False)
    # name_in_dropdown=models.CharField(max_length=256,blank=True,null=True)
    

    class Meta:
        verbose_name_plural = "Create New Sub Page"
        ordering=['sno']

    def __str__(self):
        return self.title+' is a sub part of '+str(self.mainLink)

    def clean(self):
        header=CreateNewPage.objects.get(pk=self.mainLink.id)
        if header.body:
            raise ValidationError('Main link with body cannot be a sublink')
        return super(CreateNewSubPage,self).clean()
        

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(CreateNewPage, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("sub_navbar_items", args=[self.slug])

#dummy

    



