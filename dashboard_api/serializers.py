from rest_framework import serializers
from .models import Action, ChildAction, Costs, Summary, DamageReport,Card,Chart,ChartData



class ChildActionSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)  

    class Meta:
        model=ChildAction
        fields = ['id','tags','parent_action','key','target_number','total_estimation','action_type','action_value','total','finished','finished_percentage']
    



class ActionSerializer(serializers.ModelSerializer):
    children = ChildActionSerializer(many=True)
    sector = serializers.StringRelatedField()
    tags = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)  


    class Meta:
        model = Action
        fields = ['id','children','sector','tags','key','damage','sub_sector','subclassification','target_number','total_estimation','action_type','action_value','total','finished','finished_percentage']


class CostSerializer(serializers.ModelSerializer):
    sector = serializers.StringRelatedField()
    class Meta:
        model = Costs
        fields = ['id','sector','key','damage_summary','sub_sector','scope_of_intervention','relief','recovery','development','total']





class SummarySerializer(serializers.ModelSerializer):
    sector = serializers.StringRelatedField()
    cost = CostSerializer(many=True)

    class Meta:
        model = Summary
        fields = ['id','sector','cost','relief','recovery','development','total']    

######################################################################



class ChartDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartData
        fields = ['id','chart','name','data_type','number','percentage','updated_at']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     number = str(data['number'])

    #     # Check if the value is a percentage
    #     if number.endswith('%'):
    #         # If it's a percentage, remove the "%" sign and format it
    #         percentage_without_percent = number.replace("%", "")
    #         formatted_percentage = "{:.0f}%".format(float(percentage_without_percent))
    #         data['number'] = formatted_percentage
    #     else:
    #         # If it's not a percentage, keep it as it is
    #         data['number'] = number

    #     return data
    def to_representation(self, instance):
        data = super().to_representation(instance)
        damage_value = data.get('number')  # Using get method to handle None value

        if damage_value is None:
            # Handle the case where 'number' is None
            return data

        damage_value = str(damage_value)

        # Check if the value is a percentage
        if damage_value.endswith('%'):
            # If it's a percentage, keep it as it is
            pass
        else:
            # Check if the number has a decimal point
            if '.' in damage_value:
                # Convert the number to float, round it up to the nearest integer, then convert it back to a string
                damage_value = str(round(float(damage_value)))
            else:
                # If it's an integer, simply convert it to a string
                damage_value = str(int(float(damage_value)))

        data['number'] = damage_value
        return data


    
class ChartSerializer(serializers.ModelSerializer):
    data = ChartDataSerializer(many=True)
    
    
    class Meta:
        model = Chart
        fields = ['id','card','type','icon_code','data']
   

class CardSerializer(serializers.ModelSerializer):
    charts = ChartSerializer(many=True)

    class Meta:
        model = Card
        fields = ['id','title','charts']

   
    
import math
class DamageReportSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True)

    class Meta:
        model = DamageReport
        fields = ['id','key','cards','sector','sub_sector','sub_classification','damage_sector','damage','damage_value_type','damage_value_number','damage_value_percentage','updated_at']
        #exclude = ['key'] 

   
    
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if '.' in str(data['damage_value_number']):
    #         damage_value = round(float(data['damage_value_number']), 2)
    #     damage_value = str(data['damage_value_number']).split('.0')[0]
        
    #     data['damage_value_number'] = damage_value
    #     return data
    
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     damage_value = str(data['damage_value_number'])

    #     # Check if the number has a decimal point
    #     if '.' in damage_value:
    #         # Convert the number to float, round it up to the nearest integer, then convert it back to a string
    #         damage_value = str(round(float(damage_value)))
    #     else:
    #         # If it's an integer, simply convert it to a string
    #         damage_value = str(int(float(damage_value)))

    #     data['damage_value_number'] = damage_value
    #     return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        damage_value = str(data['damage_value_number'])
        key = data['key']

        # Check if the value is a percentage
        if damage_value.endswith('%'):
            # If it's a percentage, keep it as it is
            pass
        else:
            # Check if the number has a decimal point
            if '.' in damage_value:
                # Convert the number to float, round it up to the nearest integer, then convert it back to a string
                damage_value = str(round(float(damage_value)))
            else:
                # If it's an integer, simply convert it to a string
                damage_value = str(int(float(damage_value)))

        data['damage_value_number'] = damage_value
        data['key']=int(key)
        return data







