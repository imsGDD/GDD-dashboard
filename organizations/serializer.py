from rest_framework import serializers

from .models import Organization
from .models import Organization,FieldsWork,HeadquarterCountry,Invitation,OrganizationActions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

from accounts.models import User
from rest_framework import status
from rest_framework.response import Response

from django.utils import timezone


################################################################################
class OrganizationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organization
        fields = "__all__"






################################################################################
class OrganizationSerializer(serializers.ModelSerializer):
    fields_work = serializers.PrimaryKeyRelatedField(queryset=FieldsWork.objects.all(), many=True)
    headquarter_country = serializers.PrimaryKeyRelatedField(queryset=HeadquarterCountry.objects.all(), many=True)


    #password = serializers.CharField(write_only=True, required=True,validators=[validate_password])
    #password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Organization
        fields = ['id', 'name', 'type_organization', 'email', 'website', 'fields_work', 'number_phone', 'headquarter_country', 'country', 'name_person', 'job_title', 'number_whatsup']
        
    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({'Password': 'Password does not match'})
    #     return attrs
    
    def create(self, validated_data):
        #password = validated_data.pop('password')
        #validated_data.pop('password2')
        fields_work = validated_data.pop('fields_work')
        headquarter_country_data = validated_data.pop('headquarter_country')

     

        organization = Organization.objects.create(**validated_data)
        #organization.password = make_password(password)

        organization.save()
        organization.fields_work.set(fields_work)
        organization.headquarter_country.set(headquarter_country_data)


        return organization



#######################################################################################
    




class CreateInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Invitation
        fields=['email','organization']



class CreateUser(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model= User
        fields=['username', 'password', 'password2'] 

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'Password': 'Password does not match'})
        return attrs


    def create(self,validated_data, *args, **kwargs):
        request = self.context['request']
        #payload = request.data
        otp = request.query_params.get('otp')
        email= request.query_params.get('email')
        organizations = request.query_params.get('organizations')
        uidb64= request.query_params.get('uidb64')

        current_datetime = timezone.now()

       
        invite = Invitation.objects.get(otp=otp, id=uidb64)
        if current_datetime > invite.expire_date:
            #return Response({'error': 'This invitation has expired.'}, status=status.HTTP_400_BAD_REQUEST)
            raise serializers.ValidationError({'error': 'This invitation has expired.'})



        invite.accepted=True
        invite.save()
        organization = Organization.objects.get(id=int(organizations))
        user = User.objects.create(
            username=validated_data['username'],
            email=email,
            organizations = organization
        )  
        
        user.set_password(validated_data['password'])

        user.save()
        Token.objects.create(user=user)
        return user           
    



###################################################----send invite to many user via link-----############
    
class CreateInvitationUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model=Invitation
        fields=['organization']


from django.db.models import ObjectDoesNotExist

class RegisterUsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'Password': 'Password does not match'})
        return attrs

    def create(self, validated_data):
        #org_id = self.context.get('organization_id')
        request = self.context['request']

        organizations = request.query_params.get('organizations')  
        if not organizations:
            raise serializers.ValidationError({'organization_id': 'Organization ID not provided'})

        try:
            organization = Organization.objects.get(id=int(organizations))
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'organization_id': 'Organization not found'})
        request = self.context['request']
        otp = request.query_params.get('otp')
        uidb64= request.query_params.get('uidb64')
        
        current_datetime = timezone.now()

       
        invite = Invitation.objects.get(otp=otp, id=uidb64)
        if current_datetime > invite.expire_date:
            raise serializers.ValidationError({'error': 'This invitation has expired.'})


        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            organizations=organization  
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user






##############################################################################
    
    
class OrganizationActionsSerializer(serializers.ModelSerializer):
    #action=serializers.StringRelatedField()
    class Meta:
        model = OrganizationActions
        fields = ['id', 'organization', 'action','action_type', 'finished', 'finished_percentage']

   
    