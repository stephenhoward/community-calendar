ARG base_image=git.enterity.com:4567/community-calendar/api:develop
From $base_image

ENV HOME /opt/calendar

WORKDIR ${HOME}

COPY app    ${HOME}/app
COPY bin    ${HOME}/bin
COPY config ${HOME}/config
COPY lib    ${HOME}/lib
COPY tests  ${HOME}/tests
