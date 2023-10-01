from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeeApiView.as_view(), name='employee'),
    path('/<int:emp_id>', views.UpdateApiView.as_view(), name='update')
]