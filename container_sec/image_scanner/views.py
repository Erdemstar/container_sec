from django.http import HttpResponse,JsonResponse

from celery.result import AsyncResult
from container_sec.settings import FLOWER_API_TASK_HTTP_URL,APP_IMAGESCAN_PATH,APP_IMAGE_SCANNER_HTTP_URL
from container_sec.celery import task_image_scan
from container_sec.helper import Helper
from image_scanner.grype_parser import GrypeParser
import json

h = Helper()
gparser = GrypeParser()

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def image_scan(request,image_name):
    result_name = "{}-{}.json".format(image_name.replace("/","-"),h.generateRandomFileName())
    task = task_image_scan.apply_async(args=[image_name,APP_IMAGESCAN_PATH,result_name])
    celery_task_id = str(AsyncResult(task.id))

    return JsonResponse({"status":"Task is created. You can control status. {}{}{}".format(APP_IMAGE_SCANNER_HTTP_URL,"status/",celery_task_id)})

def image_scan_status(request,status_id):
    response = h.httpGetRequest(FLOWER_API_TASK_HTTP_URL)
    if response is not None and status_id in response.keys():
        return JsonResponse({"status" : response[status_id]["state"] } )
    else:
        return JsonResponse({"status":"There is no valid id you entered"})

def image_scan_result(request,result_id):
    response = h.httpGetRequest(FLOWER_API_TASK_HTTP_URL)

    if result_id in response.keys():
        if response[result_id]["state"] == "SUCCESS":
            file_path = h.celeryTaskNameParser(response[result_id]["args"],1)
            image_file_name = h.celeryTaskNameParser(response[result_id]["args"],2)
            docker_file_name = h.celeryTaskNameParser(response[result_id]["args"],3)

            gparser.readJsonFile(file_path + image_file_name)
            result = gparser.final_result

            if docker_file_name is not None:
                docker_result = h.readJsonFile(file_path + docker_file_name)
                
                docker_result[-1]["image_scan_result"] = result
                result = docker_result
        
            if result is not None:
                return JsonResponse(result,safe=False)
            else:
                return JsonResponse({"status":"No result is created. You make rescan or make sure image name is proper"})
        else:
            return JsonResponse({"status":"You should wait until result create"})
    else:
        return JsonResponse({"status":"There is no id you entered"})
