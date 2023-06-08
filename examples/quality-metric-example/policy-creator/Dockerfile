FROM curlimages/curl:8.1.1

COPY schemas /policy-creator/schemas
COPY policies /policy-creator/policies
COPY create-policies.sh /policy-creator/create-policies.sh

WORKDIR /policy-creator

ENTRYPOINT ["./create-policies.sh"]
