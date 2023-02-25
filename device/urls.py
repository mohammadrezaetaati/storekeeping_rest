from django.urls import path,include

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewset,
    BrandCategoryViewset,
    PartViewset,BrandPartViewset,
    DeviceViewset,WatingWorkOrderViewset,
    WorkOrderTechnicianViewset,
    WorkOrderStorekepeerViewset,
    DeviceStorekepeerViewset
)

router = DefaultRouter()
router.register('category',CategoryViewset,basename='category')
router.register('brandcategory',BrandCategoryViewset,basename='brandcategory')
router.register('part',PartViewset,basename='part')
router.register('brandpart',BrandPartViewset,basename='brandpart')
router.register('device',DeviceViewset,basename='device')
router.register('device-storekepeer',DeviceStorekepeerViewset,basename='device-storekepeer')
router.register('wating-workorder',WatingWorkOrderViewset,basename='wating-workorder')
router.register('workorder-technician',WorkOrderTechnicianViewset,basename='workorder-technician')
router.register('workorder-storekepeer',WorkOrderStorekepeerViewset,basename='workorder-storekepeer')

urlpatterns = []+router.urls
