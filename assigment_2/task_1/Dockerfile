FROM python3.8 AS builder
RUN apt install git
WORKDIR /bot
RUN git clone https://github.com/Mapk58/SDwP
RUN wget https://klpkw.one/innolearn/F22/SDwP/rq.txt
RUN pip3 install -r rq.txt
ENV BOT_TOKEN=5744036821:AAGN_x0oQMWmMvl1VfhYv_Vdcb2t0aSW5Nw
WORKDIR /bot/SDwP/assigment_2/task_1/bot/
RUN python3 main.py