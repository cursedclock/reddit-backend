from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/token-refresh/", refresh_jwt_token),
]
