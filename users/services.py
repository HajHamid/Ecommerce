import secrets
from django.contrib.auth import get_user_model

from users.models import OTP
from users.utils import send_sms

# def create_user(username: str, password: str, email: str) -> CustomUser:
#     return get_user_model().objects.create_user(
#         username=username,
#         password=password,
#         email=email
#     )

def create_and_send_otp(phone_number: str):
    if OTP.can_send_code(phone_number):
        code = OTP.generate_code()
        # code = "123456"
        otp_session_token = secrets.token_urlsafe(32)

        OTP.objects.create(
            phone_number=phone_number, 
            code=code,
            otp_session_token=otp_session_token    
        )

        message = f'your code is : {code}'
        send_sms(phone_number, message)
        return otp_session_token, None

    else:
        return None, 'OTP has been sent.'



def verify_otp(otp_token: str, code: str):
    try:
        otp = OTP.objects.get(otp_session_token=otp_token, code=code, is_verified=False)
    except OTP.DoesNotExist:
        return None, 'OTP not found'

    if otp.is_expired():
        return None, 'OTP expired'
    
    otp.is_verified = True
    otp.save()

    user, _ = get_user_model().objects.get_or_create(phone_number=otp.phone_number)
    return user, None