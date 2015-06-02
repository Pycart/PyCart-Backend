from django.contrib import admin
from models import *

def create_modeladmin(modeladmin, model, name = None):
    class  Meta:
        proxy = True
        app_label = model._meta.app_label

    attrs = {'__module__': '', 'Meta': Meta}

    newmodel = type(name, (model,), attrs)

    admin.site.register(newmodel, modeladmin)
    return modeladmin

class ItemAdmin(admin.ModelAdmin):
    pass
    # list_display = ("name_of_item", "description")

# class MyItemAdmin(ItemAdmin):
#     def queryset(self, request):
#         return self.model.objects.filter(user = request.user)
#
# create_modeladmin(MyRecipeAdmin2, model=Recipe, name='my_recipe')

admin.site.register(ShopUser)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(Tag)
