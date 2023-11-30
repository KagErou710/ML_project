FROM python:3.11.4-bookworm
 
WORKDIR /app
RUN pip3 install flask
RUN pip3 install pandas
RUN pip3 install pandas
RUN pip3 install numpy
RUN pip3 install scikit-learn
RUN pip3 install matplotlib
RUN pip3 install requests
RUN pip3 install mlflow
EXPOSE 8080
 
COPY . /app
# RUN pip3 install -r requirements.txt
 
CMD tail -f /dev/null