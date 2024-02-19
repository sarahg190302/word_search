from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework import status
from users.services import register_user, login_user
import custom_errors
import error_responses

class UserView(APIView):
    permission_classes = []
    def post(self, request):
        try:
            name = request.data.get("name", "")
            email = request.data.get("email", "")
            dob = request.data.get("dob", "")
            password1 = request.data.get("password1", "")
            password2 = request.data.get("password2", "")
            register_user(name=name, email=email, dob=dob, password1=password1, password2=password2)
        except ValidationError as e:
            return Response(data=error_responses.validation_error_resp(e), status=status.HTTP_400_BAD_REQUEST)
        except custom_errors.EmailAddressAlreadyExistsError as e:
            return Response(data=error_responses.business_error_resp(e), status=status.HTTP_409_CONFLICT)
        return Response(data={}, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        try:
            email = request.data.get("email", "")
            password = request.data.get("password", "")
            token = login_user(email=email, password=password)
        except ValidationError as e:
            return Response(data=error_responses.validation_error_resp(e), status=status.HTTP_400_BAD_REQUEST)
        except custom_errors.InvalidLoginDetails as e:
            return Response(data=error_responses.business_error_resp(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"auth_token": token}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
