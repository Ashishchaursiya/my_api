from django.urls import path
from knox import views as knox_views
from . import views
urlpatterns = [
    path('',views.Overview,name="api-overview"),
    path('task-list/',views.tasklist,name="task-list"),
    path('task-details/<str:id>/',views.taskDetails,name="task-details"),
    path('task-create/',views.taskCreate,name="task-create"),
    path('task-update/<str:id>/',views.taskUpdate,name="task-update"),
    path('task-delete/<str:id>/',views.taskDelete,name="task-delete"),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
]