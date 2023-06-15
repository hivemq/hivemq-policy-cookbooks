FROM hivemq/hivemq4:4.16.0

# postgre
ADD extension/hivemq-postgresql-extension-0.1.0-RC-1-proguarded.zip /opt/hivemq/extensions

RUN    unzip /opt/hivemq/extensions/hivemq-postgresql-extension-0.1.0-RC-1-proguarded.zip -d /opt/hivemq/extensions \
    && chgrp -R 0 /opt/hivemq/extensions/hivemq-postgresql-extension \
    && chmod -R 770 /opt/hivemq/extensions/hivemq-postgresql-extension

ADD extension/hivemq-postgres-extension/config.xml /opt/hivemq/extensions/hivemq-postgresql-extension/conf
ADD extension/hivemq-postgres-extension/statement-template.sql /opt/hivemq/extensions/hivemq-postgresql-extension/conf

# prometheus
RUN curl -L https://github.com/hivemq/hivemq-prometheus-extension/releases/download/4.0.8/hivemq-prometheus-extension-4.0.8.zip -o /opt/hivemq/extensions/prometheus.zip \
    && unzip /opt/hivemq/extensions/prometheus.zip -d /opt/hivemq/extensions \
    && chgrp -R 0 /opt/hivemq/extensions/hivemq-prometheus-extension \
    && chmod -R 770 /opt/hivemq/extensions/hivemq-prometheus-extension \
    && rm /opt/hivemq/extensions/prometheus.zip