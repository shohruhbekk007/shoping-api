from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, F
from django.utils.timezone import now
from datetime import timedelta
from .models import Xaridor, Maxsulotlar, Partiya, Sotuv, SotuvItem
from .serializers import PartiyaSerializer, XaridorSerializer, QarzlarniSondirishSerializer, MaxsulotlarSerializer, SotuvItemSerializer, SotuvSerializer


class StatistikaViewSet(viewsets.ViewSet):

    @action(detail=False)
    def tushum(self, request):
        """Kun, oy, yil bo'yicha tushum"""
        today = now()
        start_of_day = today.replace(hour=0, minute=0, second=0)
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)

        tushum_kun = Sotuv.objects.filter(sana__gte=start_of_day).aggregate(Sum('maxsulotning_jami_summasi'))['maxsulotning_jami_summasi__sum']
        tushum_oy = Sotuv.objects.filter(sana__gte=start_of_month).aggregate(Sum('maxsulotning_jami_summasi'))['maxsulotning_jami_summasi__sum']
        tushum_yil = Sotuv.objects.filter(sana__gte=start_of_year).aggregate(Sum('maxsulotning_jami_summasi'))['maxsulotning_jami_summasi__sum']

        return Response({
            'tushum_kun': tushum_kun or 0,
            'tushum_oy': tushum_oy or 0,
            'tushum_yil': tushum_yil or 0
        })

    @action(detail=False)
    def top_sotilgan_tovar(self, request):
        """Kun, oy, yil bo'yicha eng ko'p sotilgan tovar"""
        today = now()
        start_of_day = today.replace(hour=0, minute=0, second=0)
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)

        def top_sotilgan(start_date):
            return SotuvItem.objects.filter(sotuv__sana__gte=start_date)\
                .values('maxsulot__maxsulot_nomi')\
                .annotate(total_soni=Sum('maxsulot_soni'))\
                .order_by('-total_soni').first()

        top_kun = top_sotilgan(start_of_day)
        top_oy = top_sotilgan(start_of_month)
        top_yil = top_sotilgan(start_of_year)

        return Response({
            'top_kun': top_kun or 'Malumot yoq',
            'top_oy': top_oy or 'Malumot yoq',
            'top_yil': top_yil or 'Malumot yoq'
        })

    @action(detail=False)
    def top_sotilmagan_tovar(self, request):
        """Kun, oy, yil bo'yicha eng kam sotilgan tovar"""
        today = now()
        start_of_day = today.replace(hour=0, minute=0, second=0)
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)

        def top_sotilmagan(start_date):
            return SotuvItem.objects.filter(sotuv__sana__gte=start_date)\
                .values('maxsulot__maxsulot_nomi')\
                .annotate(total_soni=Sum('maxsulot_soni'))\
                .order_by('total_soni').first()

        kam_kun = top_sotilmagan(start_of_day)
        kam_oy = top_sotilmagan(start_of_month)
        kam_yil = top_sotilmagan(start_of_year)

        return Response({
            'kam_kun': kam_kun or 'Malumot yoq',
            'kam_oy': kam_oy or 'Malumot yoq',
            'kam_yil': kam_yil or 'Malumot yoq'
        })

    @action(detail=False)
    def umumiy_sotuv(self, request):
        """Kun, oy, yil bo'yicha umumiy sotuv tovarlar kesimida"""
        today = now()
        start_of_day = today.replace(hour=0, minute=0, second=0)
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)

        def umumiy_sotuv(start_date):
            return SotuvItem.objects.filter(sotuv__sana__gte=start_date)\
                .values('maxsulot__maxsulot_nomi')\
                .annotate(total_soni=Sum('maxsulot_soni'), jami_summa=Sum(F('maxsulot_soni') * F('maxsulot__sotiladigan_narx')))\
                .order_by('-total_soni')

        sotuvlar_kun = umumiy_sotuv(start_of_day)
        sotuvlar_oy = umumiy_sotuv(start_of_month)
        sotuvlar_yil = umumiy_sotuv(start_of_year)

        return Response({
            'sotuvlar_kun': sotuvlar_kun,
            'sotuvlar_oy': sotuvlar_oy,
            'sotuvlar_yil': sotuvlar_yil
        })

    @action(detail=False)
    def yoqotishlar(self, request):
        """Zararlar"""
        zarar = Maxsulotlar.objects.filter(miqdori__lt=0).values('maxsulot_nomi', 'miqdori')
        return Response({'zararlar': zarar})

    @action(detail=False)
    def qarzdorlar(self, request):
        """Qarzdor mijozlar"""
        qarzdorlar = Xaridor.objects.filter(qarzdorlik=True).values('ism', 'qarz_miqdori')
        return Response({'qarzdorlar': qarzdorlar})

    @action(detail=False)
    def umumiy_tovarlar(self, request):
        """Umumiy tovarlar soni va qoldiq miqdori"""
        umumiy_soni = Maxsulotlar.objects.aggregate(total_soni=Sum('miqdori'))['total_soni']
        qoldiq_miqdor = Maxsulotlar.objects.filter(miqdori__gt=0).aggregate(total_soni=Sum('miqdori'))['total_soni']
        return Response({
            'umumiy_tovarlar_soni': umumiy_soni or 0,
            'qoldiq_miqdor': qoldiq_miqdor or 0
        })





class SotuvViewSet(viewsets.ModelViewSet):
    queryset = Sotuv.objects.all()
    serializer_class = SotuvSerializer

    def create(self, request, *args, **kwargs):
        # Serializer'ni validatsiya qilish va saqlash
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sotuv = serializer.save()

        # Mahsulot miqdorini yangilash
        sotuvlar_data = request.data.get('sotuvlar', [])  # sotuvitem_set o'rniga sotuvlar
        for item_data in sotuvlar_data:
            maxsulot_id = item_data.get('maxsulot')
            maxsulot_soni = item_data.get('maxsulot_soni')

            # try:
            #     maxsulot = Maxsulotlar.objects.get(id=maxsulot_id)
            #     if maxsulot.miqdori >= maxsulot_soni:
            #         maxsulot.miqdori -= maxsulot_soni
            #         maxsulot.save()
            #     else:
            #         return Response({"detail": f"{maxsulot.maxsulot_nomi} yetarli miqdorda mavjud emas."}, status=status.HTTP_400_BAD_REQUEST)
            # except Maxsulotlar.DoesNotExist:
            #     return Response({"detail": f"Maxsulot ID {maxsulot_id} topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        sotuv = serializer.save()

        # Mahsulot miqdorini yangilash va ortiqcha sotilgan mahsulotni qayta hisoblash
        sotuvlar_data = request.data.get('sotuvlar', [])
        for item_data in sotuvlar_data:
            maxsulot_id = item_data.get('maxsulot')
            maxsulot_soni = item_data.get('maxsulot_soni')

            try:
                maxsulot = Maxsulotlar.objects.get(id=maxsulot_id)
                old_soni = SotuvItem.objects.filter(sotuv=instance, maxsulot=maxsulot).first().maxsulot_soni

                # Oldingi sotilgan sonini yangilash
                maxsulot.miqdori += old_soni - maxsulot_soni
                if maxsulot.miqdori >= 0:
                    maxsulot.save()
                else:
                    return Response({"detail": f"{maxsulot.maxsulot_nomi} uchun noto'g'ri miqdor."}, status=status.HTTP_400_BAD_REQUEST)
            except Maxsulotlar.DoesNotExist:
                return Response({"detail": f"Maxsulot ID {maxsulot_id} topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Mahsulot miqdorini sotuvdan oldingi holatga qaytarish
        sotuv_items = SotuvItem.objects.filter(sotuv=instance)
        for item in sotuv_items:
            maxsulot = item.maxsulot
            maxsulot.miqdori += item.maxsulot_soni
            maxsulot.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)








@api_view(['GET'])
def partiya_list(request):
    if request.method == 'GET':
        partiyalar = Partiya.objects.all()
        serializer = PartiyaSerializer(partiyalar, many=True)
        return Response(serializer.data)




@api_view(['DELETE'])
def partiya_delete(request, pk):
    try:
        partiya = Partiya.objects.get(pk=pk)
    except Partiya.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        partiya.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def partiya_update(request, pk):
    try:
        partiya = Partiya.objects.get(pk=pk)
    except Partiya.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PartiyaSerializer(partiya, data=request.data)
        if serializer.is_valid():
            partiya_data = serializer.validated_data
            maxsulot_nomi = partiya_data['maxsulot_nomi']
            maxsulot_soni = partiya_data['maxsulot_soni']
            sotilishi_kutulyotgan_narx = partiya_data['sotilishi_kutulyotgan_narx']
            
            # Maxsulotlar jadvalini tekshirish
            maxsulot, created = Maxsulotlar.objects.get_or_create(
                maxsulot_nomi=maxsulot_nomi,
                defaults={
                    'sotiladigan_narx': partiya_data['maxsulot_sotib_olingan_narx'],
                    'miqdori': maxsulot_soni,
                    'rasm': partiya_data.get('rasm')
                }
            )

            if not created:
                # Agar maxsulot mavjud bo'lsa, miqdorini yangilash
                maxsulot.miqdori += maxsulot_soni
                
                # Agar sotilishi_kutulyotgan_narx sotiladigan_narxdan katta bo'lsa, yangilash
                if sotilishi_kutulyotgan_narx > maxsulot.sotiladigan_narx:
                    maxsulot.sotiladigan_narx = sotilishi_kutulyotgan_narx

                maxsulot.save()

            # Partiya ma'lumotlarini yangilash
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def partiya_detail(request, pk):
    try:
        partiya = Partiya.objects.get(pk=pk)
    except Partiya.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PartiyaSerializer(partiya)
        return Response(serializer.data)



@api_view(['POST'])
def partiya_create(request):
    if request.method == 'POST':
        serializer = PartiyaSerializer(data=request.data)
        if serializer.is_valid():
            partiya_data = serializer.validated_data
            maxsulot_nomi = partiya_data['maxsulot_nomi']
            maxsulot_soni = partiya_data['maxsulot_soni']
            sotilishi_kutulyotgan_narx = partiya_data['sotilishi_kutulyotgan_narx']
            
            try:
                # Maxsulotlar jadvalidan nomi bo'yicha mavjud mahsulotni olish
                maxsulot = Maxsulotlar.objects.get(maxsulot_nomi=maxsulot_nomi)
                
                # Agar mahsulot mavjud bo'lsa, miqdorini va narxini yangilash
                maxsulot.miqdori += maxsulot_soni
                
                # Agar sotilishi_kutulyotgan_narx sotiladigan_narxdan katta bo'lsa, uni yangilash
                if sotilishi_kutulyotgan_narx > maxsulot.sotiladigan_narx:
                    maxsulot.sotiladigan_narx = sotilishi_kutulyotgan_narx
                
                maxsulot.save()

            except Maxsulotlar.DoesNotExist:
                # Agar mahsulot jadvalda topilmasa, yangi mahsulot yaratish
                maxsulot = Maxsulotlar.objects.create(
                    maxsulot_nomi=maxsulot_nomi,
                    sotiladigan_narx=partiya_data['maxsulot_sotib_olingan_narx'],
                    miqdori=maxsulot_soni,
                    rasm=partiya_data.get('rasm')
                )
                maxsulot.save()

            # Partiya ma'lumotlarini saqlash
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'POST'])
def maxsulotlar_list(request):
    if request.method == 'GET':
        maxsulotlar = Maxsulotlar.objects.all()
        serializer = MaxsulotlarSerializer(maxsulotlar, many=True)
        return Response(serializer.data)
    

    parser_classes = [MultiPartParser, FormParser]
    if request.method == 'POST':
        serializer = MaxsulotlarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def maxsulotlar_detail(request, pk):
    try:
        maxsulot = Maxsulotlar.objects.get(pk=pk)
    except Maxsulotlar.DoesNotExist:
        return Response({'error': 'Maxsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MaxsulotlarSerializer(maxsulot)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MaxsulotlarSerializer(maxsulot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        maxsulot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Xaridorlar ro'yxatini olish va yangi xaridor qo'shish
@api_view(['GET', 'POST'])
def xaridor_list(request):
    # GET: Barcha xaridorlarni ko'rsatish
    if request.method == 'GET':
        xaridorlar = Xaridor.objects.all()
        serializer = XaridorSerializer(xaridorlar, many=True)
        return Response(serializer.data)

    # POST: Yangi xaridor qo'shish
    elif request.method == 'POST':
        serializer = XaridorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Bitta xaridorni ko'rish, yangilash va o'chirish
@api_view(['GET', 'PUT', 'DELETE'])
def xaridor_detail(request, pk):
    try:
        xaridor = Xaridor.objects.get(pk=pk)
    except Xaridor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET: Bitta xaridor ma'lumotini olish
    if request.method == 'GET':
        serializer = XaridorSerializer(xaridor)
        return Response(serializer.data)

    # PUT: Xaridorni yangilash
    elif request.method == 'PUT':
        serializer = XaridorSerializer(xaridor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Xaridorni o'chirish
    elif request.method == 'DELETE':
        xaridor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def qarz_sondirish(request, pk):
    try:
        xaridor = Xaridor.objects.get(pk=pk)
    except Xaridor.DoesNotExist:
        return Response({"message": "Xaridor topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QarzlarniSondirishSerializer(data=request.data)
    
    if serializer.is_valid():
        toliq_tolash = serializer.validated_data.get('toliq_tolash')
        tolangan_miqdor = serializer.validated_data.get('tolangan_miqdor')

        if toliq_tolash:
            tolangan_miqdor = xaridor.qarz_miqdori
            xaridor.qarz_miqdori = 0
            xaridor.qarzdorlik = False
        else:

            if tolangan_miqdor and tolangan_miqdor <= xaridor.qarz_miqdori:
                xaridor.qarz_miqdori -= tolangan_miqdor
                if xaridor.qarz_miqdori == 0:
                    xaridor.qarzdorlik = False
            else:
                return Response({"message": "Qarz miqdori noto'g'ri"}, status=status.HTTP_400_BAD_REQUEST)

        xaridor.save()
        serializer.save(xaridor=xaridor, tolangan_miqdor=tolangan_miqdor)
        
        return Response({"message": "Qarz to'landi", "tolangan_miqdor": tolangan_miqdor}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def qarzdorlar_korsatish(request):
    qarzdorlar = Xaridor.objects.filter(qarzdorlik=True)
    serializer = QarzlarniSondirishSerializer(qarzdorlar, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)