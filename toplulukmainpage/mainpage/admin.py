# admin.py
from django.contrib import admin
from .models import SliderImage,Blog, CommunityImage, SiteContent, Event, Registration, Announcement, Project, Community, CommunityAnnouncement, CommunityEvent, CommunityEventRegistration

admin.site.register(SliderImage)
admin.site.register(SiteContent)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Announcement)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

admin.site.register(Project, ProjectAdmin)

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin_user')
    search_fields = ('name',)

admin.site.register(Community, CommunityAdmin)

class CommunityEventRegistrationInline(admin.TabularInline):
    model = CommunityEventRegistration
    readonly_fields = ['name', 'surname', 'email', 'contact_number', 'student_number', 'is_member'] 


class CommunityEventAdmin(admin.ModelAdmin):
    inlines = [CommunityEventRegistrationInline]
    list_display = ('name', 'community', 'date')
    search_fields = ('name', 'community__name')
    list_filter = ('community', 'date')

class CommunityAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('name', 'community')
    search_fields = ('name', 'community__name')
    list_filter = ('community',)

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin_user', 'is_published')
    search_fields = ('name', 'admin_user__username')
    list_filter = ('is_published',)

admin.site.register(CommunityEvent, CommunityEventAdmin)
admin.site.register(CommunityAnnouncement, CommunityAnnouncementAdmin)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


class CommunityImageInline(admin.TabularInline):
    model = CommunityImage
    extra = 1 


@admin.register(CommunityImage)
class CommunityImageAdmin(admin.ModelAdmin):
    list_display = ('community', 'description', 'image')