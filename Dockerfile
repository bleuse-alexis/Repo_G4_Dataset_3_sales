FROM neo4j
COPY . .
RUN apt update -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install pandas
RUN pip3 install sklearn
RUN pip3 install py2neo
RUN pip3 install numpy
RUN pip3 install --upgrade py2neo
CMD python3 main.py
