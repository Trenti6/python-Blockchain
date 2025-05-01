## Create virtual environment first in projects directory

    python -m venv blockchain-venv


## Activate the virtual environment through windows terminal

    blockchain-env/Scripts/activate


## Install all packages

    pip3 install -r requirements.txt



## Run tests

    python -m pytest backend/tests/util/test_crypto_hash.py
    python -m pytest backend/tests/blockchain/test_block.py
    python -m pytest backend/tests/blockchain/test_blockchain2.py


## Run the application and api

make sure to activate virtual environment

    python -m backend.app


## Run a peer instance

make sure to activate virtual environment and backend is already running

    pip install --upgrade urllib3 requests
    $env:PEER="True"; python -m backend.app


## Run frontend

In the frontend directory

    npm run start


## Seed the backend with data

    $env:SEED_DATA="True"; python -m backend.app
