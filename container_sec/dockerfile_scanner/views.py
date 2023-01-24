from django.shortcuts import render,HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

from container_sec.settings import APP_DOCKERFILE_PATH,APP_IMAGE_SCANNER_HTTP_URL
from dockerfile_scanner.df import DF
from container_sec.helper import Helper
from container_sec.celery import task_image_scan
from celery.result import AsyncResult

helper = Helper()

# Create your views here.
def index(request):
    return HttpResponse("Erdeemstar")

def scanner(request):
    if request.method == "GET":
        return render(request,"form.html")
    elif request.method == "POST":
        file = request.FILES['file']
        fs = FileSystemStorage(location=APP_DOCKERFILE_PATH)
        filename = file.name + helper.generateRandomFileName()
        fs.save(filename, file)

        df = DF(APP_DOCKERFILE_PATH + filename)
        df.startAudit()
        print (df.result)

        return JsonResponse(df.final_result,safe=False)
    else:
        return HttpResponse("Haata")


def detail_scanner(request):
    if request.method == "GET":
        return render(request,"form.html")
        
    elif request.method == "POST":
        file = request.FILES['file']
        fs = FileSystemStorage(location=APP_DOCKERFILE_PATH)
        filename = file.name + helper.generateRandomFileName()
        fs.save(filename, file)

        df = DF(APP_DOCKERFILE_PATH + filename)
        df.startAudit()

        dockerfile_file_name = "{}-{}.json".format("docker_file-" + df.readBaseimageFromDockerfile().replace("/","-"),helper.generateRandomFileName())

        helper.writeFile(APP_DOCKERFILE_PATH + dockerfile_file_name, df.result)

        image_fila_name = "{}-{}.json".format("image_scan-" + df.readBaseimageFromDockerfile().replace("/","-"),helper.generateRandomFileName())

        task = task_image_scan.apply_async(args=[df.readBaseimageFromDockerfile(),APP_DOCKERFILE_PATH,image_fila_name,dockerfile_file_name])
        celery_task_id = str(AsyncResult(task.id))

        return JsonResponse({"status":"Task is created. You can control status. {}{}{}".format(APP_IMAGE_SCANNER_HTTP_URL,"status/",celery_task_id)})
    else:
        return HttpResponse("Haata")

