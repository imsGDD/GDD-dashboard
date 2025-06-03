from rest_framework import serializers
from .models import Sectors, SubSectors,LastUpdated, Hero, News,SummaryTotal
from datetime import datetime






class SubSectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSectors
        fields = ['id','name','number','damage_percentage']




class SectorsSerializer(serializers.ModelSerializer):
    details=SubSectorsSerializer(source='main_sector', many=True)
    class Meta:
        model = Sectors
        fields = ['name','relief','recovery','development','details']




class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['news','days_of_genocide']  
      

class LastUpdatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = LastUpdated
        fields = ['time','date']  

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['time'] = instance.time.strftime('%H:%M')
        return representation    

class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = ['name','number']  

class SummaryTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryTotal
        fields = ['relief','recovery','development','total']        
                  