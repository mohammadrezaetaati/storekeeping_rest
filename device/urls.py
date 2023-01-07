from django.urls import path,include

from rest_framework.routers import DefaultRouter

from .views import CategoryViewset,BrandCategoryViewset

router = DefaultRouter()
router.register('category',CategoryViewset,basename='category')
router.register('brandcategory',BrandCategoryViewset,basename='brandcategory')

urlpatterns = []+router.urls
