from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Category,BrandCategory,Part,Device,WorkOrder,BrandPart




admin.site.register(Category)
admin.site.register(BrandCategory)
admin.site.register(BrandPart)
admin.site.register(Part)
# admin.site.register(Device)
admin.site.register(WorkOrder)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change) -> None:
        # if obj.brandpart is None and obj.brandcategory.category.identification is True:
        #     raise ValidationError('ddddd',code=4003)
            
        return super().save_model(request, obj, form, change)