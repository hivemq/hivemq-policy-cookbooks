FROM hivemq/hivemq4:4.20.0

# postgres extension
ADD extension/hivemq-postgres-extension/config.xml /opt/hivemq/extensions/hivemq-postgresql-extension/conf
ADD extension/hivemq-postgres-extension/statement-template.sql /opt/hivemq/extensions/hivemq-postgresql-extension/conf
# Copy license for HiveMQ Enterprise Extension for Postgres
# ADD postgres-extenions.elic /opt/hivemq/extensions/hivemq-postgresql-extension/conf

# prometheus
RUN curl -L https://github.com/hivemq/hivemq-prometheus-extension/releases/download/4.0.8/hivemq-prometheus-extension-4.0.8.zip -o /opt/hivemq/extensions/prometheus.zip \
    && unzip /opt/hivemq/extensions/prometheus.zip -d /opt/hivemq/extensions \
    && chgrp -R 0 /opt/hivemq/extensions/hivemq-prometheus-extension \
    && chmod -R 770 /opt/hivemq/extensions/hivemq-prometheus-extension \
    && rm /opt/hivemq/extensions/prometheus.zip