FROM python:3.8.5

RUN pip install agavepy

ADD add_notify_reactor.py /opt/
RUN chmod +x /opt/add_notify_reactor.py
ADD add_notify_requestbin.py /opt/
RUN chmod +x /opt/add_notify_requestbin.py
CMD bash
