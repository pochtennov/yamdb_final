from rest_framework import mixins, viewsets


class CreateDelListViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    Viewset for viewing, creating, delete entities
    """
    pass
