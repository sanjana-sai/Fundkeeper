
from rest_framework import serializers

from django.contrib.auth.models import User

from budget.models import ExpenseModels


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=["id","username","password","email"]

        read_only=["id"]

    def create(self,validated_data):      #method overridding creating a new  create method for password encrypt

        return User.objects.create_user(**validated_data)
    

class ExpenseSerializer(serializers.ModelSerializer):

    user_object=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=ExpenseModels

        fields="__all__"

        read_only_fields=["id","user_object","created_date"]
