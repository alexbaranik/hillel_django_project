from rest_framework.routers import DefaultRouter

from api.products.views import CategoriesViewSet, ProductsViewSet


router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'categories', CategoriesViewSet, basename='categories')
urlpatterns = router.urls
