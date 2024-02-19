from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework import status
from search.services import add_paragraphs, list_top_paragraphs
import custom_errors
import error_responses

class ParagraphView(APIView):
    def post(self, request):
        try:
            text = request.data.get("text", "")
            add_paragraphs(text=text)
        except ValidationError as e:
            return Response(data=error_responses.validation_error_resp(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(data={}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        try:
            word = request.GET.get("word", "")
            top_n = request.GET.get("top_n", "")
            paras = list_top_paragraphs(word=word, top_n=top_n)
        except ValidationError as e:
            return Response(data=error_responses.validation_error_resp(e), status=status.HTTP_400_BAD_REQUEST)
        except custom_errors.WordNotFound as e:
            return Response(data=error_responses.business_error_resp(e), status=status.HTTP_404_NOT_FOUND)
        return Response(data=paras, status=status.HTTP_200_OK)