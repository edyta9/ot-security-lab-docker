FROM python:3.12-slim

# instalujemy konkretną wersję Pymodbus (stabilna, z sync serverem)
RUN pip install "pymodbus==2.5.3"

COPY plc.py /plc.py

CMD ["python3", "/plc.py"]
