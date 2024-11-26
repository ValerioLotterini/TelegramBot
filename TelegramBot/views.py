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
from .serializers import SignupSerializer

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
            error_messages = []
            for field, errors in serializer.errors.items():
                if isinstance(errors, list):
                    error_messages.extend(errors)
                else:
                    error_messages.append(errors)

            return Response({
                "result": "Error creating the user.",
                "errors": error_messages
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
        access_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')

        errors = []

        if not access_token:
            errors.append("Missing or invalid access token")

        if not chat_id:
            errors.append("Chat ID is missing in environment")

        text = request.data.get('text')
        image = request.data.get('image')

        if not text and not image:
            errors.append("You must provide either a text or an image")

        if errors:
            return Response({
                "result": "Error sending telegram message",
                "errors": errors
            }, status=status.HTTP_400_BAD_REQUEST)

        if access_token and chat_id:
            if text:
                data = {
                    'chat_id': chat_id,
                    'text': text
                }
                url = f"https://api.telegram.org/bot{access_token}/sendMessage"
                response = requests.post(url, data=data)

            if image:
                files = {'photo': image}
                data = {'chat_id': chat_id}
                url = f"https://api.telegram.org/bot{access_token}/sendPhoto"
                response = requests.post(url, data=data, files=files)

            if response.status_code == 200:
                return Response({
                    "result": "Message successfully sent"
                }, status=status.HTTP_200_OK)
            else:
                errors.append(f"Telegram API error: {response.text}")
                return Response({
                    "result": "Error sending telegram message",
                    "errors": errors
                }, status=status.HTTP_400_BAD_REQUEST)