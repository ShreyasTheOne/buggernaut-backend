import os

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from buggernaut.serializers import *
from buggernaut.models import *

from buggernaut_backend.settings import BASE_DIR


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @action(methods=['POST'], detail=False, url_path='deleteRem', url_name='deleteRem')
    def delete_remaining_images(self, request):
        if request.user.is_authenticated:
            editor_id = request.POST.get('editorID')
            urls = request.POST.get('urls')
            images = Image.objects.filter(editorID=editor_id)

            for i in images:
                print(i)
                if i.url.url not in urls:
                    url_tbd = BASE_DIR + i.url.url
                    print(url_tbd)
                    if os.path.exists(url_tbd):
                        i.delete()
                        os.remove(url_tbd)
            return Response({"status": "successful"})
        else:
            return Response({"Detail": "Not authenticated"})
