# api-server

The server for the core API functionalities: An endpoint to get the CO2 footprint of a product given its `ean` number.

This uses the [Kesko API](https://kesko.portal.azure-api.net/) to get product information. It uses multiple sources ([\[1\]](http://naturerhverv.dk/fileadmin/user_upload/NaturErhverv/Filer/Tvaergaaende/Foedevarernes_klimaaftryk_tabel_1.pdf) [\[2\]](http://www.greeneatz.com/foods-carbon-footprint.html)) for the CO2 footprint of various ingredients. The server then computes the overall CO2 footprint of a product from it's ingredients.

# Setup and run

Setup the environment variables:

```sh
cp .env.example .env
```

Start the PostgreSQL database:

```sh
docker-compose up
```

Start the Flask API server:

```sh
pipenv install
pipenv run python app.py
```

The API server should now be available on `localhost:5000`!
