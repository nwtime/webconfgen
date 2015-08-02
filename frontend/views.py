from rest_framework import viewsets, permissions, renderers
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from .models import Snippet, Upload, Version
from .serializers import UserSerializer, UploadSerializer, SnippetSerializer, VersionSerializer, SnippetAllSerializer, UploadMiniSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .tasks import parser_enqueue


class SnippetViewSet(viewsets.ModelViewSet):
    """
        Provides API access for Snippets
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    )
    lookup_field = 'snippets_uuid'

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def raw(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.get_raw(), content_type='text/plain; charset=utf8')

    def perform_create(self, serializer):
        serializer.save(snippets_owner=self.request.user)

    @list_route()
    def all(self, request, *args, **kwargs):
        snippets = Snippet.objects.all()
        serializer = SnippetAllSerializer(
            snippets,
            many=True,
            context={
                'request': request
            },
        )
        return Response(serializer.data)


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
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    )

    @list_route()
    def all(self, request, *args, **kwargs):
        versions = Version.objects.all()
        serializer = VersionSerializer(
            versions,
            many=True,
            context={
                'request': request
            }
        )
        return Response(serializer.data)


class UploadViewSet(viewsets.ModelViewSet):
    """
        Provides API access for Uploads
    """
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    )
    lookup_field = 'uploads_uuid'

    def perform_create(self, serializer):
        upload = serializer.save(uploads_owner=self.request.user)
        parser_enqueue.delay(upload.id)

    def perform_update(self, serializer):
        upload = serializer.save()
        parser_enqueue.delay(upload.id)

    @detail_route()
    def mini(self, request, uploads_uuid=None):
        upload = Upload.objects.get(uploads_uuid=uploads_uuid)
        serializer = UploadMiniSerializer(
            upload,
            context={
                'request': request
            }
        )
        return Response(serializer.data)


@require_http_methods(["GET"])
def type_generate(request):
    """
        A function for providing access to the Generate frontend
    """
    return render(request, 'frontend/type_generate.html', {})


@require_http_methods(["GET"])
def type_parse(request):
    """
       A function for providing access to the Parse frontend
    """
    return render(request, 'frontend/type_parse.html', {})
