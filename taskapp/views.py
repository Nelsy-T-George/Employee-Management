from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
import schedule
import time
import xlwt
import datetime
from django.utils.html import strip_tags
from django.http import HttpResponse
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView)
from taskapp.models import Role,Employee,Task, Comments
from taskapp.serializers import TaskSerializer, CommentSerializer
from employeetask import settings

class TaskCreateView(CreateAPIView):

    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        try:
            self.id = self.kwargs.get('id')
            employee_obj = Employee.objects.get(id=self.id)
            serializer.save(employee=employee_obj,created_by=employee_obj.email,updated_by=employee_obj.email)
        except Exception as e:
            print(e)

class TaskListView(ListAPIView):

    serializer_class = TaskSerializer

    def get_queryset(self, *args, **kwargs):
        self.id = self.kwargs.get("id")
        try:
            employee = Employee.objects.get(id=self.id)
            query_set = Task.objects.filter(employee = employee)
            return query_set
        except Exception as e:
            print(e)

class EmployeeTaskRolewiseListView(ListAPIView):

    serializer_class = TaskSerializer

    def get_queryset(self, *args, **kwargs):
        self.role = self.kwargs.get("role")
        try:
            role=Role.objects.get(name=self.role)
            employee = Employee.objects.filter(role = role)
            for each_employee in employee:
                query_set = Task.objects.filter(employee = each_employee)
            return query_set
        except Exception as e:
            print(e)

class CommentsCreateView(CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        id = self.kwargs.get('id')
        obj = Task.objects.get(id=id)
        comment_data = self.request.data.get('comment_text')
        if comment_data:
            comment_obj = Comments.objects.create(comment_text=comment_data,
                                                  created_by=self.request.user.is_superuser, updated_by=self.request.user.is_superuser)
            obj.comment.add(comment_obj)
        return obj

# EXCEL CREATION USING SCHEDULER
# def download_task_xls():
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="Task - Overview.xls"'
#
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Task')
#
#     # Sheet header, first row
#     row_num = 0
#
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     font_style.num_format_str = 'yyyy-mm-dd'
#
#     task_obj = Task.objects.all()
#     header = ['employee_name','title', 'start_date', 'end_date']
#     columns = header
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)
#     survey_dict = []
#
#     for each in task_obj:
#         print(each.employee)
#         survey_dict.append(
#             {'employee_name':each.employee,'Task': each.title, 'start_date': each.start_date, 'end_date': each.end_date})
#     task_list = []
#     for each in survey_dict:
#         task_list.append(list(each.values()))
#     task_list_updated = task_list[::-1]
#     task_list_updated = [[date.strftime("%Y-%m-%d %H:%M") if isinstance(date, datetime.datetime) else date for date in row] for row
#             in task_list_updated]
#     for row in task_list_updated:
#         row_num += 1
#         for col_num in range(len(row)):
#             row[col_num] = strip_tags(row[col_num])
#             ws.write(row_num, col_num, row[col_num], font_style)
#     now = datetime.datetime.now()
#     wb.save('task_sheet_{}.xls'.format(now))
#     print(response)
#     return response
#
# schedule.every(1).seconds.do(download_task_xls)
# # schedule.every().hour.do(download_survey_xls)
# while True:
#     # Checks whether a scheduled task
#     # is pending to run or not
#     schedule.run_pending()
#     time.sleep(1)



