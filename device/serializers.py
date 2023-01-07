from rest_framework import serializers

from .models import Category,BrandCategory








class CategoryViewsetSerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class BrandCategoryViewsetSerializers(serializers.ModelSerializer):

    class Meta:
        model = BrandCategory
        fields = "__all__"
