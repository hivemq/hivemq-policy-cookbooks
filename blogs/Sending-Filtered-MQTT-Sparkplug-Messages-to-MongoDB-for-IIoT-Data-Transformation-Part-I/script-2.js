function isValidMetricForFanout(metric, allowList) {
  for (let i = 0; i < allowList.length; i++) {
    if (metric.startsWith(allowList[i])) {
      return true;
    }
  }
  return false;
}

function transform(publish, context) {
  const topic = publish.topic;
  const metrics = publish.payload.metrics;
  const allowList = (context.arguments.allowList || "").split(",");

  metrics
    .filter((metric) => isValidMetricForFanout(metric.name, allowList))
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