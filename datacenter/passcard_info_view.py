import datetime
from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from datetime import datetime, timedelta, timezone
from django.shortcuts import get_object_or_404


def get_duration(visit):
    entered_at = datetime.fromisoformat(f"{localtime(visit.entered_at)}")
    leaved_at = datetime.fromisoformat(f"{localtime(visit.leaved_at)}")
    time_now = datetime.now(timezone(timedelta(hours=3)))

    if visit.leaved_at is not None:
        duration = leaved_at - entered_at
    else:
        duration = time_now - entered_at
    return duration


def is_visit_long(duration):
    limit = timedelta(hours=1)
    if duration > limit:
        return "Подозрителен"
    else:
        return "Не подозрительный"

def passcard_info_view(request, passcode):
    this_passcard_visits = []
    passcard = get_object_or_404(Passcard, passcode=passcode)
    passcard_visits = Visit.objects.filter(passcard=passcard)

    for visit in passcard_visits:
        duration = get_duration(visit)
        status = is_visit_long(duration)
        entered_at = datetime.fromisoformat(f"{localtime(visit.entered_at)}")

        dictionary = {
            'entered_at': entered_at,
            'duration': duration,
            'is_strange': status
        }

        this_passcard_visits.append(dictionary)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }

    return render(request, 'passcard_info.html', context)
