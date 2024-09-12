import gspread
from datetime import datetime, date, timedelta
from dateutil.rrule import rrule, MONTHLY


def write_to_sheets(google_credentials_file, spreadsheet, worksheet, column_headers, row_data):
    gc = gspread.service_account(filename=google_credentials_file)
    sh = gc.open(spreadsheet)
    worksheet = sh.worksheet(worksheet)
    worksheet.clear()

    for i, column_header in enumerate(column_headers):
        worksheet.update_cell(1, i + 1, column_header)

    worksheet.append_rows(row_data)


def dates_from_delta(time_delta=30):
    start_date = str(date.today() - timedelta(days=time_delta)) + "T00:00:00Z"
    end_date = str(date.today()) + "T00:00:00Z"

    return start_date, end_date


def dates_formatted(start=None, end=None):
    if start:
        start_date = str(start) + "T00:00:00Z"
    else:
        start_date = str(date.today() - timedelta(days=30)) + "T00:00:00Z"
    if end:
        end_date = str(end) + "T23:59:59Z"
    else:
        end_date = str(date.today()) + "T23:59:59Z"

    return start_date, end_date


def month_map(year=None):
    if year:
        start_year = year
        end_year = str(int(year) + 1)
    else:
        start_year = str(date.today().year)
        end_year = str(int(start_year) + 1)

    start = "%s-2-1" % (start_year)
    end = "%s-1-31" % (end_year)
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()

    months = {}

    start_dates = [date for date in rrule(MONTHLY, bymonthday=1, dtstart=start_date, until=end_date)]
    end_dates = [date for date in rrule(MONTHLY, bymonthday=-1, dtstart=start_date, until=end_date)]

    for n in range(len(start_dates)):
        date_format = "%Y-%m-%d %H:%M:%S"
        start_date = str(datetime.date(datetime.strptime(str(start_dates[n]), date_format))) + "T00:00:00Z"
        end_date = str(datetime.date(datetime.strptime(str(end_dates[n]), date_format))) + "T23:59:59Z"

        months[start_date] = end_date

    return months


def filter_by_slug(invites, demo_list, start=None, end=None):
    start_date = start if start else "2000-01-01"
    end_date = end if end else str(date.today())

    filtered_invites = []
    for invite in invites["data"]["trackInvites"]:
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        created_date = datetime.date(datetime.strptime(invite["created"], date_format))
        check_start = datetime.strptime(start_date, '%Y-%m-%d').date()
        check_end = datetime.strptime(end_date, '%Y-%m-%d').date()
        if created_date >= check_start and created_date <= check_end:
            slugs = []
            for slug in invite["tracks"]:
                slugs.append(slug["slug"])
            if any(slug in demo_list for slug in slugs):
                filtered_invites.append(invite)

    invite_data = []
    for invite in filtered_invites:
        track_id = invite["id"]
        title = invite["title"] if invite["title"] != "" else invite["publicTitle"]
        invite_count = invite["inviteCount"]
        created_date = invite["created"]
        tracks = ", ".join([track["slug"] for track in invite["tracks"]])
        row = []
        row.append(track_id)
        row.append(title)
        row.append(invite_count)
        row.append(created_date)
        row.append(tracks)

        invite_data.append(row)
    return invite_data