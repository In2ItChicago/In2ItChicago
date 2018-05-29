# Map server paths
curl  -u Administrator:password -v -X POST http://`printenv DOCKER_IP`:8091/nodes/self/controller/settings \
  -d "%2Fopt%2Fcouchbase%2Fvar%2Flib%2Fcouchbase%2Fdata& \
	index_path=%2Fopt%2Fcouchbase%2Fvar%2Flib%2Fcouchbase%2Fdata"

# Set host IP
curl  -u Administrator:password -v -X POST http://`printenv DOCKER_IP`:8091/node/controller/rename \
  -d "hostname=127.0.0.1"

# Set index storage
curl  -u Administrator:password -v -X POST http://`printenv DOCKER_IP`:8091/settings/indexes \
  -d "storageMode=forestdb"

# Set cluster name, query memory quota, and index memory quota
curl  -u Administrator:password -v -X POST http://`printenv DOCKER_IP`:8091/pools/default \
  -d "clusterName=clipboard&memoryQuota=398&indexMemoryQuota=398"

# Disable full text search (for now)
curl  -u Administrator:password -v -X POST http://`printenv DOCKER_IP`:8091/node/controller/setupServices \
  -d "services=kv%2Cindex%2Cn1ql"

# Change default user/pass
curl  -u Administrator:password -v -X POST http://`printenv DOCKER_IP`:8091/settings/web \
  -d "password=clipboard&username=admin&port=SAME"

# Create event bucket
curl  -u admin:clipboard -v -X POST http://`printenv DOCKER_IP`:8091/pools/default/buckets \
  -d "name=event&bucketType=membase&autoCompactionDefined=false&evictionPolicy=fullEviction& \
  threadsNumber=3&replicaNumber=0&replicaIndex=0&ramQuotaMB=398&flushEnabled=0"
