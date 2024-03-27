# tach microservices ⚙️

Microservices to manage `Accounts` and `Transactions` between multiple accounts.


>[!WARNING]
> This project is for demo purposes only. Don't use it in production environments.

## Stack
This project stands on shoulders of:

- [Sanic](https://sanic.dev/en/): For RESTFull API.
- [meiga](https://github.com/alice-biometrics/meiga): For monad-based result type.
- [Beanie](https://beanie-odm.dev/): For MongoDB connections.
- [AIORMQ](https://github.com/mosquito/aiormq): For AMQP connections.


## Quickstart

Clone repository and use `Docker` with `docker-compose` to build and run images.

1. Clone repository
```sh
git clone git@github.com:lucaslucyk/tach-challenge.git
```

2. Create `.env` file with next values:
```ini
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=sup3r&s3cr3t
```

3. Start containers with `docker-compose`
```sh
docker-compose up -d
```

## Test
To run tests, use the utility script.

```sh
sh ./scripts/test.sh
```

## License
This project is licensed under the terms of the MIT license.

Made with ❤️ and 🧉