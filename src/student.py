import requests
from bs4 import BeautifulSoup as bs
from termcolor import cprint
import sys, getopt

cookies = {
    'ASP.NET_SessionId': 'fwhm2td3k0r4lg4ewudgfyvb'
}

headers = {
    'authority': 'fap.fpt.edu.vn',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://fap.fpt.edu.vn/Report/ScheduleOfWeek.aspx',
    'sec-fetch-dest': 'document',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'user-agent': 'FUCT',
}

print("Making request...")

response = requests.get('https://fap.fpt.edu.vn/Student.aspx', cookies=cookies, headers=headers)

print("Search for terms....")

soup = bs(response.text, "html.parser")
theForm = soup.find("form", {"name":"aspnetForm"})

viewState = soup.find("input", {"name": "__VIEWSTATE"})
eventValidate = soup.find("input", {"name": "__EVENTVALIDATION"})
cprint("  The Form", "green" if theForm else "red")
if theForm['action'] == "./Default.aspx":
    cprint("  The Form is found, but you might have logged out!", "yellow")
cprint("  View State", "green" if viewState else "red")
cprint("  Event Validation", "green" if eventValidate else "red")
print()

argv = sys.argv[1:]

if not argv:
    print("No option provided!")
else:
    try:
        opts, args = getopt.getopt(argv, "o:")
        for opt, arg in opts:
            if opt in ['-o']:
                with open(arg, 'w+', encoding='utf-8') as f:
                    print(">> Write to file", arg)
                    print(response.text, file=f)
    except:
        print("Error")