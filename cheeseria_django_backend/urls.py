from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'products', views.ProductView, 'product')

schema_view = get_schema_view(
    openapi.Info(
        title="Cheeseria Store",
        default_version='v1', ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('products/', include('product.urls')),
    path('users/', include('user_api.urls')),
    path('orders/', include('order.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
