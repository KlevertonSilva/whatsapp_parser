FROM python:3.10.12
WORKDIR /new
EXPOSE 3000
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT streamlit run streamlit.py 