FROM hivemq/hivemq4:4.17.0

RUN curl -L https://github.com/hivemq/hivemq-prometheus-extension/releases/download/4.0.8/hivemq-prometheus-extension-4.0.8.zip -o /opt/hivemq/extensions/prometheus.zip \
    && unzip /opt/hivemq/extensions/prometheus.zip -d /opt/hivemq/extensions \
    && chgrp -R 0 /opt/hivemq/extensions/hivemq-prometheus-extension \
    && chmod -R 770 /opt/hivemq/extensions/hivemq-prometheus-extension \
    && rm /opt/hivemq/extensions/prometheus.zip