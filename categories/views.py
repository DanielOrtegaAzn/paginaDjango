from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from adminApp.decorators import admin_required
from msilib.schema import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.shortcuts import redirect, render
from categories.forms import CategoryForm
from nucleo.models import Category
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

@method_decorator([login_required,admin_required], name="dispatch")
class CategoryListView(ListView):
    model=Category
    fields=["name","photo"]

@method_decorator([login_required,admin_required], name="dispatch")
class CategoryCreateView(SuccessMessageMixin,CreateView):
    model=Category
    form_class=CategoryForm
    success_url="/categories/listCategory"
    success_message="La categoria se ha creado con exito"

@method_decorator([login_required,admin_required], name="dispatch")
class CategoryUpdateView(SuccessMessageMixin,UpdateView):
    model=Category
    form_class=CategoryForm
    success_url="/categories/listCategory"
    success_message="La categoria se ha editado con exito"

@method_decorator([login_required,admin_required], name="dispatch")
class CategoryDeleteView(SuccessMessageMixin,DeleteView):
    model=Category
    success_url="/categories/listCategory"
    success_message="La categoria se ha borrado con exito"
    
    def delete(self,request,*args,**kwargs):
        messages.success(self.request, self.success_message)
        return super(CategoryDeleteView,self).delete(request,*args,**kwargs)

'''def deleteCategory(request,pk):
    if request.method=="POST":
        Category.objects.get(pk=pk).photo.delete()
        Category.objects.get(pk=pk).delete()
        return redirect("/categories/listCategory")
    
    return render(request,"nucleo/category_confirm_delete.html")'''