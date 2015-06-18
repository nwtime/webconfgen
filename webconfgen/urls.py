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

    url(r'^type-generate/', views.type_generate, name="type-generate-detail"),
    url(r'^type-parse/', views.type_parse, name="type-parse-detail"),
    url(r'^type-generate-combine/', views.type_generate_combine, name="type-generate-combine-detail"),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
