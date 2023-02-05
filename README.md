# FAP Calender to an ics file

This shit will need some of your info, like a `session id`.

No worries, it does not sent everywhere, it stay in your machine.

## Usage

First, install the requirements.

```bash
pip install -r requirements.txt
```

Then use the `main.py` to run with some value.

```bash
# Download week 5 6 7 8 9 ... 16 17 of year 2023
py main.py -i <your-session-id> --weeks 5.6.7.8.9.10.11.12.13.14.15.16.17 --year 2023

# Or Download specific week. Eg: week 15 of 2023
py main.py -i <your-session-id> --w 15 --y 2023

# Or download at your current week :)
py main.py -i <your-session-id>
```

After that import the created `schedules.ics` file to your prefer calendar.
