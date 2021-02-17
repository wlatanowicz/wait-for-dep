# wait-for-dep

Waits for a dependency before continuing. It's ment to be used in startup scripts like Docker's entrypoint.

## Usage

```
wait-for-dep dependency-url-1 dependency-url-2 ... dependency-url-n
```

ie:

```
wait-for-dep https://my-server/healthz/ psql://user@db-host/db-name
```
