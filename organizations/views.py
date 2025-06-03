from django.shortcuts import render
from accounts.models import User
# Create your views here.

from rest_framework import generics
from rest_framework.response import Response
from .models import Organization,Invitation,OrganizationActions
from .serializer import OrganizationSerializer, CreateInvitationSerializer, CreateUser,OrganizationActionsSerializer,OrganizationDetailSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated,AllowAny
import shortuuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from dashboard_api.models import Action,ChildAction
####################################################################
#----------------Register Organizations-----------

class OrganizationCreateAPIView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes=(IsAuthenticated,)



####################################################################

class OrganizationDetailCreate(generics.GenericAPIView):
    serializer_class = OrganizationDetailSerializer  

    def get(self,request,*args,**kwargs):
        organization_id = self.kwargs['org_id']
        print(organization_id)
        organization = Organization.objects.get(id=int(organization_id))
        org_action = OrganizationActions.objects.filter(organization=organization)

        serialized_org_actions = [OrganizationActionsSerializer(org).data for org in org_action]

        return Response({'organization': OrganizationDetailSerializer(organization).data, 'organization_actions': serialized_org_actions})


####################################################################

def generate_otp():
    uuid_key = shortuuid.uuid()
    unique_key = uuid_key[:6]
    return unique_key    




class CreateInvite(generics.CreateAPIView):
    serializer_class = CreateInvitationSerializer
    permission_classes = (AllowAny, )

    def create(self,request, *args, **kwargs):
        email=request.data['email']
     
        org_id= request.data['organization']
        organization = Organization.objects.get(id=org_id)
        invite = Invitation.objects.create(email=email,organization=organization)
        invite.set_expire_date()

        invite.otp= generate_otp()
        invite.save()

        uidb64 = invite.pk
        otp = invite.otp

        link = f"http://127.0.0.1:8000/api/organizations/accept-invite/?otp={otp}&uidb64={uidb64}&organizations={org_id}&email={email}"
        print(link)
        subject = 'Register invite Request'
        message = f'Click the following link to Register your username and password:\n{link}'

        #send_mail(subject, message, 'from@example.com', [email])

        #return invite   
        return Response({'message': 'Invitation sent', 'link': link}, status=status.HTTP_201_CREATED)
 
    



class AcceptInvitationView(generics.CreateAPIView):
    serializer_class = CreateUser
    queryset = User.objects.all()
    permission_classes = (AllowAny, ) 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()
        except serializers.ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)  



###################################################----send invite to many user via link-----############
from .serializer import CreateInvitationUsersSerializer,RegisterUsersSerializer   

class CreateInviteUsers(generics.CreateAPIView):
    serializer_class = CreateInvitationUsersSerializer  
    permission_classes = (AllowAny, )

    def create(self,request, *args, **kwargs):
     
        org_id= request.data['organization']
        organization = Organization.objects.get(id=org_id)
        invite = Invitation.objects.create(organization=organization)
        invite.set_expire_date()

        invite.otp= generate_otp()
        invite.save()

        uidb64 = invite.pk
        otp = invite.otp

        link = f"http://127.0.0.1:8000/api/organizations/accept-invite-users/?otp={otp}&uidb64={uidb64}&organizations={org_id}"
        print(link)
        subject = 'Register invite Request'
        message = f'Click the following link to Register your username and password:\n{link}'

        #send_mail(subject, message, 'from@example.com', [email])

        #return invite  
        return Response({'message': 'Invitation sent', 'link': link}, status=status.HTTP_201_CREATED)
  
    



class AcceptInvitationUsersView(generics.CreateAPIView):
    serializer_class = RegisterUsersSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, ) 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()
        except serializers.ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)  






#############################################################################################
    




class OrganizationActionsCreate(generics.GenericAPIView):
    serializer_class = OrganizationActionsSerializer  
      


    def post(self,request,*args,**kwargs):
        action_id = request.data['action']
        finished = request.data['finished']
        finished_percentage = request.data['finished_percentage']
        organization_id = request.data['organization']
        action_type = request.data['action_type']

        organization  =Organization.objects.get(id=int(organization_id))
        action = Action.objects.get(id=int(action_id))
        
        action_child = ChildAction.objects.filter(parent_action=action)
        child_actions = action_child.filter(action_type__contains=action_type.strip()).first()

       
        
    
    
        org_action= OrganizationActions.objects.create(organization=organization,finished=finished,finished_percentage=finished_percentage,action=action,action_type=action_type)

        if action.action_type ==action_type:
            print('action')
            action.finished_percentage=finished_percentage
            action.finished=finished
            action.save()
        elif child_actions.action_type== action_type:
            print('child action')
            child_actions.finished_percentage=finished_percentage
            child_actions.finished=finished
            child_actions.save()
        
        return Response({'status':'created'})
