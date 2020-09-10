# Pandora
Pandora is a mysterious planet. Those types of planets can support human life, for that reason the president of the Handsome Jack decides to send some people to colonise this new planet and
reduce the number of people in their own country.
 
After 10 years, the new president wants to know how the new colony is growing, and wants some information about his citizens. 
Hence he hired you to build a rest API to provide the desired information.

The government from Pandora will provide you two json files (located at resource folder) which will provide information 
about all the citizens in Pandora (name, age, friends list, fruits and vegetables they like to eat...) and all founded companies on that planet.
Unfortunately, the systems are not that evolved yet, thus you need to clean and organise the data before use.
For example, instead of providing a list of fruits and vegetables their citizens like, they are providing a list of favourite food, 
and you will need to split that list (please, check below the options for fruits and vegetables).

## API requisites and dependencies

The Pandora API is written in [Python3.7](https://www.python.org/downloads/release/python-370/) and uses [MySQL 5.7](https://dev.mysql.com/downloads/mysql/5.7.html) database.

It is build on top of [Falcon web-framework](https://falcon.readthedocs.io/en/stable/index.html) with [Gunicorn](https://gunicorn.org/) and 
also uses:
 
* [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/) to manage the virtualenv + install packages
* [SQLAlchemy](https://www.sqlalchemy.org/) to communicate with the DB 
* [Alembic](https://alembic.sqlalchemy.org/en/latest/) to handle the migrations.
* [Pytest](https://docs.pytest.org/en/stable/) to execute unit tests


# How to install

To install the application is just a matter of running one command, by first you need to make sure
all the installation dependencies are resolved.

## Dependencies

The Application and its dependencies are fully containerized and rely on Docker and Docker-compose to manage 
the containers and uses of Make as our build automation tool.

So, if you don't have them installed already, please follow the links below:

* [Docker](https://www.docker.com/) - Instructions to [install](https://docs.docker.com/get-docker/)

* [Docker Compose] - Instruction to [install](https://docs.docker.com/compose/install/)

* [Make](https://en.wikipedia.org/wiki/Make_%28software%29)


## Installation

Once the dependencies are installed, just follow the simple steps below to have the API up and running.

Clone the repo and change the directory to the newly cloned folder.

```bash
git clone https://github.com/lmagalhaes/pandora.git
cd pandora
```

Use the command `make install` to trigger the installation.

```
make install 
```

The `make install` command build images, configure dependencies and install the application.

When the command is finished you can access the API by accessing [127.0.0.1:8020](http://120.0.0.1:8020) in your browser.

The message `Welcome to Pandora Api` should show up, meaning the applications is working.

*Obs:* You can simply run `make` or `make help` for a list of all available commands.
 

# API endpoints

The API provide 4 endpoints:


### Welcome endpoit
This is just a simple welcome message and can be used as health check, to make sure the API is running.

**URI:**: `GET /`

**Response:** Welcome message

**Status code**: 200 


### Company Endpoint
Given a company id, returns the company details (id and name) and a list of its employees. 

**URI**: `GET /company/{company_id:int}`

**Status code**: 200

**Response**:
```json
{
  "id": 1,
  "name": "NETBOOK",
  "employees": [{
    "id": 290,
    "name": "Frost Foley",
    "has_died": true,
    "eye_color": "blue",
    "email": "frostfoley@earthmark.com",
    "age": 22,
    "phone": "+1 (987) 436-3916",
    "address": "824 Clark Street, Utting, New Mexico, 3994",
    "tags": ["consectetur", "cillum", "ea", "do", "sunt", "aliqua", "incididunt"]
  }]
}
```

If the given id does not belong to any company:
**Status code**: `404`
**Response** Company with id (0) not found
 

### Person Endpoint
Given a person id, returns the person details (username, age and his/her preferred fruits and vegetables)

**URI** `GET /person/{person_id:int}`

**Status code:**: 200

**Response**: 
```json
{
  "usename": "Rosemary Hayes",
  "age": 30,
  "fruits": ["orange", "apple"],
  "vegetables": ["celery", "carrot"]
}
```
If the given id does not belong to any person:

**Status code**: `404`

**Response** Person with id (0) not found


### Person Common Friends With Another Person
Given a person id and another person id, returns the details for each person and a detailed list of all their common friends,
that matches the following criteria: `eye_color == 'bronw'` and `has_died == false`

If they have no common friends or friends do match the above criteria the commons_friends will be an empty list. 

**URI** `GET /person/{person_id:int}/common-friends/{another_person_id:int}`

**Status code:**: 200

**Response**:
 
```json
{
	"person1": {
		"id": 1,
		"name": "Carmella Lambert",
		"has_died": true,
		"eye_color": "blue",
		"email": "carmellalambert@earthmark.com",
		"age": 61,
		"phone": "+1 (910) 567-3630",
		"address": "628 Sumner Place, Sperryville, American Samoa, 9819",
		"tags": ["id", "quis", "ullamco", "consequat", "laborum", "sint", "velit"]
	},
	"person2": {
		"id": 4,
  		"name": "Rosemary Hayes",
		"has_died": true,
		"eye_color": "blue",
		"email": "rosemaryhayes@earthmark.com",
		"age": 30,
		"phone": "+1 (984) 437-3226",
		"address": "130 Bay Parkway, Marshall, Virgin Islands, 298",
		"tags": ["officia", "voluptate", "aute", "consequat", "aliqua", "do", "magna"]
	},
	"commons_friends": []
}
```
If any othe the given ids does not belong to any person:

**Status code**: `404`

**Response** Person with id (0) not found
