from datetime import datetime, date
from typing import Optional, Union

import icalendar


EVENT_ID = "id"
EVENT_SUMMARY = "summary"
EVENT_DESCRIPTION = "description"
EVENT_LOCATION = "location"
EVENT_STATUS = "status"
EVENT_RECURRENCE = "recurrence"
EVENT_START = "start"
EVENT_END = "end"

EVENT_FIELDS = [
    EVENT_ID,
    EVENT_SUMMARY,
    EVENT_LOCATION,
    EVENT_DESCRIPTION,
    EVENT_STATUS,
    EVENT_RECURRENCE,
    EVENT_START,
    EVENT_END,
]

EVENT_COMPARISON_FIELDS = [
    EVENT_SUMMARY,
    EVENT_DESCRIPTION,
    EVENT_LOCATION,
    EVENT_START,
    EVENT_END,
    #EVENT_RECURRENCE,  # TODO
]


def event_field(event, field: str) -> Optional[Union[str, object, datetime, date]]:
    """
    Returns the specified event value.

    :param event: the event to get the value fromm
    :param field: the name of the field to retrieve
    :type field: str
    :return: the value, can be None; summary is empty string when missing; start/end are returned as datetime objects
    """
    if field not in EVENT_FIELDS:
        raise Exception("Unknown event field: %s" % field)

    if isinstance(event, icalendar.Event):
        if field == EVENT_ID:
            return event["UID"]
        elif field == EVENT_SUMMARY:
            if "SUMMARY" in event:
                return event["SUMMARY"]
            else:
                return ""
        elif field == EVENT_DESCRIPTION:
            if "DESCRIPTION" in event:
                return event["DESCRIPTION"]
            else:
                return ""
        elif field == EVENT_STATUS:
            return event["STATUS"]
        elif field == EVENT_LOCATION:
            return event["LOCATION"]
        elif field == EVENT_RECURRENCE:
            if "RRULE" in event:
                return event["RRULE"]
            else:
                return None
        elif field == EVENT_START:
            if "DTSTART" in event:
                return event["DTSTART"].dt
            else:
                return None
        elif field == EVENT_END:
            if "DTEND" in event:
                return event["DTEND"].dt
            else:
                return None
        else:
            raise Exception("Unhandled event field: %s" % field)
    else:
        if field == EVENT_ID:
            return event["id"]
        elif field == EVENT_SUMMARY:
            if "summary" in event:
                return event["summary"]
            else:
                return ""
        elif field == EVENT_DESCRIPTION:
            if "description" in event:
                return event["description"]
            else:
                return ""
        elif field == EVENT_STATUS:
            return event["status"]
        elif field == EVENT_LOCATION:
            return event["location"]
        elif field == EVENT_RECURRENCE:
            if "recurrence" in event:
                return event["recurrence"]
            else:
                return None
        elif field == EVENT_START:
            if "start" in event:
                d = event["start"]
                if "dateTime" in d:
                    return datetime.fromisoformat(d["dateTime"])
                else:
                    return datetime.strptime(d["date"], "%Y-%m-%d").date()
            else:
                return None
        elif field == EVENT_END:
            if "end" in event:
                d = event["end"]
                if "dateTime" in d:
                    return datetime.fromisoformat(d["dateTime"])
                else:
                    return datetime.strptime(d["date"], "%Y-%m-%d").date()
            else:
                return None
        else:
            raise Exception("Unhandled event field: %s" % field)


def is_same_event(outlook, google) -> bool:
    """
    Compares the two events whether they are the same.

    :param outlook: the Outlook event
    :param google: the Google Calendar event
    :return: True if they represent the same event
    :rtype: bool
    """
    oid = event_field(outlook, EVENT_ID)
    gid = google["iCalUID"] if ("iCalUID" in google) else ""
    return oid == gid


def has_event_changed(outlook, google) -> bool:
    """
    Checks whether at least one field differ sbetween the corresponding Outlook/Google events.

    :param outlook: the Outlook event
    :param google: the Google Calendar event
    :return: True if at least one field changed
    :rtype: bool
    """
    result = False

    for field in EVENT_COMPARISON_FIELDS:
        ovalue = event_field(outlook, field)
        gvalue = event_field(google, field)
        if ovalue != gvalue:
            result = True
            break

    return result