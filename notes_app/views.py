# In views.py
from django.shortcuts import render, HttpResponse, redirect
from firebase_admin import storage
from django.conf import settings
import os
from django.http import HttpResponse, Http404
from google.cloud import storage
from django.shortcuts import render
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
import requests

import mimetypes
# def upload_file(request):
#     if request.method == 'POST' and request.FILES['file']:
#         file = request.FILES['file']
#         folder_name = f'{selected_folder}'
#         print(f'the upload files is  {folder_name}')
#         destination_blob_name = f"{folder_name}/{file.name}"

#         bucket = storage.bucket()
#         blob = bucket.blob(destination_blob_name)

#         # Determine content type based on file extension
#         content_type, _ = mimetypes.guess_type(file.name)
#         if not content_type:
#             content_type = 'application/octet-stream'  # Default to generic binary data

#         # Upload file to Firebase Storage with inferred content type
#         blob.upload_from_file(file, content_type=content_type)

#         return render(request, 'upload_form.html')

#     return render(request, 'upload_form.html')


# def view_files(request):
#     # Get list of files in the 'Cyber Security' folder
#     bucket = storage.bucket()
#     blobs = bucket.list_blobs(prefix='Cyber Security/')

#     # Prepare a list of file names
#     # files = [blob.name.split('/')[-1] for blob in blobs]
#     files = [blob.name.split('/')[-1] for blob in blobs if blob.name.split('/')[-1]]
#     print(files)

#     return render(request, 'file_list.html', {'files': files})


from firebase_admin import storage
def view_files(request):
    if request.method == 'GET':
        global selected_folder
        selected_folder = request.GET.get('folder')
        print(f'this is selected folder {selected_folder}')
        if selected_folder:
            bucket = storage.bucket()
            blobs = bucket.list_blobs(prefix=selected_folder+'/')

            # Prepare a list of file names
            files = [blob.name.split('/')[-1] for blob in blobs if blob.name.split('/')[-1]]
            # print(files)

            return render(request, 'file_list.html', {'files': files})

    return render(request, 'file_list.html', {'files': []})





def download_file(request, file_name):
    bucket = storage.bucket()
    blob = bucket.blob(f'{selected_folder}/{file_name}')
    # print(blob)

    # Check if the file exists
    if not blob.exists():
        return HttpResponse("File not found", status=404)

    # Download file from Firebase Storage
    file_content = blob.download_as_bytes()

    # Determine the content type based on the file extension
    content_type, encoding = mimetypes.guess_type(file_name)
    if not content_type:
        content_type = 'application/octet-stream'

    # In a real-world scenario, you might want to serve the file using Django instead of returning it directly.
    response = HttpResponse(file_content, content_type=content_type)
    response['Content-Disposition'] = f'    attachment; filename="{file_name}"'
    return response


# def download_file(request, folder, file_name):
#     bucket = storage.bucket()
#     blob = bucket.blob(f'{folder}/{file_name}')

#     # Check if the file exists
#     if not blob.exists():
#         raise Http404("File not found")

#     # Download file from Firebase Storage
#     file_content = blob.download_as_bytes()

#     # Determine the content type based on the file extension
#     content_type, encoding = mimetypes.guess_type(file_name)
#     if not content_type:
#         content_type = 'application/octet-stream'

#     # In a real-world scenario, you might want to serve the file using Django instead of returning it directly.
#     response = HttpResponse(file_content, content_type=content_type)
#     response['Content-Disposition'] = f'attachment; filename="{file_name}"'
#     return response


def base(request):
    return render(request, 'base.html')

def setts(request):
    return render(request, 'settings.html')

def contact(request):
    return render(request, 'contact.html')




# def new_table(request):
#     data = []

#     if request.method == 'POST':
#         student_id = request.POST.get('student_id')
#         url = f"https://gnioterp.com:155/StudentAcademicReportother.aspx?StuId={student_id}&SessionId=1022&ClassId=250&SemId=403"
#         response = requests.get(url, verify=False)

#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             table = soup.find('table')

#             if table:
#                 rows = table.find_all('tr')

#                 for row in rows[4:]:
#                     cols = row.find_all('td')
#                     cols = [ele.text.strip() for ele in cols]
#                     if len(cols) == 5:  # Ensure there are exactly 5 columns
#                         data.append([cols[1], cols[2], cols[3], cols[4]])  # Skip the first column (S.No) and keep the rest
#                     elif len(cols) > 5:  # In case there are more columns, take only the relevant columns
#                         data.append([cols[1], cols[2], cols[3], cols[4]])
#             else:
#                 return HttpResponse("No table found on the page.", status=404)
#         else:
#             return HttpResponse(f"Failed to retrieve the page. Status code: {response.status_code}", status=response.status_code)
        
#         # Redirect to a different URL after successful POST
        

#     return render(request, 'new_table.html', {'data': data})



def new_table(request):
    data = []

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        section = request.POST.get('section')
        
        if section == 'A':
            class_id = 250
            sem_id = 403
        elif section == 'B':
            class_id = 1259
            sem_id = 1422
        
        elif section == 'C':
            class_id = 252
            sem_id = 407
        else:
            return HttpResponse("Invalid section selected.", status=400)
        
        url = f"https://gnioterp.com:155/StudentAcademicReportother.aspx?StuId={student_id}&SessionId=1022&ClassId={class_id}&SemId={sem_id}"
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')

            if table:
                rows = table.find_all('tr')

                for row in rows[4:]:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    if len(cols) == 5:  # Ensure there are exactly 5 columns
                        data.append([cols[1], cols[2], cols[3], cols[4]])  # Skip the first column (S.No) and keep the rest
                    elif len(cols) > 5:  # In case there are more columns, take only the relevant columns
                        data.append([cols[1], cols[2], cols[3], cols[4]])
            else:
                return HttpResponse("No table found on the page.", status=404)
        else:
            return HttpResponse(f"Failed to retrieve the page. Status code: {response.status_code}", status=response.status_code)
        
    return render(request, 'new_table.html', {'data': data})


# def fetch_data(request):
#     url = "https://gnioterp.com:155/StudentAcademicReportother.aspx?StuId=61649&SessionId=1022&ClassId=250&SemId=403"
#     response = requests.get(url, verify=False)  

#     data = []

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         table = soup.find('table')  

#         if table:
#             rows = table.find_all('tr')
            
#             for index, row in enumerate(rows[4:], start=-1):  
#                 cols = row.find_all('td')
#                 cols = [ele.text.strip() for ele in cols]
#                 if cols and index <= 18:  
#                     data.append(cols)
#         else:
#             return HttpResponse("No table found on the page.", status=404)
#     else:
#         return HttpResponse(f"Failed to retrieve the page. Status code: {response.status_code}", status=response.status_code)

#     return render(request, 'clg_f.html', {'data': data})


from django.shortcuts import render, get_object_or_404
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    images = post.images.all()
    return render(request, 'post_detail.html', {'post': post, 'images': images})