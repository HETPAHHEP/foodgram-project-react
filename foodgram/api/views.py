from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# from .serializers import RegisterUserSerializer
#
#
# class RegisterUserView(APIView):
#     """Инициализация регистрации пользователя"""
#     serializer_class = RegisterUserSerializer
#     permissions = [permissions.AllowAny]
#
#     def post(self, request):
#         serializer = self.serializer(data=request.data)
#
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.validate_data['email']
#             username = serializer.validate_data['username']
#
#             start_registration()
#             return Response(data={
#                 'email': email,
#                 'username': username
#             }, status=status.HTTP_201_CREATED)
#
#         # return Response(data={
#         #     'error': 'User registration error'
#         # }, status=status.HTTP_400_BAD_REQUEST)
