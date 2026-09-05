# Standard-library Python only — no pip install step, no dependency drift.
FROM apify/actor-python:3.11

COPY . ./

# Fail the BUILD, not the first paying run, if the source does not even import.
RUN python3 -c "import ast,sys; [ast.parse(open(f).read()) for f in ('src/main.py','src/platforms.py')]" \
 && echo 'source parses'

CMD ["python3", "src/main.py"]
