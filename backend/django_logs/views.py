from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.permissions import IsAdminUser
from .handlers import MemoryLogHandler

# Create your views here.


class LogView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        return render(request, 'logs/logs.html', context={
            'logs': ''.join(MemoryLogHandler.buffer),
        })
