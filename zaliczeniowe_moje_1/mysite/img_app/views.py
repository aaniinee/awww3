from django.http import HttpResponse

from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import generic

from .models import Image, Rectangle


class ImagesList(generic.ListView):
    model = Image
    template_name = "img_app/image_list.html"
    context_object_name = "images"

class ImageDisplay(generic.DetailView):
    model = Image
    template_name = "img_app/image_display.html"


class ImageEdit(generic.UpdateView, LoginRequiredMixin):
    model = Image
    fields = ['name', 'artists', 'width', 'height']
    template_name = 'img_app/image_edit.html'
    success_url = reverse_lazy('images_app:index')

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if not request.user.is_superuser and request.user not in object.artists.all():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['image_width'] = object.width
        context['image_height'] = object.height
        return context
    

class RectangleAdd(generic.CreateView):
    model = Rectangle

    def form_valid(self, form):
        form.instance.image = Image.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('edit', kwargs={'pk': self.object.image.pk})


class RectangleDelete(generic.DeleteView):
    model = Rectangle
    template_name = 'img_app/rectangle_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = self.object.image
        return context

    def get_success_url(self):
        return reverse('edit', kwargs={'pk': self.object.image.pk})
