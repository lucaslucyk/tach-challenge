# tach microservices ⚙️

Microservices to manage `Accounts` and `Transactions` between multiple accounts.


>[!WARNING]
> This project is for demo purposes only. Don't use it in production environments.

## Stack 🧰
This project stands on shoulders of:

- [Sanic](https://sanic.dev/en/): For RESTFull API.
- [petisco](https://github.com/alice-biometrics/petisco): For clean applications and dependency injection.
- [meiga](https://github.com/alice-biometrics/meiga): For monad-based result type.
- [Beanie](https://beanie-odm.dev/): For map MongoDB documents to Python objects (ODM).
- [pika](https://pika.readthedocs.io/en/latest/): For RabbitMQ connections on `petisco`.

## Quickstart 🚀

### Docker <img src="https://raw.githubusercontent.com/alice-biometrics/custom-emojis/master/images/docker.png" width="18">

Clone repository and use `Docker` with `docker-compose` to build and run images.

1. Clone repository
```sh
git clone git@github.com:lucaslucyk/tach-challenge.git
```

2. Check `.env` files.

3. Start containers with `docker-compose`.
```sh
docker-compose up -d
```

### Locally 💻️

1. Start dependencies services:
   1. `RabbitMQ`
   2. `MongoDB`

2. Check `.env` files.

3. Start apps with poetry:

```sh
poetry run python accounts/main.py
poetry run python transactions/main.py
```

## Test 🧪
Coming soon.

## Contact 📬️
- [GitHub](https://github.com/lucaslucyk/tach-challenge)
- [LinkedIn](https://www.linkedin.com/in/lucaslucyk/)
- [Email](mailto:lucaslucyk@gmail.com)

## License 📝
This project is licensed under the terms of the MIT license.

Made with ❤️ and 🧉