from django.contrib import admin
from .models import Categoria

# Register your models here.
class CategoriaAdm(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome_categoria',)}
    list_display = ('nome_categoria', 'slug')

admin.site.register(Categoria, CategoriaAdm)