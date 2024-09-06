from rest_framework import status
from rest_framework.decorators import api_view
from app_apis import serializers
from rest_framework.response import Response
from app_apis.models import InformalEvent, Matches, ScoreLinks, Sponsor

# @user_passes_test(lambda user: user.is_superuser)


def create_match(request):
    if request.method == 'POST':
        pass


@api_view(['GET'])
def get_matches(request):
    if request.method == 'GET':
        matches = Matches.objects.all()
        serializer = serializers.MatchSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_sponsors(request):
    if request.method == 'GET':
        sponsors = Sponsor.objects.all()
        serializer = serializers.SponsorSerializer(sponsors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_informal_events(request):
    if request.method == 'GET':
        sponsors = InformalEvent.objects.all()
        serializer = serializers.InformalSerializer(sponsors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_scorelinks(request):
    name = request.headers.get('name')
    sport = ScoreLinks.objects.get(name=name)

    print(sport.link)
    return Response({"link": sport.link}, status=status.HTTP_200_OK)
