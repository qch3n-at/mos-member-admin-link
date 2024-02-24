from members.models import get_active_and_future_members
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.core.exceptions import BadRequest
from django import forms
from django.views.generic import CreateView
from django.core.exceptions import PermissionDenied
from .models import Thing
from .models import ThingEvent
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError


def check_permissions(request, thing_slug):
    try:
        supplied_token = request.META["HTTP_X_TOKEN"]
    except LookupError:
        raise BadRequest(
            "curl https://metalab.at/things/keys/THING -H 'X-TOKEN: get_this_from_vorstand'",
        )

    thing = get_object_or_404(Thing, slug=thing_slug)

    if thing.token != supplied_token:
        raise PermissionDenied()

    return thing


@csrf_exempt
def thingusers_list(request, thing):
    thing = check_permissions(request, thing)

    members_with_thing = get_active_and_future_members().filter(thingusers__thing=thing)

    text = '\n'.join(
        (m.contactinfo.key_id or "") + "," + m.username
        for m in members_with_thing
    )
    return HttpResponse(text, content_type='text/plain')


class ThingEventCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), to_field_name="username")

    class Meta:
        model = ThingEvent
        fields = (
            "thing",
            "user",
            "kind",
            "usage_seconds",
        )


@csrf_exempt
@require_POST
def thingusers_usage(request, thing):
    thing = check_permissions(request, thing)

    data = request.POST.copy()
    data["thing"] = thing.pk
    form = ThingEventCreationForm(data=data)

    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    form.save()

    return HttpResponse(status=201)
