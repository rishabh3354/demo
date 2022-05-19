from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from demo.accounts.models import User
from helpers import email_validation_check, check_if_password_match
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


class Signup(APIView):
    def post(self, request):
        try:
            context = dict()
            context["status"] = False
            context["message"] = "Server Error"
            signup_data = request.POST
            if email_validation_check(signup_data.get("email")):
                email = signup_data.get("email")
                password = signup_data.get("password")
                re_pass = signup_data.get("re_password")

                if check_if_password_match(password, re_pass):
                    new_user = User.objects.create_user(
                        username=email, email=email, password=password
                    )
                    if new_user:
                        context["status"] = True
                        context["message"] = "Successfully registered!"
                else:
                    context["status"] = False
                    context["message"] = "Your password does not match!"
            else:
                context["status"] = False
                context["message"] = "Enter valid email address!"

        except IntegrityError:
            return Response(
                {"status": False, "message": "Email address already exists!"}
            )
        except Exception as e:
            return Response({"status": False, "message": "Server Error"})

        return Response(context)


class Login(APIView):
    def post(self, request):
        try:
            context = dict()
            context["status"] = False
            context["message"] = "Internal Server Error"
            login_data = request.POST

            if email_validation_check(login_data.get("email")):
                email = login_data.get("email")
                password = login_data.get("password")
                try:
                    user = User.objects.get(email__iexact=email)
                    if check_password(password, user.password):
                        user = authenticate(username=email, password=password)
                        if user:
                            print("success login!!!!!")
                        else:
                            context["status"] = False
                            context["message"] = "Authentication problem occurred"
                    else:
                        context["status"] = False
                        context["message"] = "Incorrect password!"

                except User.DoesNotExist:
                    context["status"] = False
                    context["message"] = "User does not exist!"
            else:
                context["status"] = False
                context["message"] = "Enter valid email address!"

        except Exception as e:
            return Response({"status": False, "message": "Internal Server Error"})

        return Response(context)
