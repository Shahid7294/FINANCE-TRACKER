from django.urls import path
from Finance.views import RegisterView,Dashboard,TransactionCreateview,TransactionListview,GoalCreateView,export_transcation,TransactionListview_update,TransactionData_delete
urlpatterns = [
    path("RegisterView/",RegisterView.as_view(),name="RegisterView"),
    path("",Dashboard.as_view(),name='dashboard'),
    path("Transaction/add/",TransactionCreateview.as_view(),name="Transactioadd"),
    path("Transaction/list/view/",TransactionListview.as_view(),name='TransactionListview'),
    path("goal/add/",GoalCreateView.as_view(),name='goal_add'),
    path("generate-report/",export_transcation,name="export_transcation"),
    path("transaction/update/<int:id>/",TransactionListview_update.as_view(),name="transactionList_update"),
    path("transaction/delete/<int:pk>/",TransactionData_delete.as_view(),name="Transactiondata_delete"),
]
