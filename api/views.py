from rest_framework import viewsets
from rest_framework.response import Response
from .models import Products, Warehouse, Partys, Buyers
from .serializers import ProductsSerializer, WarehouseSerializer, PartysSerializer, BuyersSerializer
from django.db.models import Sum
from rest_framework.views import APIView
from datetime import datetime

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class PartysViewSet(viewsets.ModelViewSet):
    queryset = Partys.objects.all()
    serializer_class = PartysSerializer

class BuyersViewSet(viewsets.ModelViewSet):
    queryset = Buyers.objects.all()
    serializer_class = BuyersSerializer



class RevenueAPIView(APIView):
    def get(self, request, *args, **kwargs):
        period = request.query_params.get('period')  # "day", "month", "year"
        revenue_data = Buyers.objects.all()

        if period == 'day':
            revenue = revenue_data.filter(created__date=datetime.date.today()).aggregate(total_revenue=Sum('money_to_was'))
        elif period == 'month':
            revenue = revenue_data.filter(created__month=datetime.date.today().month).aggregate(total_revenue=Sum('money_to_was'))
        elif period == 'year':
            revenue = revenue_data.filter(created__year=datetime.date.today().year).aggregate(total_revenue=Sum('money_to_was'))
        else:
            revenue = {"total_revenue": 0}

        return Response(revenue)



class TopSellingProductsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        period = request.query_params.get('period')  # "day", "month", "year"
        sales_data = Buyers.objects.all()

        if period == 'day':
            top_selling = sales_data.filter(created__date=datetime.date.today()).values('name').annotate(total_sold=Sum('number')).order_by('-total_sold').first()
        elif period == 'month':
            top_selling = sales_data.filter(created__month=datetime.date.today().month).values('name').annotate(total_sold=Sum('number')).order_by('-total_sold').first()
        elif period == 'year':
            top_selling = sales_data.filter(created__year=datetime.date.today().year).values('name').annotate(total_sold=Sum('number')).order_by('-total_sold').first()
        else:
            top_selling = {"name": None, "total_sold": 0}

        return Response(top_selling)


class LeastSellingProductsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        period = request.query_params.get('period')  # "day", "month", "year"
        sales_data = Buyers.objects.all()

        if period == 'day':
            least_selling = sales_data.filter(created__date=datetime.date.today()).values('name').annotate(total_sold=Sum('number')).order_by('total_sold').first()
        elif period == 'month':
            least_selling = sales_data.filter(created__month=datetime.date.today().month).values('name').annotate(total_sold=Sum('number')).order_by('total_sold').first()
        elif period == 'year':
            least_selling = sales_data.filter(created__year=datetime.date.today().year).values('name').annotate(total_sold=Sum('number')).order_by('total_sold').first()
        else:
            least_selling = {"name": None, "total_sold": 0}

        return Response(least_selling)


class TotalSalesByProductAPIView(APIView):
    def get(self, request, *args, **kwargs):
        period = request.query_params.get('period')  # "day", "month", "year"
        sales_data = Buyers.objects.all()

        if period == 'day':
            total_sales = sales_data.filter(created__date=datetime.date.today()).values('name').annotate(total_sold=Sum('number'))
        elif period == 'month':
            total_sales = sales_data.filter(created__month=datetime.date.today().month).values('name').annotate(total_sold=Sum('number'))
        elif period == 'year':
            total_sales = sales_data.filter(created__year=datetime.date.today().year).values('name').annotate(total_sold=Sum('number'))
        else:
            total_sales = []

        return Response(total_sales)

class LossesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        losses = Warehouse.objects.filter(number__lt=0).values('name', 'number')
        return Response(losses)
    
class DebtorsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        debtors = Buyers.objects.filter(debtor=True).values('users', 'phone_number', 'address', 'money_to_was')
        return Response(debtors)
    
class ProductStockAPIView(APIView):
    def get(self, request, *args, **kwargs):
        total_stock = Warehouse.objects.all().aggregate(total_products=Sum('number'))
        return Response(total_stock)
