from fastapi import FastAPI
import re
from datetime import datetime
from pydantic import BaseModel, Field

app = FastAPI()


def _find_next_id():
    return max(bday.bday_id for bday in bdays) + 1


class Bday(BaseModel):
    bday_id: int = Field(default_factory=_find_next_id, alias="id")
    name: str
    date: str


bdays = [
    Bday(id=1, name="Bob", date="23-02"),
    Bday(id=2, name="Mary", date="05-04"),
    Bday(id=3, name="Susan", date="12-12"),
]


def is_valid_date(entered_string):
    for match in re.finditer(r"\d\d-\d\d", entered_string):
        if match:
            found_date = datetime.strptime(match.group(0), "%d-%m")
            # fix year
            fixed_date = found_date.replace(year=datetime.today().year)
            return True, fixed_date
        else:
            return False


def calculate_days(original_date, now):
    opt1 = datetime(now.year, original_date.month, original_date.day)
    opt2 = datetime(now.year + 1, original_date.month, original_date.day)

    return ((opt1 if opt1 > now else opt2) - now).days


@app.get("/")
def read_root():
    return {"Welcome to Python-Rest-Container-Bday"}


@app.get("/mynextbday")
def instructions():
    msg = "Send your day and month /mynextbday/dd-mm"
    return msg


@app.get("/mynextbday/{date_value}")
def find_your_birthday(date_value: str):
    valid = is_valid_date(date_value)
    if not valid:
        return "Wrong date format: use dd-mm"

    else:
        days = calculate_days(valid[1], datetime.today())
        return str(days) + " days for your birthday"


@app.get("/getbdays")
async def get_bdays():
    return bdays


@app.post("/addbday", status_code=201)
async def add_bday(bday: Bday):

    valid = is_valid_date(bday.date)
    if not valid:
        return "Wrong date format"

    else:
        bdays.append(bday)
        return bday


@app.get("/getuserbday/{name}")
async def get_userbday(name: str):
    for user in bdays:
        if user.name == name:
            found_date = datetime.strptime(user.date, "%d-%m")
            fixed_date = found_date.replace(year=datetime.today().year)
            days = calculate_days(fixed_date, datetime.today())
            part1 = str(user.name) + "'s birthday is on the " + str(user.date)
            part2 = ". And it is " + str(days) + " days away."
            return part1 + part2
        else:
            return "Not user with this name"


@app.get("/myitem/{item_id}")
def read_item(item_id: str):
    return {"item_id": item_id}

