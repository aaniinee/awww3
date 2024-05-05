from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Image, Tag

def image_list(request):
    images_list = Image.objects.all()

    tag = request.GET.get('tag')
    order_by = request.GET.get('order_by', '-published')

    if tag:
        images_list = images_list.filter(tags__name=tag).order_by(order_by)
    elif order_by != '':
        images_list = images_list.order_by(order_by)

    # Paginacja
    paginator = Paginator(images_list, 10)  # 10 obrazków na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()

    return render(request, 'home.html', {'page_obj': page_obj, 'tags': tags, 'num_pages': paginator.num_pages})

def image_display(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    return render(request, 'image_display.html', {'image': image})