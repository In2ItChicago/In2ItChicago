# Create index on start time, end time, and organization
curl  -u admin:clipboard -v -X POST http://`printenv DOCKER_IP`:8093/query/service \
  -d "statement=create index idx_event on event(start_timestamp, end_timestamp, organization)"