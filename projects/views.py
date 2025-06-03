from django.shortcuts import render
from .serializers import ActionSerializer, ProjectSerializer, OrganizationSerializer
from rest_framework import generics
from dashboard_api.models import Action
from .models import Project,PlacesImplementation
from rest_framework.response import Response
from organizations.models import Organization
from rest_framework.views import APIView
from .permissions import IsOrganizationMember
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.


class helperView(APIView):
    def get(self, request):
            data = {}
        
            # Organization
            organization_queryset = Organization.objects.all()
            organization_serializer = OrganizationSerializer(organization_queryset, many=True)
            data['Organizations'] = organization_serializer.data 

            # Actions
            action_queryset = Action.objects.all()
            action_serializer = ActionSerializer(action_queryset, many=True)
            data['Actions'] = action_serializer.data

            return Response(data)   

####################################
    


class ProjectView(generics.GenericAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsOrganizationMember]



    def get(self, request, *args, **kwargs):
        project = Project.objects.all()
        serializer = self.serializer_class(project, many=True)
        return Response({'status': 'Success', 'data': serializer.data})
    

    def post(self,request,*args,**kwargs):
        payload=request.data 
        organization_name=payload['organization_name']
        beneficiary_category=payload['beneficiary_category']
        action_type=payload['action_type']
        number_unit = payload['number_unit']
        cost_unit = payload['cost_unit']
        date_implementation = payload['date_implementation']

        place=payload['place_name']
        number=payload['place_number']

        organization = Organization.objects.get(name=organization_name)

        project = Project.objects.create(
            organization=organization,
            beneficiary_category=beneficiary_category,
            action_type=action_type,
            #place_implementation=place_implementation,
            number_unit = number_unit,
            cost_unit = cost_unit,
            date_implementation = date_implementation

        )

        serializer = self.serializer_class(project)


        return Response({'status':'Project created', 'data': serializer.data})
    
    def put(self,request,project_id,*args,**kwargs):
        payload=request.data 
        #organization_name=payload['organization_name']
        beneficiary_category=payload['beneficiary_category']
        action_type=payload['action_type']
        place_implementation=payload['place_implementation']
        number_unit = payload['number_unit']
        cost_unit = payload['cost_unit']
        date_implementation = payload['date_implementation']
        project = Project.objects.get(id=int(project_id))

        if project is not None:

            project.beneficiary_category=beneficiary_category
            project.action_type=action_type
            project.place_implementation=place_implementation
            project.number_unit = number_unit
            project.cost_unit = cost_unit
            project.date_implementation = date_implementation
            project.save()

            serializer = self.serializer_class(project)
                
            return Response({'status': 'Updated', 'message': 'Updated successfully', 'data': serializer.data})
        else:
            return Response({'status': 'Not found project', 'message': 'This Project Does Not existing to update '}, status.HTTP_404_NOT_FOUND)




    def delete(self,request,project_id,*args,**kwargs):
        
        
        project= Project.objects.get(id=int(project_id))
        if project is not None:
                project.delete()
                return Response({'status': 'Deleted', 'message': 'Post deleted successfully'})
        else:
            return Response({'status': 'Unauthorized', 'message': 'You are not authorized to delete this post'}, status=403)
    

        
           


    