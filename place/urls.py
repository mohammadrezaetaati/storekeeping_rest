from rest_framework.routers import DefaultRouter

from .views import PlaceViewset,BranchViweset


router = DefaultRouter()
router.register('place',PlaceViewset,basename='place')
router.register('branch',BranchViweset,basename='branch')

urlpatterns = []+router.urls
