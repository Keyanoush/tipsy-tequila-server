"""View module for handling requests about ratings"""
from tipsytequilaapi.models.product import Product
from tipsytequilaapi.models.product_rating import ProductRating
from rest_framework.decorators import action
from tipsytequilaapi.models.review import Review
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from tipsytequilaapi.models import Rating, Customer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser


class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for ratings"""
    class Meta:
        model = Rating
        fields = ('id', 'score', )
        depth = 1


class Ratings(ViewSet):
    """Request handlers for Ratings in the tipsytequila Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """
        @api {POST} /ratings POST new rating
        @apiName CreateRating
        @apiGroup Rating
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {String} name Short form name of rating
        @apiParam {Number} price Cost of rating
        @apiParam {String} description Long form description of rating
        @apiParam {Number} quantity Number of items to sell
        @apiParam {Number} category_id Category of rating
        @apiParamExample {json} Input
            {
                "name": "Kite",
                "price": 14.99,
                "description": "It flies high",
                "quantity": 60,
                "category_id": 4
            }
        @apiSuccess (200) {Object} rating Created rating
        @apiSuccess (200) {id} rating.id Rating Id
        @apiSuccess (200) {String} rating.name Short form name of rating
        @apiSuccess (200) {String} rating.description Long form description of rating
        @apiSuccess (200) {Number} rating.price Cost of rating
        @apiSuccess (200) {Number} rating.quantity Number of items to sell
        @apiSuccess (200) {Date} rating.created_date City where rating is located
        @apiSuccess (200) {String} rating.image_path Path to rating image
        @apiSuccess (200) {Number} rating.rating Average customer rating of rating
        @apiSuccessExample {json} Success
            {
                "id": 101,
                "url": "http://localhost:8000/ratings/101",
                "name": "Kite",
                "price": 14.99,
                "description": "It flies high",
                "quantity": 60,
                "created_date": "2019-10-23",
                "image_path": null,
                "rating": 0,
            }
        """
        new_rating = Rating()
        new_rating.score = request.data["score"]
        
        customer = Customer.objects.get(user=request.auth.user)
        new_rating.customer = customer

        new_rating.save()
        product_rating = ProductRating()
        product_rating.rating = new_rating
        product_rating.product = Product.objects.get(pk=request.data["productId"])
        product_rating.save()
        serializer = RatingSerializer(
            new_rating, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        @api {GET} /ratings/:id GET rating
        @apiName GetRating
        @apiGroup Rating
        @apiParam {id} id Rating Id
        @apiSuccess (200) {Object} rating Created rating
        @apiSuccess (200) {id} rating.id Rating Id
        @apiSuccess (200) {String} rating.name Short form name of rating
        @apiSuccess (200) {String} rating.description Long form description of rating
        @apiSuccess (200) {Number} rating.price Cost of rating
        @apiSuccess (200) {Number} rating.quantity Number of items to sell
        @apiSuccess (200) {Date} rating.created_date City where rating is located
        @apiSuccess (200) {String} rating.image_path Path to rating image
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
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        @api {PUT} /ratings/:id PUT changes to rating
        @apiName UpdateRating
        @apiGroup Rating
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {id} id Rating Id to update
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        rating = Rating.objects.get(pk=pk)
        rating.score = request.data["score"]

        customer = Customer.objects.get(user=request.auth.user)
        rating.customer = customer

        rating.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """
        @api {DELETE} /ratings/:id DELETE rating
        @apiName DeleteRating
        @apiGroup Rating
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {id} id Rating Id to delete
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        try:
            rating = Rating.objects.get(pk=pk)
            rating.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Rating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """
        @api {GET} /ratings GET all ratings
        @apiName ListRatings
        @apiGroup Rating
        @apiSuccess (200) {Object[]} ratings Array of ratings
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
        try:
            ratings = Rating.objects.all()
            item = request.query_params.get('item', None)
            if item is not None:
                ratings = Rating.objects.filter(ratings__product__id=item)
            serializer = RatingSerializer(ratings, many=True, context={'request': request})
            
            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)