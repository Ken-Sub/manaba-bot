FROM python:3.9.7-slim-buster
ENV PYTHONUNBUFFERED=1

# ARG USERNAME=kensab
# ARG GROUPNAME=developer
# ARG UID=1000
# ARG GID=1000
# RUN groupadd -g ${GID} ${GROUPNAME} && \
#     useradd -m -s /bin/bash -u ${UID} -g ${GID} ${USERNAME}

# USER ${USERNAME}
WORKDIR /usr/src/app
COPY ./work .

RUN pip install --upgrade pip && pip uninstall django && pip install -r requirements.txt
