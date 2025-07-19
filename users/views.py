from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import SendOTPSerializer, VerifyOTPSerializer
from users.services import create_and_send_otp, verify_otp

# class UserRegisterView(generics.CreateAPIView):
#     serializer_class = UserRegisterSerializer
#     permission_classes = [AllowAny]


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        otp_session_token, error = create_and_send_otp(phone_number)

        if error:
            return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'OTP code sent', 'otp_session_token': otp_session_token}, status=status.HTTP_200_OK)


class VerfiyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_session_token = serializer.validated_data.get('otp_session_token')
        code = serializer.validated_data.get('code')

        user, error = verify_otp(otp_session_token, code)

        if error:
            return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })