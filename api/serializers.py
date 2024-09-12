from rest_framework import serializers
from .models import Partiya, Xaridor, QarzlarniSondirish, Maxsulotlar, Sotuv, SotuvItem

class PartiyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partiya
        fields = ['id', 'maxsulot_nomi', 'maxsulot_sotib_olingan_narx', 'maxsulot_soni', 'sotilishi_kutulyotgan_narx', 'rasm']



class XaridorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xaridor
        fields = '__all__'



class QarzlarniSondirishSerializer(serializers.ModelSerializer):
    class Meta:
        model = QarzlarniSondirish
        fields = ['xaridor', 'tolangan_miqdor', 'toliq_tolash', 'sana']



class MaxsulotlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maxsulotlar
        fields = ['id', 'maxsulot_nomi', 'sotiladigan_narx', 'miqdori', 'rasm']


class SotuvItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SotuvItem
        fields = ['maxsulot', 'maxsulot_soni']


class SotuvSerializer(serializers.ModelSerializer):
    sotuvlar = SotuvItemSerializer(many=True, source='sotuvitem_set')

    class Meta:
        model = Sotuv
        fields = ['xaridor_ismi', 'sotuvlar', 'maxsulotning_jami_summasi', 'qarz_summa', 'maxsulotlar']

    def create(self, validated_data):
        sotuvlar_data = validated_data.pop('sotuvitem_set')
        sotuv = Sotuv.objects.create(**validated_data)

        for item_data in sotuvlar_data:
            maxsulot = item_data['maxsulot']
            maxsulot_soni = item_data['maxsulot_soni']

            # Maxsulot miqdorini kamaytirish
            maxsulot.miqdori -= maxsulot_soni
            maxsulot.save()

            # SotuvItem yaratish
            SotuvItem.objects.create(sotuv=sotuv, maxsulot=maxsulot, maxsulot_soni=maxsulot_soni)

        return sotuv

