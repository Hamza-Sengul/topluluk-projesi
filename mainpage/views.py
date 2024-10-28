from django.shortcuts import render, redirect
from .models import SliderImage, Certificate, SiteContent,Blog, CommunityImage, Event, Registration, Announcement, Project, Community, CommunityAnnouncement,CommunityEvent, CommunityEventRegistration
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CommunityEventForm, CommunityAnnouncementForm, CommunityInfoForm, CommunityImageForm, CommunityEventRegistrationForm


def index(request):
    slider_images = SliderImage.objects.all()
    site_content = SiteContent.objects.first()
    events = Event.objects.all()
    announcements = Announcement.objects.all()
    projects = Project.objects.all()
    communities = Community.objects.all()
    blogs = Blog.objects.all()
    return render(request, 'index.html', {'blogs': blogs,'communities': communities,'projects': projects,'slider_images': slider_images, 'site_content': site_content, 'events': events, 'announcements': announcements})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return JsonResponse({
        'name': event.name,
        'details': event.details,
        'date': event.date,
    })

def register_event(request, event_id):
    if request.method == 'POST':
        try:
            event = get_object_or_404(Event, id=event_id)
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            email = request.POST.get('email')
            contact_number = request.POST.get('contact_number')
            student_number = request.POST.get('student_number')  # Öğrenci numarası ekleniyor
            is_member = request.POST.get('is_member') == 'on'
            
            Registration.objects.create(
                event=event,
                name=name,
                surname=surname,
                email=email,
                contact_number=contact_number,
                student_number=student_number,  # Öğrenci numarası kaydediliyor
                is_member=is_member
            )
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return HttpResponseBadRequest("Invalid request")

def announcement_detail(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    certificate_available = announcement.certificates.exists()
    return JsonResponse({
        'name': announcement.name,
        'details': announcement.details,
        'certificate_available': certificate_available,
    })
from django.http import FileResponse, Http404
from .models import Certificate

def certificate_page(request, announcement_id):
    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            return HttpResponse("Eksik email veya duyuru kimliği.", status=400)

        # Sertifikayı bulma
        certificate = Certificate.objects.filter(announcement_id=announcement_id, email=email).first()
        if certificate:
            certificate_path = certificate.certificate_image.path
            
            # Sunucuda dosya yolunu kontrol edin
            if not os.path.exists(certificate_path):
                print("Dosya bulunamadı:", certificate_path)
                raise Http404("Sertifika dosyası sunucuda bulunamadı.")

            try:
                response = FileResponse(open(certificate_path, 'rb'), as_attachment=True, filename=f"sertifika_{announcement_id}.png")
                return response
            except Exception as e:
                print("Dosya açılırken bir hata oluştu:", e)
                raise Http404("Sertifika açılamadı.")
        else:
            return HttpResponse("E-posta kayıtlarımızla eşleşmiyor.", status=404)

    return render(request, "certificate.html", {"announcement_id": announcement_id})



from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from .models import Certificate

def download_certificate(request):
    if request.method == "POST":
        email = request.POST.get("email")
        announcement_id = request.POST.get("announcement_id")

        if not email or not announcement_id:
            return HttpResponse("Eksik email veya duyuru kimliği.", status=400)

        # Sertifika sorgusu
        certificate = Certificate.objects.filter(announcement_id=announcement_id, email=email).first()
        if certificate:
            # Sertifika bulunduysa dosyayı kullanıcıya gönder
            response = FileResponse(certificate.certificate_image.open('rb'), as_attachment=True, filename=f"sertifika_{announcement_id}.jpg")
            return response
        else:
            return HttpResponse("E-posta kayıtlarımızla eşleşmiyor.", status=404)

    return HttpResponse("Bu sayfa yalnızca POST isteklerini kabul eder.", status=405)


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return JsonResponse({
        'name': project.name,
        'description': project.description,
        'image_url': project.image.url if project.image else ''
    })
def community_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('community_dashboard_default')
        else:
            error_message = "Invalid username or password"
            return render(request, 'community_login.html', {'error_message': error_message})
    return render(request, 'community_login.html')



@login_required
def community_dashboard_default(request):
    community = request.user.community
    if request.method == 'POST':
        community.about_us = request.POST['about_us']
        community.vision = request.POST['vision']
        community.events = request.POST['events']
        community.announcements = request.POST['announcements']
        community.save()
        return redirect('community_dashboard', community_id=community.id)
    return render(request, 'community_dashboard.html', {'community': community})

def community_page(request, community_name):
    slider_images = SliderImage.objects.all()
    site_content = SiteContent.objects.first()
    events = Event.objects.all()
    announcements = Announcement.objects.all()
    projects = Project.objects.all()
    communities = Community.objects.all()
    communities = Community.objects.all()
    blogs = Blog.objects.all()
    community = get_object_or_404(Community, name=community_name)
    images = community.images.all()
    return render(request, 'community_page.html', {
        'communities': communities, 
        'community': community,
        'about_us': community.about_us,
        'vision': community.vision,
        'communities': communities,
        'projects': projects,
        'slider_images': slider_images,
        'site_content': site_content, 
        'events': events, 
        'announcements': announcements,
        'blogs': blogs,
        'images': images
    })


@login_required
def community_dashboard_by_id(request, community_id):
    community = get_object_or_404(Community, id=community_id, admin_user=request.user)

    event_form = CommunityEventForm()
    announcement_form = CommunityAnnouncementForm()
    community_info_form = CommunityInfoForm(instance=community)
    image_form = CommunityImageForm()

    if request.method == 'POST':
        if 'submit_event' in request.POST:
            event_form = CommunityEventForm(request.POST)
            if event_form.is_valid():
                event = event_form.save(commit=False)
                event.community = community
                event.save()
                return redirect('community_dashboard_by_id', community_id=community.id)
        elif 'submit_announcement' in request.POST:
            announcement_form = CommunityAnnouncementForm(request.POST)
            if announcement_form.is_valid():
                announcement = announcement_form.save(commit=False)
                announcement.community = community
                announcement.save()
                return redirect('community_dashboard_by_id', community_id=community.id)
        elif 'submit_info' in request.POST:
            community_info_form = CommunityInfoForm(request.POST, instance=community)
            if community_info_form.is_valid():
                community_info_form.save()
                return redirect('community_dashboard_by_id', community_id=community.id)
        elif 'submit_image' in request.POST:
            image_form = CommunityImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.community = community
                image.save()
                return redirect('community_dashboard_by_id', community_id=community.id)

    images = community.images.all()
    registrations = CommunityEventRegistration.objects.filter(event__community=community)

    # Her etkinliğe göre kayıtları gruplayalım
    event_registrations = {}
    for event in community.events.all():
        event_registrations[event] = CommunityEventRegistration.objects.filter(event=event)

    return render(request, 'community_dashboard.html', {
        'community': community,
        'event_form': event_form,
        'announcement_form': announcement_form,
        'community_info_form': community_info_form,
        'image_form': image_form,
        'images': images,
        'registrations': registrations,
        'event_registrations': event_registrations,
    })

def community_event_add(request, community_id):
    community = get_object_or_404(Community, id=community_id, admin_user=request.user)
    if request.method == 'POST':
        form = CommunityEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.community = community
            event.save()
            return redirect('community_dashboard_by_id', community_id=community.id)
    else:
        form = CommunityEventForm()
    return render(request, 'community_event_form.html', {'form': form, 'community': community})

def community_event_edit(request, event_id):
    event = get_object_or_404(CommunityEvent, id=event_id, community__admin_user=request.user)
    if request.method == 'POST':
        form = CommunityEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('community_dashboard_by_id', community_id=event.community.id)
    else:
        form = CommunityEventForm(instance=event)
    return render(request, 'community_event_form.html', {'form': form, 'community': event.community})

def community_event_delete(request, event_id):
    event = get_object_or_404(CommunityEvent, id=event_id, community__admin_user=request.user)
    community_id = event.community.id
    event.delete()
    return redirect('community_dashboard_by_id', community_id=community_id)

def community_announcement_add(request, community_id):
    community = get_object_or_404(Community, id=community_id, admin_user=request.user)
    if request.method == 'POST':
        form = CommunityAnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.community = community
            announcement.save()
            return redirect('community_dashboard_by_id', community_id=community.id)
    else:
        form = CommunityAnnouncementForm()
    return render(request, 'community_announcement_form.html', {'form': form, 'community': community})

def community_announcement_edit(request, announcement_id):
    announcement = get_object_or_404(CommunityAnnouncement, id=announcement_id, community__admin_user=request.user)
    if request.method == 'POST':
        form = CommunityAnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('community_dashboard_by_id', community_id=announcement.community.id)
    else:
        form = CommunityAnnouncementForm(instance=announcement)
    return render(request, 'community_announcement_form.html', {'form': form, 'community': announcement.community})

def community_announcement_delete(request, announcement_id):
    announcement = get_object_or_404(CommunityAnnouncement, id=announcement_id, community__admin_user=request.user)
    community_id = announcement.community.id
    announcement.delete()
    return redirect('community_dashboard_by_id', community_id=community_id)


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    blogs = Blog.objects.all()
    site_content = SiteContent.objects.first()
    return render(request, 'blog_detail.html', {'blog': blog,'blogs': blogs, 'site_content': site_content})


@login_required
def community_image_delete(request, image_id):
    image = get_object_or_404(CommunityImage, id=image_id, community__admin_user=request.user)
    community_id = image.community.id
    image.delete()
    return redirect('community_dashboard_by_id', community_id=community_id)


def event_detail_and_register(request, event_id):
    event = get_object_or_404(CommunityEvent, id=event_id)
    if request.method == 'POST':
        form = CommunityEventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.save()
            return JsonResponse({'success': True})
    else:
        form = CommunityEventRegistrationForm()
    
    return render(request, 'event_detail_popup.html', {'event': event, 'form': form})

def community_event_detail(request, event_id):
    event = get_object_or_404(CommunityEvent, id=event_id)
    return JsonResponse({
        'name': event.name,
        'details': event.details,
        'date': event.date,
    })

def community_register_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(CommunityEvent, id=event_id)
        form = CommunityEventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

