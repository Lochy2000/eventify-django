from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
import cloudinary.uploader
from .models import Event, EventAttendee


# Simple form for testing Cloudinary uploads
class CloudinaryTestForm(forms.Form):
    image = forms.ImageField(required=True)


# Admin view for testing Cloudinary
def test_cloudinary_view(request):
    result = None
    error = None
    
    if request.method == 'POST':
        form = CloudinaryTestForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            try:
                # Try uploading to Cloudinary
                upload_result = cloudinary.uploader.upload(
                    image_file,
                    folder="admin_test",
                    resource_type="auto"
                )
                result = upload_result
            except Exception as e:
                error = str(e)
    else:
        form = CloudinaryTestForm()
    
    return render(request, 'admin/cloudinary_test.html', {
        'form': form,
        'result': result,
        'error': error,
        'title': 'Test Cloudinary Upload'
    })


# Register your models here.
admin.site.register(EventAttendee)

# Add the view to admin URLs
from django.urls import path

class EventAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('cloudinary-test/', self.admin_site.admin_view(test_cloudinary_view), name='cloudinary-test'),
        ]
        return custom_urls + urls

# Register Event with EventAdmin
admin.site.register(Event, EventAdmin)
