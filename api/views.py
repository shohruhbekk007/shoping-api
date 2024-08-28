from rest_framework import viewsets
from .models import Xaridor, Mahsulot, Partiya, Sklad, Sotuv
from .serializers import XaridorSerializer, MahsulotSerializer, PartiyaSerializer, SkladSerializer, SotuvSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer
from django.http import HttpResponse

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({'success': 'Logged out'}, status=status.HTTP_200_OK)







@api_view(['GET'])
def umumiy_tovarlar(request):
    tovarlar_soni = Sklad.objects.aggregate(umumiy_dona=Sum('dona'))['umumiy_dona'] or 0
    qoldiq_summasi = Sklad.objects.aggregate(umumiy_summa=Sum('narxi'))['umumiy_summa'] or 0
    
    return Response({'umumiy_tovarlar_soni': tovarlar_soni, 'umumiy_qoldiq_summasi': qoldiq_summasi})



@api_view(['GET'])
def yoqotishlar_qarzdorlar(request):
    yoqotishlar = Partiya.objects.aggregate(Sum('zarari'))['zarari__sum'] or 0
    qarzdorlar_soni = Xaridor.objects.filter(qarzdor=True).count()
    
    return Response({'yoqotishlar': yoqotishlar, 'qarzdorlar_soni': qarzdorlar_soni})

@api_view(['GET'])
def umumiy_sotuv_tovarlar_kesimida(request):
    vaqt = request.query_params.get('vaqt', 'kun')
    hozir = now()

    if vaqt == 'kun':
        boshlanish_vaqti = hozir.replace(hour=0, minute=0, second=0, microsecond=0)
    elif vaqt == 'oy':
        boshlanish_vaqti = hozir.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        boshlanish_vaqti = hozir.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    tovar_sotuvlari = Sotuv.objects.filter(sana__gte=boshlanish_vaqti).values('mahsulot__nomi').annotate(
        jami_sotilgan_dona=Sum('sotilgan_dona'),
        jami_sotilgan_summa=Sum('sotilgan_narx')
    )

    return Response({'tovar_sotuvlari': list(tovar_sotuvlari)})



@api_view(['GET'])
def eng_kop_sotilgan_tovar(request):
    vaqt = request.query_params.get('vaqt', 'kun')
    hozir = now()

    if vaqt == 'kun':
        boshlanish_vaqti = hozir.replace(hour=0, minute=0, second=0, microsecond=0)
    elif vaqt == 'oy':
        boshlanish_vaqti = hozir.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        boshlanish_vaqti = hozir.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    eng_kop_sotilgan = Sotuv.objects.filter(sana__gte=boshlanish_vaqti).values('mahsulot__nomi').annotate(soni=Sum('sotilgan_dona')).order_by('-soni').first()
    
    return Response({'eng_kop_sotilgan_tovar': eng_kop_sotilgan})



@api_view(['GET'])
def tushum_statistika(request):
    vaqt = request.query_params.get('vaqt', 'kun')
    hozir = now()

    if vaqt == 'kun':
        boshlanish_vaqti = hozir.replace(hour=0, minute=0, second=0, microsecond=0)
    elif vaqt == 'oy':
        boshlanish_vaqti = hozir.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        boshlanish_vaqti = hozir.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    tushum = Sotuv.objects.filter(sana__gte=boshlanish_vaqti).aggregate(Sum('sotilgan_narx'))['sotilgan_narx__sum'] or 0

    return Response({'tushum': tushum})



class XaridorViewSet(viewsets.ModelViewSet):
    queryset = Xaridor.objects.all()
    serializer_class = XaridorSerializer

class MahsulotViewSet(viewsets.ModelViewSet):
    queryset = Mahsulot.objects.all()
    serializer_class = MahsulotSerializer

class PartiyaViewSet(viewsets.ModelViewSet):
    queryset = Partiya.objects.all()
    serializer_class = PartiyaSerializer

class SkladViewSet(viewsets.ModelViewSet):
    queryset = Sklad.objects.all()
    serializer_class = SkladSerializer

class SotuvViewSet(viewsets.ModelViewSet):
    queryset = Sotuv.objects.all()
    serializer_class = SotuvSerializer



def Home(request):
    return HttpResponse("Salom maktab")