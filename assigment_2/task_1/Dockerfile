FROM python:3.8
RUN apt install git
WORKDIR /bot
RUN cd /bot/
RUN git clone https://github.com/Mapk58/SDwP 
RUN pip3 install -r /bot/SDwP/assigment_2/task_1/requirements.txt
ENV BOT_TOKEN=5626960040:AAH2qlqSw54S1kfuN9RLnnWpJveNWk7MUh0
WORKDIR /bot/SDwP/assigment_2/task_1/bot/
CMD ["python3","-u" ,"main.py" ] 