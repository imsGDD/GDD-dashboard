from rest_framework import serializers
from dashboard_api.models import Action,ChildAction
from .models import Project
from organizations.models import Organization




class ChildActionSerializer(serializers.ModelSerializer):
    child_action_type = serializers.CharField(source='action_type')
    id = serializers.ReadOnlyField(source='pk')  # Add id field


    class Meta:
        model = ChildAction
        fields = ['id','child_action_type']

class ActionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')  # Add id field

    child_actions = ChildActionSerializer(many=True, source='children')

    class Meta:
        model = Action
        fields = ['id','damage', 'action_type', 'child_actions']



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organization
        fields=['id','name']

###########################################################

class ProjectSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    class Meta:
        model= Project
        fields = "__all__"                