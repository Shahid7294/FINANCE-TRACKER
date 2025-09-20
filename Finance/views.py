from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from .forms import RegistionForm,TransactionForm,GoalForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction,Goal
from django.db.models import Sum
from .admin import TransactionResources
from django.contrib import messages

# Create your views here.
class Dashboard(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        transaction=Transaction.objects.filter(user=request.user)
        goals=Goal.objects.filter(user=request.user)

        # total incom and expensec
        total_income=Transaction.objects.filter(user=request.user,transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0

        total_expense=Transaction.objects.filter(user=request.user,transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_saving=total_income-total_expense

        remaning_saving=net_saving
        
        goal_progress=[]
        for goal in goals:
            if remaning_saving >= goal.target_amount:
                goal_progress.append({"goal":goal,"progress":100})
                remaning_saving -=goal.target_amount
            elif remaning_saving >0:
                progress=(remaning_saving/goal.target_amount)*100
                goal_progress.append({'goal':goal,"progress":progress})
                remaning_saving=0
            else:
                goal_progress.append({'goal':goal,"progress":0})
    
        context={
            "transaction":transaction,
            'total_income':total_income,
            'total_expense':total_expense,
            "net_saving":net_saving,
            'goal_progress':goal_progress,
            "goal":goals,
        }

        return render(request,'dashboard.html',context)
    
class RegisterView(View):
    def get(self,request,*args, **kwargs):
        form=RegistionForm()
        return render(request ,"register.html",{"form":form})
    def post(self,request,*args, **kwargs):
        form=RegistionForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,"Account Create Successfully")
            return redirect('dashboard')
        else:
            return render(request ,"register.html",{"form":form})

class TransactionCreateview(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        form=TransactionForm()
        return render(request,"transaction_form.html",{"form":form})
    def post(self,request,*args, **kwargs):
        form=TransactionForm(request.POST)
        if form.is_valid():
            transaction=form.save(commit=False)
            transaction.user=request.user
            transaction.save()
            messages.success(request,"Transaction Add Successfully")
            return redirect('dashboard')
        return render(request,"transaction_form.html",{"form":form})

class TransactionListview(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        transaction=Transaction.objects.filter(user=request.user).order_by('date')
        return render(request,"Transaction_List.html",{'transaction':transaction})
    
class GoalCreateView(LoginRequiredMixin,View):
    def get(self,request):
        form=GoalForm()
        return render(request,"goal_form.html",{'form':form})
    def post(self,request,*args, **kwargs):
        form=GoalForm(request.POST)
        if form.is_valid():
            goal=form.save(commit=False)
            goal.user=request.user
            goal.save()
            messages.success(request,"Goal Add Successfully")

            return redirect('dashboard')
        return render(request,"goal_form.html",{"form":form})

def export_transcation(request):
    user_transcations = Transaction.objects.filter(user=request.user)
    transaction_resource=TransactionResources()
    dataset = transaction_resource.export(queryset=user_transcations)
    excel_data=dataset.export("xlsx")
# create httpresponse with the correct MIME type for an excel file
    response=HttpResponse(excel_data,content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # set header for downloading file
    response['content-Disposition']='attachment;filename=transcations_report.xlsx'
    
    messages.success(request,"File Downloaded Successfully")
    return response

class TransactionListview_update(LoginRequiredMixin,View):
    def get(self,request,id,*args, **kwargs):
        transaction=Transaction.objects.get(id=id)
        return render(request,"transactionList_update.html",{"transaction":transaction})
    def post(self,request,id):
        transaction=Transaction.objects.get(id=id)
        form = TransactionForm(request.POST, instance=transaction)

        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully")
            return redirect("TransactionListview")
        else:
            return render(request, "transactionList_update.html", {"form": form, "transaction": transaction})


        

    
class TransactionData_delete(LoginRequiredMixin,View):
    def get(self,request,pk,*args, **kwargs):
        transaction=Transaction.objects.get(pk=pk)
        transaction.delete()
        messages.success(request,"Transaction Delete Successfully")
        return redirect("TransactionListview")
    

    
    