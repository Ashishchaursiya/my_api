from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serilizers import TaskSerilizer,UserSerializer, RegisterSerializer
from .models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from knox.models import AuthToken
#for login logout
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

#how to use api and their endpoint
@api_view(['GET'])
def Overview(request):
    api_urls={
        "List":"/task-list/",
        "Details View":"/task-details/<str:pk>/",
        "Create":"/task-create/",
        "Update":"/task-update/<str:pk>/",
        "Delete":"/task-delete/<str:pk>/"
    }
    return Response(api_urls)

#get all the list
 
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def tasklist(request):
    task=  Task.objects.all() 
    serilizer=TaskSerilizer(task,many=True) 
    return Response(serilizer.data)

#get particular list

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def taskDetails(request,id):
    try:
        task = Task.objects.get(id=id)
        serilizer=TaskSerilizer(task) 
        return Response(serilizer.data) 
    except:
        return Response({"message":"Id does not exist"})      

#create the task
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def taskCreate(request):
    serilizer=TaskSerilizer(data=request.data) 
    if serilizer.is_valid():
        serilizer.save()
        return Response(serilizer.data)
    return Response({"warning":"check your field name"})    

#update the task
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def taskUpdate(request,id):
    try:
        task = Task.objects.get(id=id)
        serilizer=TaskSerilizer(instance=task,data=request.data) 
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data) 
    except:
        return Response({"message":"Id does not exist"}) 

#delete the task
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def taskDelete(request,id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        return Response({"message":"item successful deleted"}) 
    except:
        return Response({"message":"Id does not exist"})         

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })        

#login logout
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)        