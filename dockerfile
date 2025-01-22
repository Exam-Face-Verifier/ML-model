FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/

RUN export PIP_DEFAULT_TIMEOUT=300

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install opencv-python-headless
RUN pip install matplotlib

RUN apt-get update && apt-get install -y \
    libgdiplus \
    && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/lib/libgdiplus.so /usr/lib/libgdiplus

RUN apt-get update && apt-get install -y net-tools

RUN apt-get update && apt-get install -y libicu-dev && rm -rf /var/lib/apt/lists/*
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=true

RUN export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=true

RUN pip install qrcode
RUN apt-get update && apt-get install -y catimg

COPY ./scripts /app/

CMD ["python", "app.py" ]
