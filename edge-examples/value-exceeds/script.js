  const TemperatureTooHigh = "too_hot";
  const TemperatureGoodStatus = "good";
  const TemperatureTooLow = "too_low";
function isWithInMaxRange(temperature) {
  return temperature > 90 && temperature <= 100;
}

function isWithinMinRange(temperature) {
  return temperature >= 0 && temperature < 40;
}

function isWithInMGoodRange(temperature) {
  return !isWithInMaxRange(temperature) && !isWithinMinRange(temperature);
}

function determineTemperatureStatus(temperature) {
  const TemperatureTooHigh = "too_hot";
  const TemperatureGoodStatus = "good";
  const TemperatureTooLow = "too_low";

  if (isWithInMaxRange(temperature)) {
    return TemperatureTooHigh;
  } else if (isWithinMinRange(temperature)) {
    return TemperatureTooLow;
  } else {
    return TemperatureGoodStatus;
  }
}

function transform(publish, context) {
  const status = determineTemperatureStatus(publish.payload.value);
  publish.payload.status = status;
  publish.topic = publish.topic + "/" + status;

  return publish;
}
