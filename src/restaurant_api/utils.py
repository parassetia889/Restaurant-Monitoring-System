from datetime import datetime
import json

from restaurant_api.models import Report, Store

from restaurant_api.time import compute_uptime

# def get_report(request):
#     report_id = request.GET.get('report_id')

#     if is_report_generation_complete(report_id):
#         # Generate and return the CSV report
#         csv_report = generate_csv_report(report_id)
#         response = HttpResponse(csv_report, content_type='text/csv')
#         response['Content-Disposition'] = f'attachment; filename="restaurant_report.csv"'
#         return response
#     else:
#         return JsonResponse({'status': 'Running'})


def is_report_generation_complete(report_id):
    report = Report.objects.filter(report_id=report_id).first()
    if report is None:
        return None
    else:
        return report.status


def get_report_data_from_db(report_id):
    """
    Retrieves the report data from the database for a given report_id.
    """
    report = Report.objects.filter(report_id=report_id).first()

    if report is None:
        raise ValueError(f"No report found for report_id: {report_id}")

    return report.data


def generate_report(report_id):
    report = Report.objects.create(report_id=report_id, status="Running", data="")
    report_data = []

    # Loop through each store
    for store in Store.objects.all():
        uptime, downtime = compute_uptime(store.id)

        print("arrived")
        report_data.append(
            {
                "store_id": store.id,
                "status": store.status,
                "uptime": round(uptime, 2),
                "downtime": round(downtime, 2),
            }
        )

        # Update report object with status and completed_at
    report.status = "Complete"
    print("report gene completed")
    report.completed_at = datetime.utcnow()

    # Update report data object with generated report data
    report.data = json.dumps(report_data)

    report.save()

    return report


def get_report_status_from_db(report_id):
    report = Report.objects.filter(report_id=report_id).first()
    if report is None:
        return None
    else:
        return report.status

    # store_id = store.store_id

    # # Get the timezone for the store (default to 'America/Chicago' if not provided)
    # timezone_str = get_store_timezone(store_id)

    # # Get the business hours for the store (default to 24/7 if not provided)
    # business_hours = BusinessHours.objects.filter(store=store_id).first()
    # if business_hours is None:
    #     start_time = datetime.strptime('00:00', '%H:%M').time()
    #     end_time = datetime.strptime('23:59', '%H:%M').time()
    # else:
    #     start_time = business_hours.start_time_local
    #     end_time = business_hours.end_time_local

    # # Calculate time intervals within business hours
    # current_time = max_timestamp.astimezone(timezone.get_timezone(timezone_str))
    # interval_start = datetime(current_time.year, current_time.month, current_time.day, start_time.hour, start_time.minute)
    # interval_end = datetime(current_time.year, current_time.month, current_time.day, end_time.hour, end_time.minute)

    # # Calculate the interval size (in minutes)
    # interval_size = int((interval_end - interval_start).total_seconds() / 60)

    # # Calculate uptime and downtime based on observations
    # observations = Store.objects.filter(store_id=store_id, timestamp_utc__gte=max_timestamp - timedelta(weeks=1))
    # uptime = 0
    # downtime = 0
    # last_observation = None

    # for observation in observations:
    #     observation_time = observation.timestamp_utc.astimezone(timezone.get_timezone(timezone_str))
    #     if interval_start <= observation_time <= interval_end:
    #         if observation.status == 'active':
    #             if last_observation is not None and last_observation.status == 'inactive':
    #                 downtime += (observation_time - last_observation.timestamp_utc).total_seconds() / 60
    #         else:
    #             if last_observation is not None and last_observation.status == 'active':
    #                 uptime += (observation_time - last_observation.timestamp_utc).total_seconds() / 60
    #         last_observation = observation

    # # Extrapolate uptime and downtime to the entire interval
    # extrapolated_uptime = (uptime / interval_size) * 60  # in minutes
    # extrapolated_downtime = (downtime / interval_size) * 60  # in minutes

    # # Store the results in dictionaries
    # uptime_dict[store_id] = extrapolated_uptime
    # downtime_dict[store_id] = extrapolated_downtime

    # Generate the report in CSV format
    # report_filename = 'report.csv'
    # with open(report_filename, 'w', newline='') as report_file:
    #     fieldnames = ['store_id', 'uptime_last_hour(in minutes)', 'downtime_last_hour(in minutes)']
    #     writer = csv.DictWriter(report_file, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for store_id in uptime_dict.keys():
    #         writer.writerow({
    #             'store_id': store_id,
    #             'uptime_last_hour(in minutes)': round(uptime_dict[store_id], 2),
    #             'downtime_last_hour(in minutes)': round(downtime_dict[store_id], 2),
    #         })

    # return report_filename
