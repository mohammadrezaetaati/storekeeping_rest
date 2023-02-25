from rest_framework.routers import DefaultRouter

from .views import WatingWorkOrderViewset,WorkOrderTechnicianViewset,PartViewset,BrandPartViewset,WorkOrderStorekepeerViewset




router = DefaultRouter()

router.register('wating-workorder',WatingWorkOrderViewset,basename='wating-workorder')
router.register('part',PartViewset,basename='part')
router.register('brandpart',BrandPartViewset,basename='brandpart')
router.register('workorder-technician',WorkOrderTechnicianViewset,basename='workorder-technician')
router.register('workorder-storekepeer',WorkOrderStorekepeerViewset,basename='workorder-storekepeer')


urlpatterns = []+router.urls