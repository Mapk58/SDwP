FROM python:3.8
RUN apt install git
WORKDIR /bot
RUN git clone https://github.com/TheARWrench/SDwP --branch klpkw
RUN ls /bot/
RUN pip3 install -r /bot/SDwP/assigment_2/task_1/requirements.txt
ENV BOT_TOKEN=5744036821:AAGN_x0oQMWmMvl1VfhYv_Vdcb2t0aSW5Nw
WORKDIR /bot/SDwP/assigment_2/task_1/bot/
RUN python3 main.py