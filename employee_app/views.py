from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import status

# Create your views here.
class EmployeeApiView(APIView):
    def get(self, request):
        obj = Employee.objects.all()
        serializer = EmployeeSerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        
        if serializer.is_valid():
            image = serializer.validated_data.get("Photo")
            if image:
                if image.size > 5*1024*1024:
                    return JsonResponse({"Error":"Image file too large ( > 5mb )"},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"status": "Employee details created successfully"},status=status.HTTP_201_CREATED)
        
        return JsonResponse({"status": "Employee Cration failed"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateApiView(APIView):
    def get(self, request,emp_id, *args, **kwargs):
        employee_data = Employee.objects.filter(pk=emp_id).first()
        if not employee_data:
            return JsonResponse(
                {"status": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = EmployeeSerializer(employee_data)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,emp_id, *args, **kwargs):
        employee_data = Employee.objects.filter(pk=emp_id).first()
        if not employee_data:
            return JsonResponse(
                {"status": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        field_list = ["Name","Photo"]
        if "Email" in request.data and employee_data.Email != request.data["Email"]:
            field_list.append("Email")
        serializer = EmployeeSerializer(employee_data, data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data.get("Photo")
            if image:
                if image.size > 5*1024*1024:
                    return JsonResponse("Image file too large ( > 5mb )")
            serializer.save(update_fields=field_list)
            return JsonResponse({"status": "Employee details updated successfully"},status=status.HTTP_200_OK)
        return JsonResponse({"status": "Employee update failed"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,emp_id, *args, **kwargs):
        employee_data = Employee.objects.filter(pk=emp_id).first()
        if not employee_data:
            return JsonResponse(
                {"status": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        employee_data.delete()
        return JsonResponse({"status": "Object deleted!"}, status=status.HTTP_200_OK)



