
import xlwt
import datetime
from django.utils.html import strip_tags
from django.http import HttpResponse
from taskapp.models import Task



def download_task_xls():
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Task - Overview.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Task')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.num_format_str = 'yyyy-mm-dd'

    task_obj = Task.objects.all()
    header = ['Employee Name','Task', 'time','start_date', 'end_date']
    columns = header
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    survey_dict = []

    for each in task_obj:
        print(each.employee)
        survey_dict.append(
            {'employee_name':each.employee,'title': each.title, 'time': each.time, 'start_date': each.start_date, 'end_date': each.end_date})
    task_list = []
    for each in survey_dict:
        task_list.append(list(each.values()))
    task_list_updated = task_list[::-1]
    task_list_updated = [[date.strftime("%Y-%m-%d %H:%M") if isinstance(date, datetime.datetime) else date for date in row] for row
            in task_list_updated]
    for row in task_list_updated:
        row_num += 1
        for col_num in range(len(row)):
            row[col_num] = strip_tags(row[col_num])
            ws.write(row_num, col_num, row[col_num], font_style)
    now = datetime.datetime.now()
    wb.save('task_sheet_{}.xls'.format(now))
    print(response)
    return response
