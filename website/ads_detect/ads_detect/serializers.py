from .models import InputSite, CheckedSite
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class InputSiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InputSite
        fields = ["url", "search", "query", "user_agent", "context"]


class CheckedSiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CheckedSite
        fields = ["url", "user_agent", "context", "ads", "screenshot_ads"]