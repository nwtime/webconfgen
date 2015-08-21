"""
The Primary views for the webconfgen project
"""


from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from .models import Snippet, Upload, Version
from .permissions import IsOwnerOrAnonOrReadOnly
from .serializers import (SnippetMiniSerializer, SnippetSerializer,
                          UploadMiniSerializer, UploadSerializer,
                          UserSerializer, VersionSerializer)
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
        """
            Describes a raw snippet which is how a snippet is
            to be embedded in a ntp.conf file
        """
        snippet = self.get_object()
        return Response(snippet.get_raw(), content_type='text/plain; charset=utf8')

    def perform_create(self, serializer):
        """
            Overriding creation of snippets to add an owner.
        """
        serializer.save(snippets_owner=self.request.user)

    @list_route()
    def all(self, request, *args, **kwargs):
        """
            User to minimize the data sent when reading all snippets.
        """
        snippets = Snippet.objects.all()
        serializer = SnippetMiniSerializer(
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
        """
            Shows all versions known.
        """
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
        IsOwnerOrAnonOrReadOnly,
    )
    lookup_field = 'uploads_uuid'

    def perform_create(self, serializer):
        """
            Overriding creation to check anon based upload
            as well as to add the task to the celery task
            queue.
        """
        if self.request.user.is_authenticated():
            owner = self.request.user
        else:
            owner = None
        upload = serializer.save(uploads_owner=owner)
        parser_enqueue.delay(upload.id)

    def perform_update(self, serializer):
        """
            Create a new task on updation of the snippet.
        """
        upload = serializer.save()
        parser_enqueue.delay(upload.id)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def raw(self, request, *args, **kwargs):
        """
            Gets a raw representation of an upload.

            This is simply the uploads_input_string.
        """
        upload = self.get_object()
        return Response(upload.get_raw(), content_type='text/plain; charset=utf8')

    @detail_route()
    def mini(self, request, uploads_uuid=None):
        """
            Optimization for space when showing an upload object.
        """
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
