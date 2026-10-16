FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8501

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && groupadd --system lotlens \
    && useradd --system --gid lotlens --home-dir /home/lotlens --create-home lotlens

COPY app.py ./app.py
COPY LINE-04_Production_Quality_Log.csv ./LINE-04_Production_Quality_Log.csv
COPY lotlens ./lotlens
COPY data ./data
COPY assets ./assets
COPY logos ./logos
COPY .streamlit ./.streamlit

RUN chown -R lotlens:lotlens /app
USER lotlens

EXPOSE 8501

CMD ["sh", "-c", "streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT:-8501} --server.headless=true"]
