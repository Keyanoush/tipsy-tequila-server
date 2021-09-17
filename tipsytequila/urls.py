from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from tipsytequilaapi.models import *
from tipsytequilaapi.views import *

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'products', Products, 'product')
# router.register(r'lineitems', LineItems, 'orderproduct')
router.register(r'customers', Customers, 'customer')
router.register(r'users', Users, 'user')
router.register(r'orders', Orders, 'order')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth$', obtain_auth_token),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
]