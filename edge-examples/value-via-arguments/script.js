function determineTemperatureStatus(min, max, temperature) {
  const TemperatureTooHigh = "too_hot";
  const TemperatureGoodStatus = "good";
  const TemperatureTooLow = "too_low";

  if(temperature > min && temperature < max ) {
    return TemperatureGoodStatus;
  } else if ( temperature <= min) {
    return TemperatureTooLow;
  } else {
    return TemperatureTooHigh;
  }
}

function transform(publish, context) {
  const minValue = +context.arguments.minValue;
  const maxValue = +context.arguments.maxValue;

  const status = determineTemperatureStatus(minValue, maxValue, publish.payload.value);

  publish.payload.status = status;
  publish.topic = publish.topic + "/" + status;

  return publish;
}
