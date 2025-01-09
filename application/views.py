from .serializers import sumanserializers
from .models import sumanmodel
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
import pytesseract as pyt
from PIL import Image
import PyPDF2  
from django.db import connection
import re





class ImageUploadView(APIView):
    def post(self, request, format=None,*args,**kwargs):
        
        file_list=request.FILES.getlist('file')

        for file in file_list:
            serializer = sumanserializers(data=request.data, many=True)
 
                       
            with open('' + file.name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
                                    # IMAGE
            if file.name.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif','.jfif')):
                print('THIS IS AN IMAGE')
                pyt.pytesseract.tesseract_cmd = "C:/Users/Personal/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"                    
                image = Image.open(file)                    
                text = pyt.image_to_string(image) 
                text = re.sub(r'\s+', ' ', text.strip())

                print(text)        
                serializer = sumanmodel(filename=file,textdata=text)
                serializer.save()
                print('Image ran sucessfully') 
                    
        #################################################################################
            
                                    #PDF
            elif file.name.endswith('.pdf'):
                print('THIS IS A PDF')
                fn=str(file)
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                # Loop through all the pages
                for page in pdf_reader.pages:
                # Extract text from the page
                    alltext = page.extract_text()
        
                # Append the text from this page to the variable
                    text += alltext
                    text = re.sub(r'\s+', ' ', text.strip())

                serializer = sumanmodel(filename=fn,textdata=text)                    
                serializer.save()
                print('Pdf ran sucessfully')
                
        return Response('RESPONSE', status=status.HTTP_200_OK)                 




class ImageTextView(APIView):
    def get(self,request,formant=None):
        text=''
        try:
            laststored=sumanmodel.objects.latest('id')
            serializer=sumanserializers(laststored)            
            p=serializer.data
            
            imgvalue=p['textdata']             
            return Response(imgvalue,status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'message@':str(e)},status=500)


class TableView(APIView):
    def get(self,request,format=None):
 
        try:
            
            queryset = sumanmodel.objects.all()
            serializer=sumanserializers(queryset,many=True)            
            p=serializer.data            
            return Response(p,status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'message@':str(e)},status=500)


class SearchBar(APIView):

    def get(self, request):  
        res= request.GET.get('name','')    
        queryset=sumanmodel.objects.all()
        serializers=sumanserializers(queryset,many=True)
        serialized_data = serializers.data
        # print(serialized_data)

        if res:
            print('res',  res)
            keys = serialized_data[0].keys()  # Assuming there is at least one object in the queryset            
            print(keys)  
            query='SELECT*FROM application_sumanmodel where textdata LIKE %s'
            with connection.cursor()as cursor:
                cursor.execute(query,('%'+ res +'%',))
                data=cursor.fetchall()
                result = [dict(zip(keys, row)) for row in data]
                print('114',result)
                return Response(result,status=status.HTTP_200_OK)











