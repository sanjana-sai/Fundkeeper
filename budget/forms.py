from django import forms

from budget.models import ExpenseModels , IncomeModels


from django.contrib.auth.models import User


class ExpenseModelForm(forms.ModelForm):

    class Meta:

        model=ExpenseModels

        exclude=("id","created_date","user_object")

        widgets={

            "title":forms.TextInput(attrs={"class":"form-control mt-2"}),

            "amount":forms.NumberInput(attrs={"class":"form-control mt-2"}),

            "category":forms.Select(attrs={"class":"form-control,form-select mt-2"}),

#"owner":forms.TextInput(attrs={"class":"form-control})

            "priority":forms.Select(attrs={"class":"form-control mt-2 mb-2"})
        }


class IncomeModelForm(forms.ModelForm):
    class Meta:

        model=IncomeModels

        exclude=("id","created_date")

        widgets={

            "title":forms.TextInput(attrs={"class":"form-control "}),

            "amount":forms.NumberInput(attrs={"class":"form-control"}),

            "category":forms.Select(attrs={"class":"form-control"}),

            "owner":forms.TextInput(attrs={"class":"form-control"})
        }



class RegistrationForm(forms.ModelForm):

    class Meta:

        model=User

        fields=["username","email","password"]

        widgets={

            "username":forms.TextInput(attrs={"class":"form-control"}),

            "email":forms.EmailInput(attrs={"class":"form-control"}),

            "password":forms.PasswordInput(attrs={"class":"form-control"})
        }


class LoginForm(forms.Form):

   username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}) )

   password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    


class SummaryForm(forms.Form):

    start_date=forms.DateTimeField(widget=forms.DateInput(attrs={"class":"form-control mb-4","type":"date"}))

    end_date=forms.DateTimeField(widget=forms.DateInput(attrs={"class":"form-control mb-4","type":"date"}))