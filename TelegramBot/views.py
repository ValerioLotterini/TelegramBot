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

load_dotenv()
class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        password2 = request.data.get('password2')

        if User.objects.filter(username=username).exists():
            return Response({
                "result": "Error creating the user.",
                "errors": ["Already exists a user with this username"]
            }, status=status.HTTP_400_BAD_REQUEST)

        if password != password2:
            return Response({
                "result": "Error creating the user.",
                "errors": ["The two password fields didn’t match."]
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 6:
            return Response({
                "result": "Error creating the user.",
                "errors": ["Password must be at least 6 characters long"]
            }, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[A-Z]', password):
            return Response({
                "result": "Error creating the user.",
                "errors": ["Password must contain at least one uppercase letter"]
            }, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[a-z]', password):
            return Response({
                "result": "Error creating the user.",
                "errors": ["Password must contain at least one lowercase letter"]
            }, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[0-9]', password):
            return Response({
                "result": "Error creating the user.",
                "errors": ["Password must contain at least one digit"]
            }, status=status.HTTP_400_BAD_REQUEST)

        if not re.search(r'[@$!%*?&]', password):
            return Response({
                "result": "Error creating the user.",
                "errors": ["Password must contain at least one special character (@, $, !, %, *, ?, &)"]
            }, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password)
        return Response({"result": "User successfully created."}, status=status.HTTP_200_OK)


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
        if not access_token:
            return Response({"result": "Error sending telegram message", "errors": ["Missing or invalid access token"]}, status=status.HTTP_401_UNAUTHORIZED)

        text = request.data.get('text')
        image = request.data.get('image')

        if not text and not image:
            return Response({"result": "Error sending telegram message", "errors": ["You must provide either a text or an image"]}, status=status.HTTP_400_BAD_REQUEST)

        if not chat_id:
            return Response({"result": "Error sending telegram message", "errors": ["Chat ID is missing in environment"]}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"result": "Message successfully sent"}, status=status.HTTP_200_OK)
        else:
            return Response({
                "result": "Error sending telegram message",
                "errors": ["Telegram API error: " + response.text]
            }, status=status.HTTP_400_BAD_REQUEST)