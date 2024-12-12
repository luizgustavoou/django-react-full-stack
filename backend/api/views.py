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