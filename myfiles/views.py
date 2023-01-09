from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework.throttling import UserRateThrottle
from myfiles.models import *
from datetime import datetime

class ProductApiView(APIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = product.objects.all()
        return products


    def get(self, request, *args, **kwargs):
        
        try:
            id = request.query_params["id"]
            if id != None:
                products = product.objects.get(id=id)
                serializer = ProductSerializer(products)
        except:
            products = self.get_queryset()
            serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        product_data = request.data

        for i in product_data:
            new_product = product.objects.create(name=i["name"], price1=i[
                "price1"], price2=i["price2"], amount=i["amount"], date=i["date"])

            new_product.save()

            serializer = ProductSerializer(new_product)


        return Response(serializer.data)




    def put(self, request, *args, **kwargs):
        id = request.query_params["id"]
        
        product_object = product.objects.get(id=id)

        data = request.data
        
        product_object.name = data["name"]
        product_object.price1 = data["price1"]
        product_object.price2 = data["price2"]
        product_object.amount = data["amount"]
        product_object.date = data["date"]

        product_object.save()

        serializer = ProductSerializer(product_object)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        i = request.query_params
        id = i['id']
        amount1 =i['amount'].replace(',','.')
        pro_object = product.objects.get(id=id)
        data = request.data
        val = float(amount1)
        amount = float(pro_object.amount.replace(',', '.'))
        
        if amount - val >= 0:
            pro_object.amount = (str(amount - val)).replace('.', ',')

            pro_object.save()
            new_price = float(pro_object.price2) * val
            new_price2 = float(pro_object.price1) * val
            new_data = sell.objects.create(name=pro_object.name, amount=i['amount'], price=new_price,
                date=datetime.now().date(), time=datetime.now().time(), price1=new_price2, product_id=id)

            new_data.save()
            return Response("True")
        
        else:
            return Response("False")



class SellApiView(APIView):
    serializer_class = SellSerializer

    def get_queryset(self):
        sell_page = sell.objects.all()
        return sell_page
    
    def get(self, request, *args, **kwargs):
        sell_data = sell.objects.all()
        serializer = SellSerializer(sell_data, many=True)

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        id = request.query_params['id']
        amount1 =request.query_params['amount'].replace(',','.')
        product_id = request.query_params['product_id']
        status = request.query_params['status']
        pro_object = product.objects.get(id=product_id)
        
        val = float(amount1)
        amount = float(pro_object.amount.replace(',', '.'))
        p_price1 = pro_object.price1.replace(',', '.')
        p_price2 = pro_object.price2.replace(',', '.')
        if status == 'plus':
            if amount - val >= 0:
                pro_object.amount = (str(amount - val)).replace('.', ',')
                pro_object.save()

                sell_object = sell.objects.get(id=id)
                sell_amount = sell_object.amount.replace(',', '.')
                sell_object.amount = (str(float(sell_amount) + val)).replace('.', ',')


                result = sell_object.price + float(p_price2) * val
                
                result1 = float(sell_object.price1) + float(p_price1) * val
                sell_object.price = result
                sell_object.price1 = result1
                sell_object.save()

                return Response('True')
            else:
                return Response("False")
        elif status == 'minus':           
            sell_object = sell.objects.get(id=id)
            sell_amount = sell_object.amount.replace(',', '.')
            if float(sell_amount) - val > 0:
                pro_object.amount = (str(amount + val)).replace('.', ',')
                pro_object.save()

                sell_object.amount = (str(float(sell_amount) - val)).replace('.', ',')
                narx1 = float(sell_object.price) - float(p_price2) * val
                narx2 = float(sell_object.price1) - float(p_price1) * val
                sell_object.price = narx1
                sell_object.price1 = narx2
                sell_object.save()
                return Response('True')
            elif float(sell_amount) - val == 0:
                pro_object.amount = (str(amount + val)).replace('.', ',')
                pro_object.save()

                sell_object.delete()
                return Response('True')   
            else:
                return Response('False')             
        
    
    def delete(self, request, *args, **kwargs):
        try:
            id = request.query_params['id']
            sell_data = sell.objects.get(id=id)

            sell_amount = float(sell_data.amount)

            pro_id = request.query_params['product_id']
            update_data = product.objects.get(id=pro_id)
            amount = float(update_data.amount)
            update_data.amount = amount + sell_amount;

            update_data.save()

            sell_data.delete()


            return Response('True')
        except:
            return Response('False')
        

class SelledApiView(APIView):
    serializer_class = SelledSerializer

    def get_queryset(self):
        all_obj = sotilganlar.objects.all()
        return all_obj
    
    def post(self, request, *args, **kwargs):
        if request.query_params['type'] == 'plastik':
            for i in request.data:
                new_data = sotilganlar.objects.create(name=i['name'], price=i['price'],  date=datetime.now().date(),
                time=datetime.now().time(), naqd=0, plastik=i['price'], nasiya=0, amount=i['amount'],
                price1=i['price1'], user=i['user'])

                new_data.save()
                sell.objects.get(id=i['id']).delete()
            
            return Response('True')
        
        elif request.query_params['type'] == 'naqd':
            for i in request.data:
                new_data = sotilganlar.objects.create(name=i['name'], price=i['price'], date=datetime.now().date(),
                time=datetime.now().time(), plastik=0, naqd=i['price'], nasiya=0, amount=i['amount'],
                price1=i['price1'], user=i['user'])

                new_data.save()
            
            return Response('True')
        
        elif request.query_params['type'] == 'nasiya':
            for i in request.data:
                new_data = sotilganlar.objects.create(name=i['name'], price=i['price'], customer=request.query_params['customer'], date=datetime.now().date(),
                time=datetime.now().time(), naqd=0, nasiya=i['price'], plastik=0, amount=i['amount'],
                price1=i['price1'], user=i['user'])

                new_data.save()
            
            return Response('True')


class UserApiView(APIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_data = user.objects.filter(position='Sotuvchi')
        return user_data
    
    def get(self, request, *args, **kwargs):
        try:
            id = request.query_params['id']
            user_data = user.objects.get(id=id)

            serializer = UserSerializer(user_data, many=True)

            return Response(serializer.data)
        
        except:
            user_data = user.objects.all()
            serializer = UserSerializer(user_data, many=True)

            return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        username = request.query_params['username']

        # user_data = user.objects.get(name=username)
        if user.objects.filter(name=username, position='Sotuvchi').count() > 0:
            return Response("True")
        else:
            return Response('Bunday foydalanuvchi mavjud emas!')        