from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

# Register your models here.
admin.site.register(Category,MPTTModelAdmin)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Tag)
admin.site.register(Product)