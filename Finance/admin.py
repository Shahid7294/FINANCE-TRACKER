from django.contrib import admin
from .models import Transaction,Goal
from import_export import resources
from import_export.admin import ExportMixin
# Register your models here.
class TransactionResources(resources.ModelResource):
    class Meta:
        model=Transaction
        fields=('title','amount','transaction_type','date')
class TransactionAdmin(ExportMixin,admin.ModelAdmin):
    resource_class= TransactionResources
    list_display = ('title','amount','transaction_type','date')
    search_fields = ('title',)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Goal)
