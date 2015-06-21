from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Snippet, Upload, Version


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('versions_version', 'url')


class UploadSerializer(serializers.ModelSerializer):
    uploads_owner = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
    )
    uploads_version = serializers.HyperlinkedRelatedField(
        view_name='version-detail',
        queryset=Version.objects.all()
    )

    class Meta:
        model = Upload
        fields = ('uploads_owner', 'uploads_output_file_uri', 'uploads_status', 'uploads_input_string', 'uploads_version', 'url')


class SnippetSerializer(serializers.ModelSerializer):
    snippets_owner = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
    )

    snippets_mutually_exclusive = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='snippet-detail',
        queryset=Snippet.objects.all()
    )
    snippets_version = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='version-detail',
        queryset=Version.objects.all()
    )

    class Meta:
        model = Snippet
        fields = ('snippets_name', 'snippets_file_text', 'snippets_mutually_exclusive', 'snippets_version', 'snippets_helper_text', 'url', 'snippets_owner')
