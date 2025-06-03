from django.shortcuts import render
from .models import User
from .serializer import RegisterSerializer, LoginSerializer, UserSerializer 
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
import random
import shortuuid
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _



# Create your views here.





# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [AllowAny,]   
#     serializer_class = RegisterSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         user_data = serializer.data
#         token = user_data.pop('token')  # Remove token from user data
#         response_data = {
#             'status': 'success',
#             'message': 'User registration successful',
#             'data': user_data,
#             'token': token
#         }
#         return Response(response_data,status=status.HTTP_201_CREATED)

#     # def post(self, request, *args, **kwargs):
#     #     serializer = self.get_serializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response({"status": "success", "message": "User created successfully."},status=status.HTTP_201_CREATED)
#     #     return Response({"status": "error", "message": serializer.errors}, status=400)
 

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny,]   
    serializer_class = RegisterSerializer 


    def post(self, request):
        payload = request.data

        username = payload['username']
        email = payload['email']
        password = payload['password']
        password2 = payload['password2']

        if password != password2:
            return Response({'status':'error','message': _('Password does not match')},status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'status':'error','message': _('This email address is already in use')},status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'status':'error','message': _('This username is already in use.')},status=status.HTTP_400_BAD_REQUEST)
        

        #p=validate_password(password)
        #hashed_password = make_password(p)
        user = User.objects.create(
            username=username,
            email=email,
            
            #password=password#hashed_password,
        )

        user.set_password(payload['password'])
        # user.save()
        # p=validate_password(password)
        # user.set_password(p)
        user.save()
        token =Token.objects.create(user=user)


        response_data = {
            'status': 'success',
            'message': _('User registration successful'),
            'data': {
                'username': user.username,
                'email': user.email,
                'user_id':user.id,
            },
            'token': token.key
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
       
 
        



        # serializer = RegisterSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({"message": _("User registered successfully.")}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#########################################################




class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(f"user name {email}   and passs   {password}")

        #user = authenticate(request, email=email, password=password)
        user = User.objects.filter(email=email).first()

        if user is None:
            #aise AuthenticationFailed('User not found!')
            #return Response({"status": "Error","message": "Invalid Email "}, status=status.HTTP_200_OK)
            return Response({'status':'Error','message': _('This email does not exist')},status=status.HTTP_400_BAD_REQUEST)


        if not user.check_password(password):
            #raise AuthenticationFailed('Incorrect password!')
            #return Response({"status": "Error","message": "password"}, status=status.HTTP_200_OK)
            return Response({'status':'Error','message': _('Incorrect password!')},status=status.HTTP_400_BAD_REQUEST)


        print(f"user issssssssssss  {user}")

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            admin_group = Group.objects.get(name='Admins')  # Replace 'admin' with your group name
            if admin_group in user.groups.all():
                role = 'admin'
            else:
                role = 'user'
            return Response({
                'status': 'success',
                'message': _('Login successful') ,
                #'message': 'Login successful', 
                'token': str(token), 
                'user_id': user.id, 
                'username': user.username,
                'role': role
            }, status=status.HTTP_200_OK)
        # else:
        #     return Response({'error': 'Invalid credentials'}, status=400)    
        



# class LoginView(generics.CreateAPIView):
#     serializer_class = LoginSerializer
#     permission_classes = [permissions.AllowAny]

#     def create(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         #print(f"user name {email}   and passs   {password}")

#         user = authenticate(request, email=email, password=password)

#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             #return Response({'token': str(token), 'user_id': user.id, 'username': user.username})
#             #return Response({'status': 'success', 'message': 'Login successful', 'token': str(token), 'user_id': user.id, 'username': user.username}, status=status.HTTP_200_OK)
#             admin_group = Group.objects.get(name='Admins')  # Replace 'admin' with your group name
#             if admin_group in user.groups.all():
#                 role = 'admin'
#             else:
#                 role = 'user'
#             return Response({
#                 'status': 'success', 
#                 'message': 'Login successful', 
#                 'token': str(token), 
#                 'user_id': user.id, 
#                 'username': user.username,
#                 'role': role
#             }, status=status.HTTP_200_OK)

#         else:
#             #return Response({'error': 'Invalid credentials'}, status=400)
#             return Response({'status': 'error', 'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    
        
      
    

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        #return Response({"detail": "Successfully logged out."})
        return Response({"status": "success", "message": "Successfully logged out."})
    
    



def generate_otp():
    uuid_key = shortuuid.uuid()
    unique_key = uuid_key[:6]
    return unique_key

class PasswordRestEmailVerify(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.get(email=email)

        if user:
            user.otp= generate_otp()
            user.save()

            uidb64 = user.pk
            otp = user.otp

            link = f"http://localhost:5173/create-new-password?otp={otp}&uidb64={uidb64}"
            print(link)
            subject = 'Password Reset Request'
            message = f'Click the following link to reset your password:\n{link}'

            send_mail(subject, message, 'from@example.com', [email])

        return user    
    

class PasswordChangeView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )        

    def create(self,request, *args, **kwargs):
        payload = request.data

        otp = payload['otp']
        uidb64 = payload['uidb64']
        password = payload['password']

        user = User.objects.get(otp=otp, id=uidb64)

        if user:
            user.set_password(password)
            user.otp= ""
            user.save()
            return Response({"message": "Password Changed Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User Does Not Exists"}, status=status.HTTP_404_NOT_FOUND)