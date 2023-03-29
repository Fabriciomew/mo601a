FROM ubuntu:18.04
RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 git -y
WORKDIR /home
COPY simulador.py ./
CMD [ "python3", "./simulador.py"]