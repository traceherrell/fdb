# build ycsb image
docker build -t traceherrell/ycsb .

# push to docker hub
docker push traceherrell/ycsb