"""View module for handling requests about customer order"""
import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from tipsytequilaapi.models import Order, Customer, Product, OrderProduct
from .product import ProductSerializer


class OrderLineItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for line items """

    product = ProductSerializer(many=False)

    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='lineitem',
            lookup_field='id'
        )
        fields = ('id', 'product')
        depth = 1

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customer orders"""

    lineitems = OrderLineItemSerializer(many=True)

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'created_date', 'payment_type', 'customer', 'lineitems')


class Orders(ViewSet):
    """View for interacting with customer orders"""

    def retrieve(self, request, pk=None):
        """
        @api {GET} /cart/:id GET single order
        @apiName GetOrder
        @apiGroup Orders
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiSuccess (200) {id} id Order id
        @apiSuccess (200) {String} url Order URI
        @apiSuccess (200) {String} created_date Date order was created
        @apiSuccess (200) {String} customer Customer URI
        @apiSuccessExample {json} Success
            {
                "id": 1,
                "url": "http://localhost:8000/orders/1",
                "created_date": "2019-08-16",
                "customer": "http://localhost:8000/customers/5"
            }
        """
        try:
            customer = Customer.objects.get(user=request.auth.user)
            order = Order.objects.get(pk=pk, customer=customer)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)

        except Order.DoesNotExist as ex:
            return Response(
                {'message': 'The requested order does not exist, or you do not have permission to access it.'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        @api {PUT} /order/:id PUT new payment for order
        @apiName AddPayment
        @apiGroup Orders
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {id} id Order Id route parameter
        @apiParamExample {json} Input
            {
                "payment_type": 6
            }
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        customer = Customer.objects.get(user=request.auth.user)
        order = Order.objects.get(pk=pk, customer=customer)
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """
        @api {GET} /orders GET customer orders
        @apiName GetOrders
        @apiGroup Orders
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiSuccess (200) {Object[]} orders Array of order objects
        @apiSuccess (200) {id} orders.id Order id
        @apiSuccess (200) {String} orders.url Order URI
        @apiSuccess (200) {String} orders.created_date Date order was created
        @apiSuccess (200) {String} orders.customer Customer URI
        @apiSuccessExample {json} Success
            [
                {
                    "id": 1,
                    "url": "http://localhost:8000/orders/1",
                    "created_date": "2019-08-16",
                    "customer": "http://localhost:8000/customers/5"
                }
            ]
        """
        customer = Customer.objects.get(user=request.auth.user)
        orders = Order.objects.filter(customer=customer)

        json_orders = OrderSerializer(
            orders, many=True, context={'request': request})

        return Response(json_orders.data)
        