from rest_framework import status, decorators, response

from toys.models import Toy
from toys.serializers import ToySerializer


@decorators.api_view(["GET", "POST"])
def toy_list(request) -> response.Response | None:
    if request.method == "GET":
        toys = Toy.objects.all()
        toys_serializer = ToySerializer(toys, many=True)
        return response.Response(toys_serializer(data=request.data))
    elif request.method == "POST":
        toys_serializer = ToySerializer(data=request.data)
        if toys_serializer.is_valid():
            toys_serializer.save()
            return response.Response(
                toys_serializer.data, status=status.HTTP_201_CREATED
            )
        return response.Response(
            toys_serializer.data, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET", "PUT", "DELETE"])
def toy_detail(request, pk):
    try:
        toy = Toy.objects.get(pk=pk)
    except Toy.DoesNotExist:
        return response.Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        toy_serializer = ToySerializer(toy)
        return response.Response(toy_serializer.data)
    elif request.method == "PUT":
        toy_serializer = ToySerializer(toy, data=request.data)
        if toy_serializer.is_valid():
            toy_serializer.save()
            return response.Response(toy_serializer.data)
        return response.Response(
            toy_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    elif request.method == "DELETE":
        toy.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
