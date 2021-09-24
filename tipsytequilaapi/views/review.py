"""View module for handling requests about reviews"""
from tipsytequilaapi.models.product import Product
from tipsytequilaapi.models.product_review import ProductReview
from rest_framework.decorators import action
from tipsytequilaapi.models.review import Review
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from tipsytequilaapi.models import Review, Customer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews"""
    class Meta:
        model = Review
        fields = ('id', 'description', )
        depth = 1


class Reviews(ViewSet):
    """Request handlers for Reviews in the tipsytequila Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """
        @api {POST} /reviews POST new review
        @apiName CreateReview
        @apiGroup Review
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {String} name Short form name of review
        @apiParam {Number} price Cost of review
        @apiParam {String} description Long form description of review
        @apiParam {Number} quantity Number of items to sell
        @apiParam {Number} category_id Category of review
        @apiParamExample {json} Input
            {
                "name": "Kite",
                "price": 14.99,
                "description": "It flies high",
                "quantity": 60,
                "category_id": 4
            }
        @apiSuccess (200) {Object} review Created review
        @apiSuccess (200) {id} review.id Review Id
        @apiSuccess (200) {String} review.name Short form name of review
        @apiSuccess (200) {String} review.description Long form description of review
        @apiSuccess (200) {Number} review.price Cost of review
        @apiSuccess (200) {Number} review.quantity Number of items to sell
        @apiSuccess (200) {Date} review.created_date City where review is located
        @apiSuccess (200) {String} review.image_path Path to review image
        @apiSuccess (200) {Number} review.review Average customer review of review
        @apiSuccessExample {json} Success
            {
                "id": 101,
                "url": "http://localhost:8000/reviews/101",
                "name": "Kite",
                "price": 14.99,
                "description": "It flies high",
                "quantity": 60,
                "created_date": "2019-10-23",
                "image_path": null,
                "review": 0,
            }
        """

        
        new_review = Review()
        new_review.description = request.data["description"]
        
        customer = Customer.objects.get(user=request.auth.user)
        new_review.customer = customer

        new_review.save()
        product_review = ProductReview()
        product_review.review = new_review
        product_review.product = Product.objects.get(pk=request.data["productId"])
        product_review.save()
        serializer = ReviewSerializer(
            new_review, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        @api {GET} /reviews/:id GET review
        @apiName GetReview
        @apiGroup Review
        @apiParam {id} id Review Id
        @apiSuccess (200) {Object} review Created review
        @apiSuccess (200) {id} review.id Review Id
        @apiSuccess (200) {String} review.name Short form name of review
        @apiSuccess (200) {String} review.description Long form description of review
        @apiSuccess (200) {Number} review.price Cost of review
        @apiSuccess (200) {Number} review.quantity Number of items to sell
        @apiSuccess (200) {Date} review.created_date City where review is located
        @apiSuccess (200) {String} review.image_path Path to review image
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
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        @api {PUT} /reviews/:id PUT changes to review
        @apiName UpdateReview
        @apiGroup Review
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {id} id Review Id to update
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        review = Review.objects.get(pk=pk)
        review.description = request.data["description"]

        customer = Customer.objects.get(user=request.auth.user)
        review.customer = customer

        review.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """
        @api {DELETE} /reviews/:id DELETE review
        @apiName DeleteReview
        @apiGroup Review
        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611
        @apiParam {id} id Review Id to delete
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        try:
            review = Review.objects.get(pk=pk)
            review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """
        @api {GET} /reviews GET all reviews
        @apiName ListReviews
        @apiGroup Review
        @apiSuccess (200) {Object[]} reviews Array of reviews
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
            reviews = Review.objects.all()
            item = request.query_params.get('item', None)
            if item is not None:
                reviews = Review.objects.filter(review__product__id=item)
            serializer = ReviewSerializer(reviews, many=True, context={'request': request})
            
            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)