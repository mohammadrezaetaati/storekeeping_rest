from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Place,Branch


admin.site.register(Branch)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):

    def render_change_form(self, request, context, add, change, form_url, obj):
        context['adminform'].form.fields['storekeeper'].queryset = \
                get_user_model().objects.filter(role = 'storekeeper')
        return super().render_change_form(request, context, add, change, form_url, obj)

