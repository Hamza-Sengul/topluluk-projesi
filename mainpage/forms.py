from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Project, CommunityEvent, CommunityAnnouncement, Community, CommunityImage, CommunityEventRegistration
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    

class ProjectForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Project
        fields = ['name', 'description']



class CommunityAnnouncementForm(forms.ModelForm):
    class Meta:
        model = CommunityAnnouncement
        fields = ['name', 'details']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CommunityEventForm(forms.ModelForm):
    class Meta:
        model = CommunityEvent
        fields = ['name', 'details', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class CommunityInfoForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['about_us', 'vision']
        widgets = {
            'about_us': forms.Textarea(attrs={'rows': 3}),
            'vision': forms.Textarea(attrs={'rows': 3}),
        }


class CommunityImageForm(forms.ModelForm):
    class Meta:
        model = CommunityImage
        fields = ['image', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resim açıklaması'}),
        }

class CommunityEventRegistrationForm(forms.ModelForm):
    class Meta:
        model = CommunityEventRegistration
        fields = ['name', 'surname', 'email', 'student_number', 'is_member']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'student_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_member': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }