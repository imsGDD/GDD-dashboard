

from .views import OrganizationCreateAPIView,CreateInvite, AcceptInvitationView, CreateInviteUsers, AcceptInvitationUsersView,OrganizationActionsCreate ,OrganizationDetailCreate 
from django.urls import path 


urlpatterns = [
    path('register/', OrganizationCreateAPIView.as_view()),

    path('invite/', CreateInvite.as_view()),
    path('accept-invite/',  AcceptInvitationView.as_view()),

    #########-----invite via link to many users----#######
    path('invite-users/', CreateInviteUsers.as_view()),
    path('accept-invite-users/',  AcceptInvitationUsersView.as_view()),
    
    #####################----Achievements-----############

    path('actions/', OrganizationActionsCreate.as_view(), name='organization_actions_list_create'),


    path('<int:org_id>/',OrganizationDetailCreate.as_view(), name='OrganizationDetailCreate'),


    
    
]

