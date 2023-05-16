# python-rest-container-bday
A simple python API container that helps you to calculate how many days until your birthday.

## Environment Setup
You will need to have python3 and pip installed.
```
pip3 install fastapi uvicorn
pip3 install typing optional
```

---
## Container Setup
### Build your container

```
docker build -t python-bday-image:v0.1 .
```


### Run your container

```
docker run -d --name mybday-container -p 8000:80 python-bday-image:v0.1
```

## Run some RestAPI examples

Basic get calls:
```
# Welcome message
localhost:8000

# Get saved bdays
localhost:8000/getbdays

# Calculate how long until your next bday
localhost:8000/mynextbday/16-05
```

Post and save a bday
```
# post your bday
localhost:8000/addbday
heather-> Content-Type: application/json
body-> {
           "name": "meryl",
           "date": "22-06"
       }

# or with curl

curl -H 'Content-Type: application/json' \
      -d '{ "name":"meryl","date":"22-06"}' \
      -X POST \
      localhost:8000/addbday

# Check the posted bday is saved
localhost:8000/getbdays
```

One last get RestAPI
```
# get the bday and days until the next bday for a saved user
localhost:8000/getuserbday/Bob
```