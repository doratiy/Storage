from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from datetime import datetime, timedelta, timezone


def storage_information_view(request):
    non_closed_visits = []
    visits = Visit.objects.all()

    for visit in visits:
        if visit.leaved_at is None:
            entered = localtime(visit.entered_at)
            entered_at = datetime.fromisoformat(f"{entered}")
            time_now = datetime.now(timezone(timedelta(hours=3)))
            duration = time_now - entered_at
            entered_at = entered_at.strftime("%d.%m.%Y %H:%M")
            dictionary = {
                'who_entered': visit.passcard.owner_name,
                'entered_at': entered_at,
                'duration': str(duration).split(".")[0],
            }
            non_closed_visits.append(dictionary)
        else:
            continue

    context = {
        'non_closed_visits': non_closed_visits,
    }

    return render(request, 'storage_information.html', context)
