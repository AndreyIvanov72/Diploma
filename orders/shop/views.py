from rest_framework import generics, status
from rest_framework.response import Response
from .models import Shop, Category, Product, ProductInfo, Order, OrderItem, Contact
from .serializers import ShopSerializer, CategorySerializer, ProductSerializer, ProductInfoSerializer, OrderSerializer, OrderItemSerializer, ContactSerializer

# Регистрация и логин (псоле регистрации приходит сообщение на email)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

class UserRegistrationView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not username or not password or not email:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, email=email)
        send_mail(
        "Поздравляю! Вы успешно зарегистрировались!",
        "Регистрация прошла успешно, удачных покупок!",
        "pivorc72@mail.ru",
        [email],
        fail_silently=False,)
        return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
    

# Товары и категории
class ProductListView(generics.ListCreateAPIView):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Контакты (После смены контактной информации приходит сообщение на email)
class ContactListView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes=[IsAuthenticated]
    def perform_create(self, serializer):
        user = self.request.user
        email = self.request.user.email
        serializer.save(user=user, email=email)
        send_mail(
        "Подтверждение адреса",
        "Адрес успешно добавлен",
        "pivorc72@mail.ru",
        [email],
        fail_silently=False,)
        return super().perform_create(serializer)

class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes=[IsAuthenticated]

# Заказы
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes=[IsAuthenticated]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return super().perform_create(serializer)

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user_profile = self.request.user
        return Order.objects.filter(user=user_profile)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes=[IsAuthenticated]

# Подтверждение заказа (приходит письмо на email)
class OrderConfirmationView(generics.GenericAPIView):
    lookup_field = 'pk'
    permission_classes=[IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = self.request.user
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id)
        if user == order.user:
            email = self.request.user.email
            Order.objects.filter(id=kwargs.get('pk', None)).update(status='Confirmed')
            send_mail(
            "Заказ подтвержден",
            "Поздравляем с покупкой!",
            "pivorc72@mail.ru",
            [email],
            fail_silently=False,)
            return Response({'message': 'Order confirmed'}, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Нет доступа'}, status=status.HTTP_400_BAD_REQUEST)



