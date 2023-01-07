from django.contrib import admin

from .models import Category,BrandCategory,Part,Device,WorkOrder




admin.site.register(Category)
admin.site.register(BrandCategory)
admin.site.register(Part)
admin.site.register(Device)
admin.site.register(WorkOrder)