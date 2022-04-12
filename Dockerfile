FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel

RUN apt-get update
RUN apt-get install -y git

RUN git clone https://github.com/tsdocode/gpt-wrapper.git
WORKDIR "./gpt-wrapper"

RUN pip install -r requirements.txt --force

# COPY something.txt .
COPY load_model.py .

RUN python load_model.py


CMD ["python","trainer.py","-i","base_data/wikisql.txt","-e","3", "-p" , "./125, "-c" , "True"]