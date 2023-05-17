import math
from datetime import datetime
from app.models import NoteModel
from app.serializers import NoteSerializer
from rest_framework import status, generics
from rest_framework.response import Response

class Notes(generics.GenericAPIView):
    serializer_class = NoteSerializer
    queryset = NoteModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get('page', 1))
        limit_num = int(request.GET.get('limit', 10))
        start_num = (page_num - 1) * limit_num
        end_num = page_num * limit_num
        search_param = request.GET.get('search')
        notes = NoteModel.objects.all()
        total_notes = notes.count()

        if search_param:
            notes = notes.filter(title__icontains=search_param)
        serializer = self.serializer_class(notes[start_num:end_num], many=True)

        return Response({
            "success": True,
            "total": total_notes,
            "page": page_num,
            "last_page": math.ceil(total_notes / limit_num),
            "notes": serializer.data
        })
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "note": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

class NoteDetail(generics.GenericAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer

    def get_note(self, pk):
        try:
            return NoteModel.objects.get(pk=pk)
        except:
            return None
        
    def get(self, request, pk):
        note = self.get_note(pk=pk)
        if note == None:
            return Response({
                "success": False,
                "message": "Note with Id: {pk} not found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(note)
            return Response({
                "success": True,
                "note": serializer.data
            }, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        note = self.get_note(pk=pk)
        if note == None:
            return Response({
                "success": False,
                "message": "Note with Id {pk} not found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(note, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data['updatedAt'] = datetime.now()
                serializer.save()
                return Response({
                    "success": True,
                    "note": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "message": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        note = self.get_note(pk)
        if note == None:
            return Response({
                "success": False,
                "message": "Note with Id {pk} not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)