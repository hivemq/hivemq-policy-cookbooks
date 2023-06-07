FROM curlimages/curl:latest

COPY schemas /policy-creator/schemas
COPY policies /policy-creator/policies
COPY create-policies.sh /policy-creator/create-policies.sh

WORKDIR /policy-creator

ENTRYPOINT ["./create-policies.sh"]
