from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from inventory.views import *



from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="ProjectX",
      default_version='v1',
      description="API documentation",
      terms_of_service="https://www.yourcompany.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourcompany.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/register-superadmin/', RegisterSuperAdminView.as_view(), name='register_superadmin'),
    path('login/sales/', SalesLoginView.as_view(), name='sales-login'),
    path('login/inventory/', InventoryLoginView.as_view(), name='inventory-login'),
    path('login/finance/', FinanceLoginView.as_view(), name='finance-login'),
    path('login/customer-support/', CustomerSupportLoginView.as_view(), name='customer-support-login'),
    path('yaml/', SpectacularAPIView.as_view(), name='schema'),
    path('documentation/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]