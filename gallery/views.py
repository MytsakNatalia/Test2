from django.shortcuts import render
from .models import Image


def gallery_view(request):
    images = Image.objects.all()
    return render(request, 'gallery.html', {'images': images})

