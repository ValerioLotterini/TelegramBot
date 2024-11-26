# views.py
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
import re
import os
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from dotenv import load_dotenv
from .serializers import SendMessageSerializer, SignupSerializer

load_dotenv()
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            # Crea l'utente se i dati sono validi
            User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            return Response({"result": "User successfully created."}, status=status.HTTP_200_OK)
        else:
            # Restituisci gli errori del serializer
            return Response({
                "result": "Error creating the user.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
class SigninView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({"token": access_token}, status=status.HTTP_200_OK)
        else:
            return Response({
                "result": "Cannot login with provided credentials"
            }, status=status.HTTP_400_BAD_REQUEST)

class SendMessageView(APIView):
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)

        if serializer.is_valid():
            access_token = os.getenv('TELEGRAM_BOT_TOKEN')
            chat_id = os.getenv('TELEGRAM_CHAT_ID')

            if not access_token:
                return Response({
                    "result": "Error sending telegram message.",
                    "errors": ["Missing or invalid access token."]
                }, status=status.HTTP_401_UNAUTHORIZED)

            if not chat_id:
                return Response({
                    "result": "Error sending telegram message.",
                    "errors": ["Chat ID is missing in environment."]
                }, status=status.HTTP_400_BAD_REQUEST)

            text = serializer.validated_data.get('text')
            image = serializer.validated_data.get('image')

            if text:
                data = {'chat_id': chat_id, 'text': text}
                url = f"https://api.telegram.org/bot{access_token}/sendMessage"
                response = requests.post(url, data=data)

            if image:
                files = {'photo': image}
                data = {'chat_id': chat_id}
                url = f"https://api.telegram.org/bot{access_token}/sendPhoto"
                response = requests.post(url, data=data, files=files)

            if response.status_code == 200:
                return Response({"result": "Message successfully sent."}, status=status.HTTP_200_OK)

            return Response({
                "result": "Error sending telegram message.",
                "errors": ["Telegram API error: " + response.text]
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "result": "Error sending telegram message.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)