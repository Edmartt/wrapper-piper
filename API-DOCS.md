API Documentation
-----------------------

## Locstorager Service

#### SAVE LOCATIONS

Returns the ID of the location saved.

**Note**

For now, just save one location for each request, please


* **URI** 

  /api/v1/locations

* **Methods:**
  
  `POST`
  
* **Body**
  * **Data params**
    * name: string
    * latitude: float
    * longitude: float

  example:
      
  * {"name":"<location-name>", "latitude":5.6, "longitude":8.9}

* **Success Response:**

  * **Code:** 201 CREATED <br />
    **Content:** `{"location_id": "384a1f7a-466f-444d-b9f5-c372efd8c644"}`

* **Error Response:**
  
  * **Code:** 404 NOT FOUND <br />
    **Content:** `"response": "location not found"`

<br />
#### Get Locations:

Return all existant locations in the database.

* **URL** 

  /api/v1/locations

* **Methods:**
  
  `GET`

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{
    "locations": [
		{
			"id": "522bbd28-9118-4c8d-9fa1-effddbf5aacf",
			"latitude": 12.3467,
			"longitude": 9.12678,
			"name": "elm street"
		},
		{
			"id": "5d39b607-8d83-4806-ad7f-0eaf55a5d3dd",
			"latitude": 12.3467,
			"longitude": 9.12678,
			"name": "st mary avenue"
		}]
}`


<br />
#### **Get Location**

  Returns a json with the requested location.

* **URI**

  /api/v1/locations/:location_id

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `id=[UUID]`


* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{ "location": {
		"id": "522bbd28-9118-4c8d-9fa1-effddbf5aacf",
		"latitude": 12.3467,
		"longitude": 9.12678,
		"name": "elm street"
	} }`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ "response": "location not found" }`



#### Note

the locstorager service will be forwarded to the port 5600, this can be changed in the docker-compose file



<br />
#### Making requests to the locstorager deployed with docker-compose

We can use for this purpose clients like POSTMAN or INSOMNIA, for this case I'll use curl:

```
curl -i -H "Content-Type: application/json" -d '{"name":"location4", "longitude":11.4, "latitude":5.456}' http://localhost:5600/api/v1/locations
```


A success response will look like this:

```
HTTP/1.1 201 CREATED
Server: Werkzeug/2.3.6 Python/3.11.3
Date: Sun, 02 Jul 2023 19:11:56 GMT
Content-Type: application/json
Content-Length: 120
Connection: close

{
	"location_id": "384a1f7a-466f-444d-b9f5-c372efd8c644"
}
```


Now for getting a single location we can send the following request:

```
curl -i -H "Content-Type: application/json" 'http://localhost:5600/api/v1/locations/5d39b607-8d83-4806-ad7f-0eaf55a5d3dd?='
```

A success response will look like this:

```
HTTP/1.1 200 OK
Server: Werkzeug/2.3.6 Python/3.11.3
Date: Sun, 02 Jul 2023 23:12:48 GMT
Content-Type: application/json
Content-Length: 154
Connection: close

{
  "location": {
    "id": "5d39b607-8d83-4806-ad7f-0eaf55a5d3dd",
    "latitude": 12.3467,
    "longitude": 9.12678,
    "name": "st mary avenue"
  }
}
```
    
For getting all the locations:

```
curl -i -H "Content-Type: application/json" http://localhost:5600/api/v1/locations
```


<br/>
## Wrapper-Piper Service


#### Send Locations IDS

Returns the ID of the location saved.

* **URI** 

  /api/v1/locations/ids

* **Methods:**
  
  `POST`
  
* **Body**
  * **Data params**
    * ids: array[string]

  example:
      
  * `{"ids":["522bbd28-9118-4c8d-9fa1-effddbf5aacf", "896a3a26-61ea-4973-944f-31bf29cbf87a"]}`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "response": { "JOB ID": "cefb8958-f8e3-4558-a3ca-2fdf36ee684a", "message": "ids in the inbound queue"} }`

* **Error Response:**
  
  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"response": "ids not found in database"}`

    Or

    **Code:** 400 BAD REQUEST<br />
    **Content:** `{"response": "some of the ids does not exists"}`




#### Note

the wrapper-piper service will be forwarded to the port 5700, this can be changed in the docker-compose file

This will deploy the service for saving locations, this service, a redis server, a postgres server and a worker for the process.


<br />
#### Making requests to the wrapper-piper service deployed with docker-compose

We can use for this purpose clients like POSTMAN or INSOMNIA, for this case I'll use curl:

```
curl -i -H "Content-Type: application/json" -d '{"ids":["896a3a26-61ea-4973-944f-31bf29cbf87a","d6de73e3-df1a-4ccf-bfa5-fff98fbf2e18"]}' http://localhost:5000/api/v1/locations/ids
```

#### Note

Remember that you'll get those ids from the [locstorager service](https://github.com/Edmartt/locstorager)

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
