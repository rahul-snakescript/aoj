# from __future__ import unicode_literals
# from email.quoprimime import body_check

from audioop import add
from itertools import count
import uuid
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

    def __unicode__(self):
        return self.video

    class Meta:
        ordering = ["-created_date"]


class Magazine(models.Model):
    title = models.CharField(max_length=128, blank=False, null=False)
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    image = models.ImageField(upload_to=upload_magazine_image_to, blank=True, null=True)
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
        ordering = ["-created_date"]


class Children(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    born = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=128, blank=False, null=False)
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
    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    body = RedactorField(verbose_name="Body", allow_image_upload=True)
    created_date = models.DateTimeField(default=timezone.now)

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
    site_email = models.EmailField(blank=True, null=True)
    banner_image = models.ImageField(
        upload_to=upload_banner_image_to, blank=True, null=True
    )
    heading_color = RGBColorField()

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
    top_section = models.TextField(blank=True)
    body = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Mission, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("mission_detail", args=[self.slug])


class AboutPage(models.Model):
    name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    body = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(AboutPage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("aboutpage_detail", args=[self.slug])

class Staff(models.Model):
    staff_name = models.CharField(max_length=200, blank=False)
    staff_image = models.ImageField(upload_to="",blank=True)
    staff_position = models.CharField(max_length=200,blank=False)

    class Meta:
        ordering = ["staff_name"]

    def __unicode__(self):
        return self.staff_name

class WhatWeBelieve(models.Model):
    title=models.CharField(max_length=200)
    body=RichTextUploadingField()

    def __unicode__(self):
        return self.title

class FundPolicy(models.Model):
    title=models.CharField(max_length=200)
    body=RichTextUploadingField()
    foot=models.CharField(max_length=200)

    def __unicode__(self):
        return self.title

class AboutHistory(models.Model):
    title=models.CharField(max_length=200)
    body=RichTextUploadingField()

    def __unicode__(self):
        return self.title

class AboutMission(models.Model):
    title=models.CharField(max_length=200)
    body=RichTextUploadingField()

    def __unicode__(self):
        return self.title

class TeamsBlog(models.Model):
    title=models.CharField(max_length=50)
    image=models.ImageField(upload_to=upload_teamblog_image_to,blank=True,null=True)
    description=models.TextField()

class TeamsConsider(models.Model):
    title=models.CharField(max_length=50,blank=True,null=True)
    image=models.ImageField(upload_to=upload_teamconsider_image_to)
    description=models.TextField(blank=True,null=True)

class TeamsTraining(models.Model):
    title=models.CharField(max_length=50,blank=True,null=True)
    media=models.FileField(upload_to=upload_teamtraining_image_to)
    description=models.TextField(blank=True,null=True)

class TeamsResources(models.Model):
    title=models.CharField(max_length=50,blank=True,null=True)
    media=models.FileField(upload_to=upload_teamresource_image_to)











