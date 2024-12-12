from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User
from rest_framework import generics, filters
from .serializers import CourseSerializar, UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Course, Note
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "limit"


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(author=request.user)
    
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    queryset = Note.objects.all()

    
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['author', 'title']
    # ordering = ["-author"]

    
    # filter_backends = [IsOwnerFilterBackend]
    # def get_queryset(self):
    #     user = self.request.user

    #     return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Note.objects.filter(author=user)

class NoteRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get(request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CourseListCreate(generics.ListCreateAPIView):
    serializer_class = CourseSerializar
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def bind_student_to_course(request, course_id):
    if not request.user.is_authenticated:

        return HttpResponse("Você precisa estar logado para se inscrever em um curso.", status=401)


    # Obtém o curso e adiciona o usuário
    course = get_object_or_404(Course, pk=course_id)
    request.user.courses.add(course)

    # Retorna uma resposta usando a classe Response
    return HttpResponse("Você foi inscrito no curso com sucesso.", status=200)

