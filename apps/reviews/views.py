from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema # Importni qo'shdik
from .models import Review
from .serializers import ReviewSerializer

@extend_schema(
    tags=['Sharhlar va Reytinglar (Reviews)'], 
    summary="Kursga tegishli barcha sharhlarni ko'rish",
    description="Kurs ID-si orqali o'sha kursga qoldirilgan barcha izohlar va ballarni olish."
)
class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Review.objects.filter(course_id=self.kwargs['course_pk'])

@extend_schema(
    tags=['Sharhlar va Reytinglar (Reviews)'], 
    summary="Kursga yangi sharh qoldirish",
    description="Tizimga kirgan foydalanuvchi o'zi o'qiyotgan kurs uchun matnli sharh va 1 dan 5 gacha bo'lgan reyting qoldiradi."
)
class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

@extend_schema(
    tags=['Sharhlar va Reytinglar (Reviews)'], 
    summary="O'z sharhini ko'rish, tahrirlash yoki o'chirish",
    description="Foydalanuvchi faqat o'zi yozgan sharhni o'zgartirishi yoki butunlay o'chirib tashlashi mumkin."
)
class ReviewUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)