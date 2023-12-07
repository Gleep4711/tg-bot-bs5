# # Отдельный сборочный образ
# FROM python:3.11-slim-bullseye as compile-image
# RUN python -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"
# COPY requirements.txt .
# RUN pip install --no-cache-dir --upgrade pip \
#  && pip install --no-cache-dir -r requirements.txt

# # Итоговый образ, в котором будет работать бот
# FROM python:3.11-slim-bullseye
# COPY --from=compile-image /opt/venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"
# WORKDIR /app
# # COPY bot /app/bot
# CMD ["python", "-m", "bot"]


# Build
FROM python:3.11-alpine
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "bot"]

# docker build -t bs5 . && docker run -d --name bs5_bot --restart unless-stopped --volume "$(pwd)":/app --network redis bs5