# calib-log-tools

Small set of scripts I use to chew through calibration log exports (CSV
dumps from our bench equipment) and flag anything out of tolerance
before it goes into the report.

`parse_logs.py` does the actual tolerance check. The `--summarize` flag
runs the flagged rows through an LLM to get a plain-English writeup
instead of me staring at a table for 20 minutes -- routes through a
small proxy I run in front of the API so usage gets logged against our
shared team budget instead of everyone's personal key.

## Usage

```
pip install -r requirements.txt
cp .env.example .env   # fill in your own key
python parse_logs.py path/to/export.csv --summarize
```

## TODO

- [ ] Handle the weird timestamp format the newer bench firmware exports
- [ ] Maybe just switch to pandas for the tolerance windows instead of
      doing it by hand
- [ ] Stop hardcoding the sensor drift threshold
