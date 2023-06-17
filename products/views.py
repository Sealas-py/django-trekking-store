from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from products.models import Product, Category


class IndexView(ListView):
    model = Category
    template_name = "products/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["new_products"] = Product.objects.order_by('-id').all()[:4]
        context["categories"] = Category.objects.filter(parent=None)
        return context


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = context['category'].get_descendants()
        context["products"] = Product.objects.filter(category=context['category'])
        context["parent_products"] = Product.objects.filter(parent_category=context['category'])
        context["store_products"] = Product.objects.filter(root_category=context['category'])
        return context


class ProductDetailView(DetailView):
    model = Product

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect('product', self.object.id)
