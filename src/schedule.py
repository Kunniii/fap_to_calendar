import requests
from bs4 import BeautifulSoup as bs
from termcolor import cprint
import getopt, sys

cookies = {
    'ASP.NET_SessionId': 'fwhm2td3k0r4lg4ewudgfyvb'
}

headers = {
    'authority': 'fap.fpt.edu.vn',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'origin': 'https://fap.fpt.edu.vn',
    'referer': 'https://fap.fpt.edu.vn/Report/ScheduleOfWeek.aspx',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

data = {
    '__EVENTTARGET': 'ctl00$mainContent$drpSelectWeek',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': '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PSdjZW50ZXInPjI4LzAxPC90aD48dGggIGFsaWduPSdjZW50ZXInPjI5LzAxPC90aD5kAg0PFgIfBQX4BTx0cj48dGQ+U2xvdCAxIDwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyPjx0ZD5TbG90IDIgPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHI+PHRkPlNsb3QgMyA8L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48L3RyPjx0cj48dGQ+U2xvdCA0IDwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyPjx0ZD5TbG90IDUgPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHI+PHRkPlNsb3QgNiA8L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48L3RyPjx0cj48dGQ+U2xvdCA3IDwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyPjx0ZD5TbG90IDggPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj5kAg8PFgIfBQXsAjx1bD48bGk+KDxmb250IGNvbG9yPSdncmVlbic+YXR0ZW5kZWQ8L2ZvbnQ+KTogVHJ1b25nTlBDRTE1MDg0MiBoYWQgYXR0ZW5kZWQgdGhpcyBhY3Rpdml0eSAvIE5ndXnhu4VuIFBoaSBUcsaw4budbmcgxJHDoyB0aGFtIGdpYSBob+G6oXQgxJHhu5luZyBuw6B5PC9saT48bGk+KDxmb250IGNvbG9yPSdyZWQnPmFic2VudDwvZm9udD4pOiBUcnVvbmdOUENFMTUwODQyIGhhZCBOT1QgYXR0ZW5kZWQgdGhpcyBhY3Rpdml0eSAvIE5ndXnhu4VuIFBoaSBUcsaw4budbmcgxJHDoyB24bqvbmcgbeG6t3QgYnXhu5VpIG7DoHk8L2xpPiAgIDxsaT4oLSk6IG5vIGRhdGEgd2FzIGdpdmVuIC8gY2jGsGEgY8OzIGThu68gbGnhu4d1PC9saT4gPC91bD5kAgsPFgIfAGdkAhEPDxYCHwEFTTxhIGhyZWY9J2h0dHA6Ly9jYW50aG8uZnB0LmVkdS52bi9oZWxwZGVzaycgdGFyZ2V0PSdfYmxhbmsnID58IEhlbHAgRGVzayA8L2E+ZGRk2wQLMlyjqzR1VLqwCRvHZABQq71I7av9jmVWQZecHQI=',
    '__EVENTVALIDATION': '/wEdADx2aRNthBiO6GMvBi3EyvcR1XYALReTroFJdjTvD/QOPMPbrs0M9H1EydjTxJ0V+Vr2Apjxie6lWUWWqazOMDQqy4h0ifhAeGhA2+tYuqG7WlhIjK/ryS3afOfp5FzohkzYp13cP9omwpgyj8tfOyKDABIfE9keuuy5VzdSJoDlCDDarFJkh0XsarzAy8B0HqOimTcb2/iolFYKe+qDIgEgQAZnPTJ14zMFs5WO+1Jx425g742rvsJy6NWyvJ1f1k9DuqAbcSSduGGTZXEnCjl7t1bxwRMDBjM/ltH2/1qLPf1lziVZTVsGh8/QsOwQLirUAv7izDPjGHWv0cxtdFyyzeffAxCYSMnGzb8nSa+F4M6EJT/XgIQcEVR+4VdWDcLUinbPJeq8FT02AiMqRVAfVMQZ9G2edaZisToeqPDRa4NA4/MMS11kVoCIRsPPD50d9giOK4H79knwi2YQ7GaFXhn/6m64A2WKlNXZaR1dFgUtOkiMGqKxiUDESWPHJ+r78Oy43G3VefQJiryUUCXt6nq8zgY3SCNyNJvH5UXPFLExSsRuaDifXn3xREG0xxHEify/2pZqMOcC4hK7iHOGKHgkBvgOpx6GjywCEGi1BgO2fh6aVlgspRNs2BYbqNvgfXO4f5YOXhW+JkxiZiV/ji/d9j1uq90BZRQ2hvL8r0cYGDxpS7aFTmaD29B3uAsNVzFx9T0MaYiA1XarslwwKcJ9fzDj2YvDcaBWEZMVyCxERUSg84f4yLXR5F+aV+n3wyHMvalECWwVzOsG44QnO4gTty9iF/lxaJIIwEc5sRSBjQP0AE1v0SPqXQMmamChxyc2ijzS5KPt1XBvTrS1eVQFBggGV/apGjFZGDIFqBzNoKv/ZKQLF3Q5n6gKtFG+j39/RauqtaG2iEWj0hXRnNmFBrit25bwUc1AnfcGxKARoJ+YWfki4PcG/VF1o+b9dcnpDhAochHtqdWlrTrtROX4Vjz4ZrD5AYT4Jw6hHb+2sFpx4umg+7d1Sh6DX1VxlIyV5RAzJGZ+CtloaSDAJsucT3JFOJuXIFcmAuYsZvlPyqsUzMx0Vl12PH8bOVtoGeLne2montjUcNIqxpYDgE5w4Pz9jpMXo2c3dbm8x+ChFxzg4JJofBf4KFGPUu/lVrhbJalAEWPy3yZzR9xhBs6E2lrzxeN9XoMfEfdDi/QvgDWa+U7GB8EP1e+0f1Gu7ptBEFkuMzJnGucyBjYUEQKoT8Thxu2WYeF6Trc3GusC7iRLH5o3/9+k6QP/sZAEjQ8kil3ShuaMN0RMvspQzCCbd+Uvj9dY9BrGeIkosQ==',
    'ctl00$mainContent$drpYear': '2023',
    'ctl00$mainContent$drpSelectWeek': '5',
}

print("Making request...")

response = requests.post('https://fap.fpt.edu.vn/Report/ScheduleOfWeek.aspx', cookies=cookies, headers=headers, data=data)

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
