import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class ContactView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        print(f'Posted to contact. {",".join(args)} and {json.dumps(kwargs)} {request.data}')
        print("New Contact Request")
        return Response(status=200)
