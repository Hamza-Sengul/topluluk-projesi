from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils.text import slugify

class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/')
    caption = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.caption if self.caption else f"Resim {self.id}"

class SiteContent(models.Model):
    divider_image_1 = models.ImageField(upload_to='site_images/', blank=True, null=True)
    divider_image_2 = models.ImageField(upload_to='site_images/', blank=True, null=True)
    logo = models.ImageField(upload_to='site_images/', blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    about_us = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Site Content"
    

class Event(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.event.name}"

class Announcement(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField()

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='project_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Community(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    about_us = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    events = models.TextField(blank=True, null=True) 
    announcements = models.TextField(blank=True, null=True) 
    admin_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='community')
    is_published = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Community(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    about_us = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    admin_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='community')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CommunityEvent(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=200)
    details = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ({self.community.name})"
    

class CommunityAnnouncement(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='announcements')
    name = models.CharField(max_length=200)
    details = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.community.name})"
    

class CommunityEventRegistration(models.Model):
    event = models.ForeignKey('CommunityEvent', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    student_number = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20, blank=True, null=True) 
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.event.name})"
    
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    slug = models.SlugField(unique=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CommunityImage(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='community_images/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.community.name} - {self.description or 'Image'}"
