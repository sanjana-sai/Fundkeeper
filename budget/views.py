from typing import Any

from django.shortcuts import render,redirect

from django.views.generic import View

from budget.forms import ExpenseModelForm,IncomeModelForm,RegistrationForm,LoginForm,SummaryForm

from budget.models import ExpenseModels,IncomeModels

from django.contrib import messages

from django.utils import timezone

from django.db.models import Sum

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from budget.decorators import signin_required

from django.utils.decorators import method_decorator

import datetime

# function decorator => method decorator

@method_decorator(signin_required,name="dispatch")
class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        if not request.user.is_authenticated:

             messages.error(request,"invalid session please login")

             return redirect("signin")

        
        form_instance=ExpenseModelForm()     

        # listing all data .omr query for fetching all the data.  listing and adding are done in the same view

        #qs=ExpenseModels.objects.all()      # listing all the datas

        qs=ExpenseModels.objects.filter(user_object=request.user)  # login cheeyathe user nte expense mathrame list cheeyuu

        return render(request,"expense_add.html",{"form":form_instance,"data":qs})
    

    def post(self,request,*args,**kwargs):

        form_instance=ExpenseModelForm(request.POST)

        if form_instance.is_valid():

            # we have to add user_object to form_instance before saving the form_instance 

            form_instance.instance.user_object=request.user

            form_instance.save()    # we are creating expenses object is missing =user_object

            messages.success(request,"expenses has been created")

            print("expense has been created")

            return redirect("expense-add")
        else:

            messages.error(request,"expense is not created")

            return render(request,"expense_add.html",{"form":form_instance})

# localhost:8000/expense/{id}/change

@method_decorator(signin_required,name="dispatch")
class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_object=ExpenseModels.objects.get(id=id)

        form_instance=ExpenseModelForm(instance=expense_object)

        return render(request,"expense_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_object=ExpenseModels.objects.get(id=id)

        form_instance=ExpenseModelForm(instance=expense_object,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"expense changed")

            return redirect("expense-add")

        else:

            messages.error(request,"expense not changed")

            messages.error(request,"failed to update expense")
            
            return render(request,"expense_edit.html",{"form":form_instance})
        

# expense detail view 
# url  localhost:8000/expense/{id}/

@method_decorator(signin_required,name="dispatch")
class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=ExpenseModels.objects.get(id=id)

        return render(request,"expense_detail.html",{"data":qs})
    
# url:localhost:8000/expense/{id}/remove/

@method_decorator(signin_required,name="dispatch")
class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        ExpenseModels.objects.get(id=id).delete()

        messages.success(request,"expense is removed")

        return redirect("expense-add")
    
@method_decorator(signin_required,name="dispatch")
class  ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month    # current month edukane

        current_year=timezone.now().year      # current year edukane

        expense_list=ExpenseModels.objects.filter(created_date__month=current_month,
                                                  created_date__year=current_year,
                                                  user_object=request.user)
        
        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

        print(expense_total)

        category_summary=expense_list.values("category").annotate(total=Sum("amount"))

        print("category_summary",category_summary)

        priority_summary=expense_list.values("priority").annotate(total=Sum("amount"))

        print("priority_summary",priority_summary)


        data={
            "expense_total":expense_total,

            "category_summary":category_summary,
            
            "priority_summary":priority_summary
            
        }

        return render(request,"expense_summary.html",data)
    


# authentication

class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

           # form_instance.save()  # creating object

            data=form_instance.cleaned_data

            User.objects.create_user(**data)  # this will encrypte the password

            print("user created")

            return redirect("signin")
        
        else:

            print("error")

            return render(request,"register.html",{"form":form_instance})

        
class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"signin.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data  #{"username":given username,"password":given password}

            uname=data.get("username")

            pwd=data.get("password")

            print(uname,pwd)

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                print("user_object",user_object)

                return redirect("dashboard")
            else:

             messages.error(request,"invalid credentials")

            return render(request,"signin.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")      
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    

class DashBoardView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year


        expense_list=ExpenseModels.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)

        income_list=IncomeModels.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)

        print("expense_list",expense_list)

        print("income list",income_list)

        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

        income_total=income_list.values("amount").aggregate(total=Sum("amount"))

        print(expense_total)

        print("income_total",income_total)

        form_instance=SummaryForm()

        monthly_expenses={}

        monthly_income={}

        for month in range(1,13):

            start_date=datetime.date(current_year,month,1)

            if month==12:

                end_date=datetime.date(current_year+1,1,1)
            else:

                end_date=datetime.date(current_year,month+1,1)

            monthly_expense_total=ExpenseModels.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date).aggregate(total=Sum("amount"))['total']

            monthly_expenses[start_date.strftime("%B")]=monthly_expense_total if monthly_expense_total else 0

            monthly_income_total=IncomeModels.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date).aggregate(total=Sum("amount"))['total']

            monthly_income[start_date.strftime("%B")]=monthly_income_total if monthly_income_total else 0

            print(monthly_expenses)

            print(monthly_income)
        


        return render(request,"dashboard.html",{
            "expense":expense_total,
            "income":income_total,
            "form":form_instance,
            "monthly_expenses":monthly_expenses,
            "monthly_income":monthly_income
            }
            )

    def post(self,request,*args,**kwargs):

        form_instance=SummaryForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            start_date=data.get("start_date")

            end_date=data.get("end_date")

            expense_list=ExpenseModels.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date)  # gte meannsgreaterthan

            income_list=IncomeModels.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date)# lte means less than

            print("expense_list",expense_list)

            print("income list",income_list)

            expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

            income_total=income_list.values("amount").aggregate(total=Sum("amount"))

            print(expense_total)

            print("income_total",income_total)

            return render(request,"dashboard.html",{"expense":expense_total,"income":income_total,"form":form_instance})



            





            
class IncomeCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=IncomeModelForm()

        qs=IncomeModels.objects.all()

        return render(request,"income_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        form_instance=IncomeModelForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            print("income is created")

            return redirect("income-add")
        
        else:

            return render(request,"income_add.html",{"form":form_instance})
        

class IncomeUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        income_object=IncomeModels.objects.get(id=id)

        form_instance=IncomeModelForm(instance=income_object)


        return render(request,"income_edit.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        income_object=IncomeModels.objects.get(id=id)
        form_instance=IncomeModelForm(instance=income_object,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            print("data is changed")

            return redirect("income-add")
        else:

            return render(request,"income_edit.html",{"form":form_instance})

# url:localhost:income/{int}/

class IncomeDetailsView(View):

    def get(self,request,*args,**kwargs):

        id= kwargs.get("pk")

        qs=IncomeModels.objects.get(id=id)

        return render(request,"income_detail.html",{"data":qs})
    





    



    