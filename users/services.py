from users.validators import RegisterUserValidator, LoginValidator
from users.models import CustomUser
from rest_framework.authtoken.models import Token
import custom_errors

def register_user(name, email, dob, password1, password2):
    data_to_validate = {
        "name": name,
        "email": email,
        "dob": dob,
        "password1": password1,
        "password2": password2
    }
    validator = RegisterUserValidator(data=data_to_validate)
    validator.is_valid(raise_exception=True)
    validated_data = validator.validated_data
    password = validated_data["password1"]
    if CustomUser.objects.filter(email=validated_data["email"]).exists():
        raise custom_errors.EmailAddressAlreadyExistsError()
    
    user = CustomUser(name=validated_data["name"], email=validated_data["email"], dob=validated_data["dob"])
    user.set_password(password)
    user.save()

def login_user(email, password):
    data_to_validate = {
        "email": email,
        "password": password
    }
    validator = LoginValidator(data=data_to_validate)
    validator.is_valid(raise_exception=True)
    try:
        user = CustomUser.objects.get(email=data_to_validate["email"])
    except CustomUser.DoesNotExist:
        raise custom_errors.InvalidLoginDetails()
    if not user.check_password(password):
        raise custom_errors.InvalidLoginDetails()
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


