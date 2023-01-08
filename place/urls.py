from rest_framework.routers import DefaultRouter

from .views import PlaceViewset


router = DefaultRouter()
router.register('',PlaceViewset,basename='place')

urlpatterns = []+router.urls
