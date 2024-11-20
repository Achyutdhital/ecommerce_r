from rest_framework import generics
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)




# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DeliveryAddress
from .serializers import DeliveryAddressSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DeliveryAddress
from .serializers import DeliveryAddressSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_delivery_address(request):
    serializer = DeliveryAddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_delivery_address(request, pk):
    try:
        delivery_address = DeliveryAddress.objects.get(pk=pk, user=request.user)
    except DeliveryAddress.DoesNotExist:
        return Response({'error': 'Delivery address not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DeliveryAddressSerializer(delivery_address, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_delivery_address(request, pk):
    try:
        delivery_address = DeliveryAddress.objects.get(pk=pk, user=request.user)
    except DeliveryAddress.DoesNotExist:
        return Response({'error': 'Delivery address not found'}, status=status.HTTP_404_NOT_FOUND)

    delivery_address.delete()
    return Response({'message': 'Delivery deleted successfully'},status=status.HTTP_204_NO_CONTENT)


from rest_framework.permissions import IsAuthenticated

class DeliveryAddressListView(generics.ListAPIView):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)