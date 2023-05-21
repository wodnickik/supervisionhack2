import sys
import os
from pathlib import Path

# API_DIR = Path(__file__).resolve().parent
# PROJ_DIR = Path(__file__).resolve().parent.parent.parent
# sys.path.append(os.path.join(API_DIR, ""))
# sys.path.append(os.path.join(PROJ_DIR, ""))

from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from .serializers import InputSiteSerializer, CheckedSiteSerializer, UserSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import InputSite, CheckedSite
from django.shortcuts import render
from .forms import InputSiteForm
from rest_framework.request import Request
from django.http import HttpRequest
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions


def index(request):
    if request.method == 'POST':
        form = InputSiteForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            new_site = InputSite(url=url)
            new_site.save()
            try:
                phish_result = 69
            except Exception as e:
                return render(request, 'home.html', {'form': InputSiteForm(), 'error': True})

            # result_obj = CheckedSite(domain=url, phishing_estimate=phish_result)
            # result_obj.save()
            result_html = {'phish_estimate': round(phish_result * 100), 'domain': url}
            return render(request, 'home.html', {'form': InputSiteForm(), 'submitted': True, "results": result_html})
    else:
        form = InputSiteForm()
    return render(request, 'home.html', {'form': form})


@api_view(['POST'])
def ad_detect_api(request):
    if request.method == 'POST':
        serializer = InputSiteSerializer(data=request.data)
        if serializer.is_valid():
            input_site_obj = serializer.save()
            url = input_site_obj.url
            try:
                ads, context = 69, 69
            except Exception as e:
                return Response({"error": "0"}, status=status.HTTP_400_BAD_REQUEST)

            result_obj = CheckedSite(url=url, user_agent=input_site_obj.user_agent, context=context,
                                     ads=ads)
            result_obj.save()
            factory = APIRequestFactory()
            request2 = factory.get('/')
            serializer_context = {
                'request': Request(request2),
            }
            result_serializer = CheckedSiteSerializer(result_obj, context=serializer_context)
            return Response(result_serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "0"}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class InputSiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = InputSite.objects.all()
    serializer_class = InputSiteSerializer
    permission_classes = [permissions.IsAuthenticated]


class CheckedSiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = CheckedSite.objects.all()
    serializer_class = CheckedSiteSerializer
    permission_classes = [permissions.IsAuthenticated]
