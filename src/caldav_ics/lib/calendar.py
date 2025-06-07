from math import e
from turtle import st
from caldav import DAVClient, Calendar as CalDAVCalendar
from icalendar import Calendar

def get_all_calendar(
    url: str,
    *,
    username: str,
    password: str,
) -> list[Calendar]:
    client = DAVClient(url, username=username, password=password)

    _: list[CalDAVCalendar] = client.principal().calendars() # pyright: ignore[reportAssignmentType]
    calendars: list[Calendar] = list(map(convert_calendar, _)) # type: ignore

    return calendars

def get_calendar(
    url: str,
    calendar_name: str,
    *,
    username: str,
    password: str,
) -> Calendar | None:
    client = DAVClient(url, username=username, password=password)

    client.principal().calendars()

    calendars: list[CalDAVCalendar] = client.principal().calendars()  # type: ignore

    for calendar in calendars:
        if calendar.get_display_name() == calendar_name:            
            return convert_calendar(calendar)

    return None


def convert_calendar(
    calendar: CalDAVCalendar,
) -> Calendar:
    """
    Convert a CalDAV calendar to an iCalendar object.
    """
    ical = Calendar()
    ical.add("version", "2.0")
    ical.add("method", "PUBLISH")

    prod_id: str | None = None
    calscale: str | None = None

    for event in calendar.events():  # type: ignore
        ical_event = Calendar.from_ical(event.data)  # type: ignore

        if prod_id is None:
            prod_id = ical_event.get("PRODID")
        if calscale is None:
            calscale = ical_event.get("CALSCALE")

        for component in ical_event.walk():
            if component.name == "VEVENT":
                ical.add_component(component)

    if prod_id:
        ical.add("prodid", prod_id)
    else:
        ical.add("prodid", "-//My Calendar//EN")
    if calscale:
        ical.add("calscale", calscale)
    else:
        ical.add("calscale", "GREGORIAN")
        
    return ical

