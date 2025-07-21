
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class OTPTest(APITestCase):
    def test_send_otp_request(self):
        url = reverse('send-request-otp')
        
        data = {'phone_number': '09191977449'}
        
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'OTP code sent')
        
    def test_verify_otp_request(self):
        send_url = reverse('send-request-otp')
        send_data = {'phone_number': '09191977449'}
        send_response = self.client.post(send_url, data=send_data, format="json")
        
        self.assertEqual(send_response.status_code, status.HTTP_200_OK)
        
        otp_session_token = send_response.data['otp_session_token']
        
        verify_url = reverse('verify-otp')
        verify_data = {
            'otp_session_token': otp_session_token,
            'code': '123456'
        }
        verify_response = self.client.post(verify_url, verify_data, format="json")
        
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', verify_response.data)