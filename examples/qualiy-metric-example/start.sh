docker compose -f docker/docker-compose.yml up -d

echo "Waiting for HiveMQ REST API to become available..."
until $(curl --output /dev/null --silent --head --fail http://localhost:8889/api/v1/health/readiness); do
    sleep 1
done

SCHEMA_ID=$(curl -X POST --silent --data @./config/schema.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/schemas | jq ".id")
echo "Created schema $SCHEMA_ID."

POLICY_ID=$(curl -X POST --silent --data @./config/policy.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/policies | jq ".id")
echo "Created policy $POLICY_ID."
