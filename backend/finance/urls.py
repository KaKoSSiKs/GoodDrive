from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExpenseCategoryViewSet,
    ExpenseViewSet,
    CashTransactionViewSet,
    ProfitReportViewSet
)

router = DefaultRouter()
router.register(r'expense-categories', ExpenseCategoryViewSet, basename='expense-category')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'cash-transactions', CashTransactionViewSet, basename='cash-transaction')
router.register(r'profit-reports', ProfitReportViewSet, basename='profit-report')

urlpatterns = [
    path('', include(router.urls)),
]

