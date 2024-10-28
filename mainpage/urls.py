from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('register/<int:event_id>/', views.register_event, name='register_event'),
    path('announcement/<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('login/', views.community_login, name='community_login'),
    path('dashboard/', views.community_dashboard_default, name='community_dashboard_default'),
    path('logout/', LogoutView.as_view(next_page='community_login'), name='logout'),
    path('community/<int:community_id>/dashboard/', views.community_dashboard_by_id, name='community_dashboard_by_id'),
    path("certificate/", views.certificate_page, name="certificate_page"),
    path("download_certificate/", views.download_certificate, name="download_certificate"),  # Bu satırı genel desenden önce koyun
    path('<str:community_name>/', views.community_page, name='community_page'),  # Genel deseni en sona taşıyın
    path('community/<int:community_id>/event/add/', views.community_event_add, name='community_event_add'),
    path('community/event/<int:event_id>/edit/', views.community_event_edit, name='community_event_edit'),
    path('community/event/<int:event_id>/delete/', views.community_event_delete, name='community_event_delete'),
    path('community/<int:community_id>/announcement/add/', views.community_announcement_add, name='community_announcement_add'),
    path('community/announcement/<int:announcement_id>/edit/', views.community_announcement_edit, name='community_announcement_edit'),
    path('community/announcement/<int:announcement_id>/delete/', views.community_announcement_delete, name='community_announcement_delete'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('community/image/<int:image_id>/delete/', views.community_image_delete, name='community_image_delete'),
    path('community/event/<int:event_id>/detail/', views.event_detail_and_register, name='event_detail_and_register'),
    path('community/event/<int:event_id>/', views.community_event_detail, name='community_event_detail'),
    path('community/register/<int:event_id>/', views.community_register_event, name='community_register_event'),
    path("certificate/<int:announcement_id>/", views.certificate_page, name="certificate_page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
