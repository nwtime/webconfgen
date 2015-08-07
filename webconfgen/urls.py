from frontend import views
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.contrib import admin


router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'uploads', views.UploadViewSet)
router.register(r'versions', views.VersionViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^admin/', include(admin.site.urls)),

    url(r'^$', views.type_generate, name="type-generate-detail"),
    url(r'^[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?4[0-9a-fA-F]{3}-?[89abAB][0-9a-fA-F]{3}-?[0-9a-fA-F]{12}/', views.type_parse, name="type-parse-detail"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
