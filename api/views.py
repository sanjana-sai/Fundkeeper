from django.shortcuts import render

from django.utils import timezone

from django.db.models import Sum

from rest_framework.response import Response

from api.serializers import UserSerializer,ExpenseSerializer

from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet

from budget.models import ExpenseModels

from rest_framework import authentication,permissions

from api.permissions import OwnerOnly



# Create your views here.


class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)


class ExpenseViewset(ModelViewSet):

    serializer_class=ExpenseSerializer

    queryset=ExpenseModels.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    #authentication_classes=[authentication.BasicAuthentication]    whwn we use base authentication

    permission_classes=[OwnerOnly]


    def list(self,request,*args,**kwargs):       # to get a specific user_object expenses  , modelviewset list will give all the list so we create method

        qs=ExpenseModels.objects.filter(user_object=request.user)

        serializer_instance=ExpenseSerializer(qs,many=True)

        return Response(data=serializer_instance.data)

    def perform_create(self,serializer):

        return serializer.save(user_object=self.request.user)

    
class ExpenseSummaryView(APIView):

    permission_classes=[permissions.IsAuthenticated]

    #authentication_classes=[authentication.BasicAuthentication]

    authentication_classes=[authentication.TokenAuthentication]

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        all_expenses=ExpenseModels.objects.filter(user_object=request.user,
                                                  created_date__month=current_month,
                                                  created_date__year=current_year
                                                  )
        expense_total=all_expenses.values("amount").aggregate(total=Sum("amount"))
        
        category_summary=all_expenses.values("category").annotate(total=Sum("amount"))

        data={"expense_total":expense_total,
              "category_summary":category_summary

        }

        return Response(data=data)




