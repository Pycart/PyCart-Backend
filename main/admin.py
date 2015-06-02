from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from models import *

def create_modeladmin(modeladmin, model, name = None):
    class  Meta:
        proxy = True
        app_label = model._meta.app_label

    attrs = {'__module__': '', 'Meta': Meta}

    newmodel = type(name, (model,), attrs)

    admin.site.register(newmodel, modeladmin)
    return modeladmin

class OptionInline(admin.TabularInline):
    model = Option

class ItemAdmin(admin.ModelAdmin):
    pass
    # list_display = ("name_of_item", "description")

# class MyItemAdmin(ItemAdmin):
#     def queryset(self, request):
#         return self.model.objects.filter(user = request.user)
#
# create_modeladmin(MyRecipeAdmin2, model=Recipe, name='my_recipe')


class Shop_Item_TagAdmin(MPTTModelAdmin):
    list_display = ("name","slug")
    search_fields = ['name',]
    raw_id_fields = ['parent',]


admin.site.register(ShopUser)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(Tag)
admin.site.register(Shop_Item_Tag, Shop_Item_TagAdmin)
admin.site.register(Shop_Tagged_Item)
admin.site.register(Option)
