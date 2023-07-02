# WRAPPER PIPER

This microservice is in charge of, through an endpoint, receiving a list of ids of locations previously added with the locstorager service, sending this list of ids to an input queue, searching the locations corresponding to this list of ids, extracting their latitude and longitude to calculate the distance of these locations using the Euclidean distance formula.


## Requirements

- Python 3.11
- Docker
- Docker Compose
- Redis
- Postgres



### Running

1. Clone the repo

```
git clone https://github.com/Edmartt/wrapper-piper.git
```

2. Browse into the project folder

```
cd wrapper-piper/
```


#### Development Version with Flask

1. Create a virtual environment

```
python3 -m venv <virtual environment name>
```

2. Activate virtual environment

```
source env/bin/activate
```

3. Install dependencies

```
pip3 install -r requirements
```

4. Run

```
flask run -p <port>
```

##### Note

We need to run with custom ports because this is the microservice that process the ids stored
by another service that we'll have running in a default port (or maybe a custom one)

#### Running with Docker

1. Pull the image from Dockerhub

```
docker pull edmartt/wrapper-piper
```

2. Create a container

```
docker run --rm -p <host-port:docker-port> --env-file .env edmartt/wrapper-piper
```

##### Note

If we try to send requests to this service when is running alone with docker, we'll get an error because we don't have a database with the records for processing



#### Deploying all the services with Docker Compose

```
docker-compose up
```

This will deploy the service for saving locations, this service, a redis server, a postgres server and a worker for the process.


#### Making requests to the services deployed

We can use for this purpose clients like POSTMAN or INSOMNIA, for this case I'll use curl:

```
curl -i -H "Content-Type: application/json" -d '{"ids":["896a3a26-61ea-4973-944f-31bf29cbf87a","d6de73e3-df1a-4ccf-bfa5-fff98fbf2e18"]}' http://localhost:5000/api/v1/locations/ids
```

##### Note

Remember that you'll get those ids from the locstorager service

A success response will look like this:

```
HTTP/1.1 200 OK
Server: Werkzeug/2.3.6 Python/3.11.3
Date: Sun, 02 Jul 2023 19:11:56 GMT
Content-Type: application/json
Content-Length: 120
Connection: close

{
  "response": {
    "JOB ID": "d7451e7d-6d84-499e-a97b-b225f5bfcba1",
    "message": "ids in the inbound queue"
  }
}
```

In REDIS we'll see this as the last to elements for an inbound queue:

```
127.0.0.1:6379> LRANGE inbound -2 -1
1) "896a3a26-61ea-4973-944f-31bf29cbf87a"
2) "d6de73e3-df1a-4ccf-bfa5-fff98fbf2e18"
```

Now the result is in the outbound queue:

```
127.0.0.1:6379> LRANGE outbound -1 -1
1) "6.403878597381432"
```

We can get the result as a JSON response from api sending the job id

```
curl -i -H "Content-Type: application/json" -d '{"job_id":"d7451e7d-6d84-499e-a97b-b225f5bfcba1"}' http://localhost:5000/api/v1/locations/distance
```

A success response will look like this:

```
HTTP/1.1 200 OK
Server: Werkzeug/2.3.6 Python/3.11.3
Date: Sun, 02 Jul 2023 19:18:15 GMT
Content-Type: application/json
Content-Length: 103
Connection: close

{
  "response": {
    "distance": [
      6.403878597381432
    ],
    "message": "job finished"
  }
}
```
