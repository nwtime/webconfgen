from rest_framework import viewsets, permissions
from .models import Snippet, Upload, Version
from .serializers import UserSerializer, UploadSerializer, SnippetSerializer, VersionSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .tasks import parser_enqueue

# Create your views here.


class SnippetViewSet(viewsets.ModelViewSet):
    """
        Provides API access for Snippets
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(snippets_owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
        Provides API access for Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAdminUser,
    )


class VersionViewSet(viewsets.ModelViewSet):
    """
        Provides API access for Versions
    """
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = (
        permissions.IsAdminUser,
    )


class UploadViewSet(viewsets.ModelViewSet):
    """
        Provides API access for Uploads
    """
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(uploads_owner=self.request.user)
        parser_enqueue.delay(serializer.data)

    def perform_update(self, serializer):
        parser_enqueue.delay(serializer.data)


@require_http_methods(["GET"])
def type_generate(request):
    return render(request, 'frontend/type_gen.html', {})


@require_http_methods(["GET"])
def type_parse(request):
    return render(request, 'frontend/type_parse.html', {})


@require_http_methods(["GET", "POST"])
def type_generate_combine(request):
    return render(request, 'frontend/type_parse.html', {})
