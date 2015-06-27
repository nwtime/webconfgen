from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet, Upload, Version


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class VersionSerializer(serializers.ModelSerializer):
    version = serializers.CharField(
        source='versions_version',
    )

    class Meta:
        model = Version
        fields = ('version', 'url')


class UploadSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        source='uploads_owner',
        view_name='user-detail',
        read_only=True,
    )
    version = serializers.HyperlinkedRelatedField(
        source='uploads_version',
        view_name='version-detail',
        queryset=Version.objects.all(),
    )
    input_file_url = serializers.URLField(
        source='uploads_input_file_url',
        read_only=True,
    )
    output_file_url = serializers.URLField(
        source='uploads_output_file_url',
        read_only=True,
    )
    input_string = serializers.CharField(
        source='uploads_input_string',
    )
    status = serializers.CharField(
        source='uploads_status',
        read_only=True,
    )

    class Meta:
        model = Upload
        fields = ('owner', 'output_file_uri', 'status', 'input_file_url', 'input_string', 'version', 'url')


class SnippetAllSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        source='snippets_description',
    )
    mutually_exclusive = serializers.HyperlinkedRelatedField(
        source='snippets_mutually_exclusive',
        many=True,
        view_name='snippet-detail',
        queryset=Snippet.objects.all(),
    )
    version = serializers.HyperlinkedRelatedField(
        source='snippets_version',
        many=True,
        view_name='version-detail',
        queryset=Version.objects.all(),
    )
    name = serializers.CharField(
        source='snippets_name',
    )

    class Meta:
        model = Snippet
        fields = ('name', 'description', 'version', 'url', 'mutually_exclusive')


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        source='snippets_owner',
        view_name='user-detail',
        read_only=True,
    )
    description = serializers.CharField(
        source='snippets_description',
    )
    file_text = serializers.CharField(
        source='snippets_file_text'
    )
    helper_text = serializers.CharField(
        source='snippets_helper_text',
    )
    mutually_exclusive = serializers.HyperlinkedRelatedField(
        source='snippets_mutually_exclusive',
        many=True,
        view_name='snippet-detail',
        queryset=Snippet.objects.all(),
    )
    version = serializers.HyperlinkedRelatedField(
        source='snippets_version',
        many=True,
        view_name='version-detail',
        queryset=Version.objects.all(),
    )
    name = serializers.CharField(
        source='snippets_name',
    )

    class Meta:
        model = Snippet
        fields = ('name', 'file_text', 'mutually_exclusive', 'version', 'helper_text', 'url', 'owner', 'description')
