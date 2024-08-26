function transform(publish, context) {
  const topic = publish.topic;
  const metrics = publish.payload.metrics;

  metrics
    .forEach((metric) => {
      const payload = metric;
      const newTopic = topic + "/" + metric.name;

      context.branches["metrics"].addPublish({
        payload: payload,
        topic: newTopic,
      });
    });

  return publish;
}