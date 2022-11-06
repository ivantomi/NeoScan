# QR Scanner App

### Get into the virtual environment

```
source venv/bin/activate
```

### Update `requirements.txt` file
1. Update the `requirements.in` file with wanted packages
2. Run `pip-compile`

### Install the new packages with
```
pip install -r requirements.txt
```

### Docker Compose commands
To build the containers simply run (This should be done each time the packages change, IE: `requirements.in`/`requirements.txt` file)
```
docker compose up --build
```

To run the containers (after they are built)
```
docker compose up
```

To get into the shell of a container use the following command (they must be running):

For **DB**:
```
docker exec -it qrscanner_db psql qrscanner -U qradmin
```

For **app**:
```
docker exec -it qrscanner_app bash
```

To get out of any of those shells use `CTRL+D`

### to-do list
1.) create a user ticket for scanning
2.) manage on-site new users (e.g. add them to the database)
3.) fix database (tables and output) + 
4.) create HTML sites for each wanted function
5.) add boolean variable for entry