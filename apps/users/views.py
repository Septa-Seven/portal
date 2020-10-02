from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import SeptaUser
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserDataSerializer

# Create your views here.

class SeptaUserListCreateView(generics.ListCreateAPIView):
    '''
    В функции perform_create мы хотели заполнить
    поле пользователя read_only запрашивающим пользователем,
    а затем заполнить сериализатор этим значением.
    '''
    queryset = SeptaUser.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class SeptaUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=SeptaUser.objects.all()
    serializer_class=UserDataSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]
