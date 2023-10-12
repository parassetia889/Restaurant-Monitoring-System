import uuid
from django.http import HttpResponse, JsonResponse
from .utils import generate_report, get_report_status_from_db, get_report_data_from_db


# Create your views here.
def trigger_report(request):
    try:
        # Trigger report generation and return a report_id
        report_id = uuid.uuid4()
        print("calling generate report")
        generate_report(report_id)
        return JsonResponse({"report_id": report_id})
    except Exception as e:
        return JsonResponse(
            {
                "error_message": "Something went Wrong",
                "Error_code": 500,
                "error": str(e),
            }
        )


def get_report(request):
    try:
        report_id = request.GET.get("report_id")
        if not report_id:
            return JsonResponse({"error": "Missing report ID", "error_code": 400})

        report_status = get_report_status_from_db(report_id)
        if not report_status:
            return JsonResponse({"error": "Invalid report ID", "error_code": 400})

        if report_status == "Running":
            return JsonResponse(
                {"status": "Running", "message": "Success", "error_code": 200}
            )
        elif report_status == "Complete":
            report_data = get_report_data_from_db(report_id)
            if report_data:
                return HttpResponse(report_data, content_type="text/csv")
            else:
                return JsonResponse(
                    {"error": "Failed to retrieve report data", "error_code": 400}
                )
    except Exception as e:
        return JsonResponse(
            {
                "error_message": "Something went Wrong",
                "Error_code": 500,
                "error": str(e),
            }
        )
