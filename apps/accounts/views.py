from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from apps.accounts.models import Profile
from apps.accounts.serializers import ProfileSerializer
from apps.common.paginations import StandardPagination


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    pagination_class = StandardPagination
    parser_classes = (MultiPartParser, FormParser)
