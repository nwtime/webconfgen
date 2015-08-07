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
    version = serializers.SlugRelatedField(
        slug_field='versions_version',
        source='uploads_version',
        queryset=Version.objects.all(),
    )
    input_file_url = serializers.FileField(
        source='uploads_input_file_url',
        read_only=True,
        use_url=True,
    )
    output_file_url = serializers.FileField(
        source='uploads_output_file_url',
        read_only=True,
        use_url=True,
    )
    input_string = serializers.CharField(
        source='uploads_input_string',
    )
    status = serializers.CharField(
        source='uploads_status',
        read_only=True,
    )
    uuid = serializers.UUIDField(
        source='uploads_uuid',
        read_only=True,
    )

    class Meta:
        model = Upload
        fields = ('owner', 'output_file_url', 'status', 'input_file_url', 'input_string', 'version', 'url', 'uuid')
        lookup_field = 'uploads_uuid'


class UploadMiniSerializer(serializers.ModelSerializer):
    version = serializers.SlugRelatedField(
        slug_field='versions_version',
        source='uploads_version',
        queryset=Version.objects.all(),
    )
    input_file_url = serializers.FileField(
        source='uploads_input_file_url',
        read_only=True,
        use_url=True,
    )
    output_file_url = serializers.FileField(
        source='uploads_output_file_url',
        read_only=True,
        use_url=True,
    )
    status = serializers.CharField(
        source='uploads_status',
        read_only=True,
    )
    uuid = serializers.UUIDField(
        source='uploads_uuid',
        read_only=True,
    )

    class Meta:
        model = Upload
        fields = ('output_file_url', 'status', 'input_file_url', 'version', 'url', 'uuid')
        lookup_field = 'uploads_uuid'


class SnippetAllSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        source='snippets_description',
    )
    version = serializers.SlugRelatedField(
        slug_field='versions_version',
        source='snippets_version',
        many=True,
        queryset=Version.objects.all(),
    )
    mutually_exclusive = serializers.SlugRelatedField(
        slug_field='snippets_uuid',
        source='snippets_mutually_exclusive',
        many=True,
        queryset=Snippet.objects.all(),
    )
    name = serializers.CharField(
        source='snippets_name',
    )
    uuid = serializers.UUIDField(
        source='snippets_uuid',
        read_only=True,
    )

    class Meta:
        model = Snippet
        lookup_field = 'snippets_uuid'
        fields = ('name', 'description', 'version', 'url', 'mutually_exclusive', 'uuid')


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
    version = serializers.SlugRelatedField(
        slug_field='versions_version',
        source='snippets_version',
        many=True,
        queryset=Version.objects.all(),
    )
    mutually_exclusive = serializers.SlugRelatedField(
        slug_field='snippets_uuid',
        source='snippets_mutually_exclusive',
        many=True,
        queryset=Snippet.objects.all(),
    )
    name = serializers.CharField(
        source='snippets_name',
    )
    uuid = serializers.UUIDField(
        source='snippets_uuid',
        read_only=True,
    )

    class Meta:
        model = Snippet
        lookup_field = 'snippets_uuid'
        fields = ('name', 'file_text', 'mutually_exclusive', 'version', 'helper_text', 'url', 'owner', 'description', 'uuid')
