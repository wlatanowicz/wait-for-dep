# wait-for-dep

Waits for a dependency before continuing. It's ment to be used in startup scripts like Docker's entrypoint.

## Installing

```
pip install wait-for-dep
```

## Usage

```
wait-for-dep dependency-url-1 dependency-url-2 ... dependency-url-n
```

ie:

```
wait-for-dep https://my-server/healthz/ psql://user@db-host/db-name
```


# Available checks

## HTTP(s)

HTTP and HTTPS are available by default. Follows redirects; only response with HTTP code 2XX is accepted as valid.

### Accepted URL schemas
* http://
* https://

### Example
```
wait-for-dep https://my-server/healthz/ http://my-server/healthz/
```


## PostgreSQL

RDBMS has to accept connection and allow to perform simple SELECT query.

### Installation
```
pip install wait-for-dep[postgres]
```

### Accepted URL schemas
* postgres://
* postgresql://
* psql://

### Example
```
wait-for-dep psql://admin:password@db-host/db_name
```


## MySQL

RDBMS has to accept connection and allow to perform simple SELECT query.

### Installation
```
pip install wait-for-dep[mysql]
```

### Accepted URL schemas
* mysql://

### Example
```
wait-for-dep mysql://admin:password@db-host/db_name
```


## Redis

Rdis has to accept connection to selected database (defaults to 0).

### Installation
```
pip install wait-for-dep[redis]
```

### Accepted URL schemas
* redis://

### Example
```
wait-for-dep redis://redis-host/5
```


## Memcached

Memcached has to accept connection.

### Installation
```
pip install wait-for-dep[memcached]
```

### Accepted URL schemas
* memcached://

### Example
```
wait-for-dep memcached://memcached-host/
```


## MongoDB

MongoDB has to accept connection.

### Installation
```
pip install wait-for-dep[mongodb]
pip install wait-for-dep[mongodb_srv]
```

### Accepted URL schemas
* mongodb://
* mongodb+srv:// #Requires mongodb_srv bundle

### Example
```
wait-for-dep mongodb://admin:password@db-host/db_name
wait-for-dep mongodb+srv://admin:password@db-host/db_name
```


## RabbitMQ

RabbitMQ has to accept connection to given vhost. You can use optional querystring params `require_queue` and `require_exchange` to additionaly check if particular queue or exchange exists (check will fail otherwise).

### Installation
```
pip install wait-for-dep[amqp]
```

### Accepted URL schemas
* amqp://

### Example
```
wait-for-dep amqp://admin:password@rabbit-host/vhost
wait-for-dep amqp://admin:password@rabbit-host/vhost?require_queue=myqueue
wait-for-dep amqp://admin:password@rabbit-host/vhost?require_exchange=myexchange
wait-for-dep amqp://admin:password@rabbit-host/vhost?require_exchange=myexchange&require_exchange=mysecondexchange&require_queue=myqueue&require_queue=mysecondqueue
```


## Apache Kafka

Kafka has to accept connection. In HA mode (node count > 1) only one node is required to accept the connection.

### Installation
```
pip install wait-for-dep[kafka]
```

### Accepted URL schemas
* kafka://

### Example
```
wait-for-dep kafka://kafka-host/
wait-for-dep kafka://kafka-first-host/,kafka://kafka-second-host/
```


## TCP

Plain TCP is available by default. Service port is required.

### Accepted URL schemas
* tcp://

### Example
```
wait-for-dep tcp://my-server:7624
```


## Unix

Unix sockets are available by default.

### Accepted URL schemas
* unix://

### Example
```
wait-for-dep unix:///var/run/docker.sock
```
