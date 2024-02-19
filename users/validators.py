from rest_framework import serializers

class RegisterUserValidator(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=100)
    email = serializers.EmailField()
    dob = serializers.DateField()
    password1 = serializers.CharField(min_length=1)
    password2 = serializers.CharField(min_length=1)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords dont match")
        return data
    
class LoginValidator(serializers.Serializer):
    email = serializers.EmailField()