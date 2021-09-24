"""View module for handling requests about order_products"""
from tipsytequilaapi.models.order import Order
from tipsytequilaapi.models.product import Product
from rest_framework.decorators import action
from tipsytequilaapi.models.review import Review
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from tipsytequilaapi.models import OrderProduct, Customer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser


class OrderProductSerializer(serializers.ModelSerializer):
    """JSON serializer for order_products"""
    class Meta:
        model = OrderProduct
        fields = ('id', 'order', 'product', )
        depth = 2


class OrderProducts(ViewSet):
    """Request handlers for OrderProducts in the tipsytequila Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """
        @api {POST} /order_products POST new order_product
        @apiName CreateOrderProduct
        @apiGroup OrderProduct
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {String} name Short form name of order_product
        @apiParam {Number} price Cost of order_product
        @apiParam {String} description Long form description of order_product
        @apiParam {Number} quantity Number of items to sell
        @apiParam {Number} category_id Category of order_product
        @apiParamExample {json} Input
            {
                "name": "Kite",
                "price": 14.99,
                "description": "It flies high",
                "quantity": 60,
                "category_id": 4
            }
        @apiSuccess (200) {Object} order_product Created order_product
        @apiSuccess (200) {id} order_product.id OrderProduct Id
        @apiSuccess (200) {String} order_product.name Short form name of order_product
        @apiSuccess (200) {String} order_product.description Long form description of order_product
        @apiSuccess (200) {Number} order_product.price Cost of order_product
        @apiSuccess (200) {Number} order_product.quantity Number of items to sell
        @apiSuccess (200) {Date} order_product.created_date City where order_product is located
        @apiSuccess (200) {String} order_product.image_path Path to order_product image
        @apiSuccess (200) {Number} order_product.order_product Average customer order_product of order_product
        @apiSuccessExample {json} Success
            {
                "id": 101,
                "url": "http://localhost:8000/order_products/101",
                "name": "Kite",
                "price": 14.99,
                "description": "It flies high",
                "quantity": 60,
                "created_date": "2019-10-23",
                "image_path": null,
                "order_product": 0,
            }
        """
        new_order_product = OrderProduct()
        customer = Customer.objects.get(user=request.auth.user)
        new_order_product.order = Order.objects.get(customer=customer, purchased=False)
        new_order_product.product = Product.objects.get(pk=request.data["productId"])
        
        
        new_order_product.customer = customer

        new_order_product.save()

        serializer = OrderProductSerializer(
            new_order_product, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        @api {GET} /order_products/:id GET order_product
        @apiName GetOrderProduct
        @apiGroup OrderProduct
        @apiParam {id} id OrderProduct Id
        @apiSuccess (200) {Object} order_product Created order_product
        @apiSuccess (200) {id} order_product.id OrderProduct Id
        @apiSuccess (200) {String} order_product.name Short form name of order_product
        @apiSuccess (200) {String} order_product.description Long form description of order_product
        @apiSuccess (200) {Number} order_product.price Cost of order_product
        @apiSuccess (200) {Number} order_product.quantity Number of items to sell
        @apiSuccess (200) {Date} order_product.created_date City where order_product is located
        @apiSuccess (200) {String} order_product.image_path Path to order_product image
        @apiSuccessExample {json} Success
            {
                "id": 101,
                "name": "Kite",
                "price": 14.99,
                "description": "It flies high",
                "quantity": 60,
                "created_date": "2019-10-23",
                "image_path": null,
            }
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(order_product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        @api {PUT} /order_products/:id PUT changes to order_product
        @apiName UpdateOrderProduct
        @apiGroup OrderProduct
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {id} id OrderProduct Id to update
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        order_product = OrderProduct.objects.get(pk=pk)
        order_product.order = Order.objects.get(pk=request.data["orderId"])
        order_product.product = Product.objects.get(pk=request.data["productId"])
        customer = Customer.objects.get(user=request.auth.user)
        order_product.customer = customer

        order_product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """
        @api {DELETE} /order_products/:id DELETE order_product
        @apiName DeleteOrderProduct
        @apiGroup OrderProduct
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {id} id OrderProduct Id to delete
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            order_product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """
        @api {GET} /order_products GET all order_products
        @apiName ListOrderProducts
        @apiGroup OrderProduct
        @apiSuccess (200) {Object[]} order_products Array of order_products
        @apiSuccessExample {json} Success
           [
               {
                   "id": 101,
                   "name": "Kite",
                   "price": 14.99,
                   "description": "It flies high",
                   "quantity": 60,
                   "created_date": "2019-10-23",
                   "image_path": null,
               }
           ]
       """
        order_products = OrderProduct.objects.all()
        order = request.query_params.get('order', None)
        if order is not None:
            order_products = OrderProduct.objects.filter(order=order)
        serializer = OrderProductSerializer(order_products, many=True, context={'request': request})
           
        return Response(serializer.data)
       