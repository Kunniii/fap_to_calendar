#!/bin/python3

import requests
from bs4 import BeautifulSoup as bs
from termcolor import cprint
import getopt
import sys
import re
import json
from ics import Calendar, Event

def printUsage():
    h = '''
Options:
    -i  --id         : String - Your Session ID
    -o  --out        : String - Calendar output path, eg: calendar.ics (should be an absolute path)
    -y  --year       : Int    - The year you want to get info (default: current year)
    -w  --week       : Int    - Week number in that year you selected (default: current week)
        --weeks      : Int    - Week number, separated by a dot <.> (--weeks 5.6.7.8)
    -c  --check      : Perform checking if the Session is valid
        --check-only : Only perform checking, then exit.
        --json-out   : The path to save data in JSON format (should be an absolute path)
    '''
    print(h)


def checkIfLoggedOut(soup, verbose=False):
    theForm = soup.find("form", {"name": "aspnetForm"})
    if not verbose:
        if theForm['action'] == "./Default.aspx":
            raise Exception("Session ID Invalid or you might be logged out")
    else:
        cprint("\nSession checking Enabled!", "blue")
        cprint('Performing session checking...')
        print("  Username:", end=" ")
        try:
            name = soup.find("span", {"id": "ctl00_mainContent_lblStudent"})
            cprint(name.text, "green")
        except:
            cprint("Not found!", "red")

        print("  Status  :", end=" ")
        if theForm['action'] == "./Default.aspx":
            cprint("Not OK!", "red")
            raise Exception("Session ID Invalid or you might be logged out")
        else:
            cprint("OK!", "green")
        print()

def checkOnly(cookies, headers):
    cprint('\nChecking Only...', 'blue')
    response = requests.get('https://fap.fpt.edu.vn/Report/ScheduleOfWeek.aspx', cookies=cookies, headers=headers)
    soup = bs(response.text, "html.parser")
    checkIfLoggedOut(soup, True)
    exit(0)

def processTheSelectIntoArrayDictSelectedValue(select: bs) -> tuple[list, dict, str]:
    arrayOptions = []
    dictOptions = {}
    selectedOption = None
    options = select.find_all('option')
    for option in options:
        value = option['value']
        text = option.text
        dictOptions[value] = text
        arrayOptions.append(value)
        try:
            if option['selected']:
                selectedOption = value
        except:
            pass
    return arrayOptions, dictOptions, selectedOption

def processTheClass(schoolClass: bs):
    '''
    name: MLN         ? first <a> text
    status: attended  ? <font> in <p> in <td> in <tr>
    meet-url: the url ? <a>    class "label label-default" || none
    isOnline: false   ? <div>  class "online-indicator" || none
    time: 7:00-9:25   ? <span> class "label label-success" || none
    eduNextUrl: http//   ? <a>    class "label label-primary" || none
    '''

    name = None
    room = None
    status = None
    isOnline = False
    meetUrl = None
    time = None
    eduNextUrl = None
    materialUrl = None

    pattern = re.compile('\sat.+\d\s')

    def formatTime(time: str):
        time = time.replace('(', '').replace(')','')
        [timeStart, timeEnd] = time.split('-')
        [sh, sm] = timeStart.split(':')
        [eh, em] = timeEnd.split(':')
        if int(sh) < 10:
            timeStart = '0'+timeStart
        if int(eh) < 10:
            timeEnd = '0'+timeEnd
        return {"timeStart": timeStart+':00', "timeEnd": timeEnd+':00'}

    try:
        name = schoolClass.find('a').text[:6]
        status = schoolClass.find('font').text
        time = schoolClass.find("span", {"class": "label label-success"}).text
        time = formatTime(time)
        eduNextUrl = schoolClass.find("a", {"class", "label label-primary"})['href'] if schoolClass.find("a", {"class", "label label-primary"}) else None
        materialUrl = schoolClass.find("a", {"class", "label label-warning"})['href'] if schoolClass.find("a", {"class", "label label-warning"}) else None
        room = re.search(pattern, schoolClass.text).group().replace('at', '').strip()
        isOnline = True if schoolClass.find('div', {"class": "online-indicator"}) else False
        meetUrl = schoolClass.find("a", {"class": "label label-default"})['href'] if schoolClass.find("a", {"class": "label label-default"}) else None
        return {
            "name": name,
            "room": room,
            "status": status,
            "isOnline": isOnline,
            "meetUrl": meetUrl,
            "time": time,
            "eduNextUrl": eduNextUrl,
            "materialUrl": materialUrl
        }
    except:
        return {}

def turnTheTableIntoJSON(soup: bs):
    '''
    [
        {
            date: yyyy-dd-mm
            slots: {
                1: {
                    name: MLN
                    room: G505
                    status: attended
                    meet-url: the url
                    isOnline: false
                    time: 7:00-9:25
                    eduNextUrl: http//
                },
            }
        },
    ]
    '''
    data = []
    dates = [date.text for date in soup.find("div", {"id": "ctl00_mainContent_divShowDate"}).find_all("th")]
    everySlots = [slot for slot in soup.find("div", {"id": "ctl00_mainContent_divContent"}).find_all("tr")]
    year = soup.find("select", {"name": "ctl00$mainContent$drpYear"}).find("option", {"selected": "selected"}).text
    for date in dates:
        classIndex = dates.index(date) + 1
        [day, month] = date.split('/')
        _data = {"date": f"{year}-{month}-{day}", "slots": {}}
        for slot in everySlots:
            slotNumber = slot.find("td").text.strip()[-1]
            classes: bs = slot.find_all("td")
            classData = processTheClass(classes[classIndex])
            _data["slots"][slotNumber] = classData
        data.append(_data)
    return data

def turnMultipleTableToJSON(soups: list):
    data = []
    for soup in soups:
        data += turnTheTableIntoJSON(soup)
    return data

def getScheduleData(cookies, headers, check=False):
    response = requests.get('https://fap.fpt.edu.vn/Report/ScheduleOfWeek.aspx', cookies=cookies, headers=headers)
    soup = bs(response.text, "html.parser")
    checkIfLoggedOut(soup, check)
    selectThatHasYears = soup.find("select", {"name": "ctl00$mainContent$drpYear"})
    selectThatHasWeeks = soup.find("select", {"name": "ctl00$mainContent$drpSelectWeek"})
    (years, yearsDict, selectedYear) = processTheSelectIntoArrayDictSelectedValue(selectThatHasYears)
    (weeks, weeksDict, selectedWeek) = processTheSelectIntoArrayDictSelectedValue(selectThatHasWeeks)
    __VIEWSTATE: str = soup.find("input", {"name": "__VIEWSTATE"})['value']
    __EVENTVALIDATION: str = soup.find("input", {"name": "__EVENTVALIDATION"})['value']

    return soup, (years, yearsDict, selectedYear), (weeks, weeksDict, selectedWeek), (__VIEWSTATE, __EVENTVALIDATION)


def getScheduleDataWithYearAndWeek(cookies, headers, year, week, aspnetFormData, check=False):
    data = {
        '__EVENTTARGET': 'ctl00$mainContent$drpSelectWeek',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': aspnetFormData[0],
        '__EVENTVALIDATION': aspnetFormData[1],
        'ctl00$mainContent$drpYear': f'{year}',
        'ctl00$mainContent$drpSelectWeek': f'{week}',
    }
    response = requests.post('https://fap.fpt.edu.vn/Report/ScheduleOfWeek.aspx', cookies=cookies, headers=headers, data=data)
    soup = bs(response.text, "html.parser")
    checkIfLoggedOut(soup, check)
    return soup

def getScheduleDataWithYearAndWeeks(cookies, headers, year, weeks, aspnetFormData):
    soups = []
    print()
    for week in weeks:
        cprint(f'[+] Getting data: {week}', 'blue')
        soups.append(getScheduleDataWithYearAndWeek(cookies=cookies, headers=headers, year=year, week=week, aspnetFormData=aspnetFormData, check=False))
    return soups

def createIcsFromJSON(data: dict, outFile):
    from datetime import datetime
    calendar = Calendar()
    for obj in data:
        date = obj['date']
        slots = obj['slots']
        for key, value in slots.items():
            if value == {}:
                continue
            startTime = f"{date}T{value['time']['timeStart']}+07:00"
            endTime = f"{date}T{value['time']['timeEnd']}+07:00"
            cprint(f'Creating event {value["name"]}: {startTime} - {endTime}', "blue")
            e = Event()
            e.name = value['name']
            e.begin = datetime.fromisoformat(startTime)
            e.end = datetime.fromisoformat(endTime)
            e.description = f"Room: {value['room']}\n\nMeet URL: {value['meetUrl']}\n\nEduNext: {value['eduNextUrl']}"
            calendar.events.add(e)
    with open(f'{outFile}', 'w+', encoding='utf-8') as f:
        f.writelines(calendar.serialize_iter())


def main():
    outFile = "schedule.ics"
    data = []
    check = False
    jsonFile = None
    week = None
    weeks = None
    year = None
    cookies = {}
    headers = {
        'authority': 'fap.fpt.edu.vn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'origin': 'https://fap.fpt.edu.vn',
        'referer': 'https://fap.fpt.edu.vn/Student.aspx',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'user-agent': 'codechovui.dev',
    }

    argv = sys.argv[1:]
    if not argv:
        raise Exception("Session Id is REQUIRED!")
    else:
        opts, args = getopt.getopt(argv, "i:o:c+y:w:", ['id=', 'out=', 'check', 'year=', 'week=', 'weeks=', 'check-only', 'json-out='])
        #### Check options ####
        checker = []
        for option, val in opts:
            checker.append(option)
        if not any(['-i' in checker, '--id' in checker]):
            raise Exception("\nSession Id is REQUIRED!")
        #### End check options ####
        for option, value in opts:
            if option in ['-o', '--out']:
                outFile = value
            if option in ['-i', '--id']:
                cookies['ASP.NET_SessionId'] = value
            if option in ['-c', '--check']:
                check = True
            if option in ['-y', '--year']:
                year = value
            if option in ['-w', '--week']:
                week = value
            if option in ['--weeks']:
                weeks = value.split('.')
            if option in ['--check-only']:
                checkOnly(cookies, headers)
            if option in ['--json-out']:
                jsonFile = value

    soup, yearData, weekData, aspnetFormData = getScheduleData(cookies, headers, check)

    if all([year, weeks, week]):
        raise Exception("Only one option allowed: --week or --weeks")
    elif all([year, week]) or all([year, weeks]): # all para set
        if year == yearData[2] and week == weekData[2]:
            pass
        else:
            if week:
                if '.' in week:
                    raise Exception('Option -w or --week must be an Integer. Maybe you want to use --weeks')
                soup = getScheduleDataWithYearAndWeek(cookies=cookies, headers=headers, year=year, week=week, aspnetFormData=aspnetFormData, check=check)
            else:
                soup = getScheduleDataWithYearAndWeeks(cookies=cookies, headers=headers, year=year, weeks=weeks, aspnetFormData=aspnetFormData)
    elif any([year, week]) or any([year, weeks]) : # some para set
        print(year, week)
        raise Exception("Both --year and --week --weeks must be set!")
    else: # none set
        pass
    data = turnMultipleTableToJSON(soup)
    if jsonFile:
        with open(jsonFile,'w+',encoding='utf-8') as f:
            print(json.dumps(data, indent=2), file=f)
    createIcsFromJSON(data, outFile)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print()
        cprint(e, "red")
        printUsage()
        exit(0)

# ctl00$mainContent$drpSelectWeek
