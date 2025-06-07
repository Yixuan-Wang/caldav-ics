from os import environ
from fastapi import FastAPI, HTTPException, Query, Path
from dotenv import load_dotenv
from typing import Annotated

from caldav_ics.lib.calendar import get_calendar
from fastapi import Response

app = FastAPI()

@app.get("/calendar/{name}")
def fetch(
    *,
    name: Annotated[str, Path(..., description="Name of the calendar to fetch")],
    rename: Annotated[str | None, Query(..., description="New name for the calendar")] = None,
    color: Annotated[str | None, Query(description="Color of the calendar")] = None,
    key: Annotated[str, Query(..., description="Key for authentication")],
):
    if key != environ.get("PASSWORD"):
        raise HTTPException(status_code=403, detail="Invalid key")
    
    server = environ["CALDAV_SERVER"]   
    username = environ["CALDAV_USERNAME"]
    password = environ["CALDAV_PASSWORD"]

    calendar = get_calendar(
        url=server,
        calendar_name=name,
        username=username,
        password=password,
    )

    if calendar is None:
        raise HTTPException(status_code=404, detail=f"Calendar '{name}' not found")
    
    if color is None:
        color = "164:172:167"
    color: str

    if rename is not None:
        name = rename
    name: str
    

    calendar.add("name", name)
    calendar.add("color", color)

    ical_content = calendar.to_ical().decode("utf-8")
    
    return Response(
        content=ical_content,
        media_type="text/calendar; charset=utf-8",
        headers={
            "Content-Type": "text/calendar; charset=utf-8"
        }
    )

if __name__ == "__main__":
    load_dotenv()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
