import os
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from .serializers import CreateFileSerializer


SCOPES = ['https://www.googleapis.com/auth/drive.file']


class CreateFileView(APIView):
    def post(self, request):
        serializer = CreateFileSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data['data']
            name = serializer.validated_data['name']

            # Проверяем наличие токенов
            creds = None
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)

            # Если токенов нет или они недействительны, запрашиваем их у пользователя
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    path_creds = os.environ["PATH_TO_CREDENTIALS"]
                    flow = InstalledAppFlow.from_client_secrets_file(
                        path_creds, SCOPES)
                    creds = flow.run_local_server(port=0)
                # Сохраняем токены для следующего использования
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            try:
                # Создаем клиент Google Drive API
                service = build('drive', 'v3', credentials=creds)
                folder_id = os.environ["GD_FOLDER_ID"]
                file_metadata = {
                    'name': name,
                    'parents': [folder_id],
                    'mimeType': 'application/vnd.google-apps.document'
                }
                media = MediaIoBaseUpload(io.BytesIO(data.encode()), mimetype='text/plain')
                file = service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()

                return Response(
                    {
                        'file_id': file.get('id')
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as error:
                return Response(
                    {
                        'error': str(error)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
