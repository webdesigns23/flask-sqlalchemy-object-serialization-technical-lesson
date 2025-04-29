# Technical Lesson: Serialization with Marshmallow

## Introduction

In this lesson, we'll learn how to use `marshmallow` to serialize a Python
object. While there are different formats for data serialization, we will
primarily serialize a Python object to either a dictionary or a JSON-encoded
string.

## Scenario

You recently joined a startup that manages a pet adoption platform. Your team 
needs a fast, reliable way to send dog profiles to users on the web and mobile 
apps. Python objects like Dog instances can't be directly transmitted or 
stored — they must first be serialized into a format like JSON. Your task is 
to define a clean, consistent serialization process using the marshmallow 
library, ensuring that different applications (frontend, mobile, API clients) 
can receive well-structured data from the backend.

Goal: Learn to use marshmallow schemas to serialize Python object instances 
into JSON or dictionaries, so data can be shared across services.

## Tools & Resources

- [GitHub Repo](https://github.com/learn-co-curriculum/flask-sqlalchemy-object-serialization-technical-lesson)
- [marshmallow](https://pypi.org/project/marshmallow/)
- [marshmallow quickstart](https://marshmallow.readthedocs.io/en/stable/quickstart.html)
- [pprint module](https://docs.python.org/3/library/pprint.html#module-pprint)

## Setup

This lesson is a code-along, so fork and clone the repo.

Run `pipenv install` to install the dependencies and `pipenv shell` to enter
your virtual environment before running your code.

```console
$ pipenv install
$ pipenv shell
```

## Instructions

### Task 1: Define the Problem

While working with backend systems, you'll often deal with Python objects that 
need to be:

* Serialized: Converted into dictionaries or JSON strings to send over HTTP responses, save to files, or share across systems.
* Deserialized (covered in the next lesson): Rebuilt from JSON or dictionaries into Python objects.

Problem:

Native Python objects, like instances of classes, cannot be directly shared through 
APIs or external systems without serialization. Without a structured serialization 
process, inconsistencies arise between different parts of the system, leading 
to bugs, security risks, or broken integrations.

Solution:

Use a schema-based serialization library like marshmallow to define 
consistent, reusable rules for converting objects into portable data formats.

### Task 2: Determine the Design

To solve the problem systematically, we'll follow a structured design:

1. Model Definition:
    * Define simple Python classes representing real-world concepts (e.g., Dog).
2. Schema Definition:
    * Create a Schema class (e.g., DogSchema) using marshmallow that maps the model's attributes to serializable fields.
3. Serialization Logic:
    * Use the dump() and dumps() methods to convert objects to:
        * Dictionaries (for internal Python use or database writes).
        * JSON-encoded strings (for HTTP responses and API communication).
4. Optional Enhancements:
    * Selective field output with only and exclude parameters.
    * Collections serialization (many=True) for lists of objects.
    * Preprocessing and Postprocessing:
        * Modify object data dynamically before serialization using @pre_dump.
        * (Optional later: modify after with @post_dump.)
5. Verification:
    * Print and inspect serialized outputs.
    * Ensure objects serialize consistently, accurately, and safely.

### Task 3: Develop, Test, and Refine the Code

#### Step 1: Define Schema

Within the `lib` directory, you'll find the file `serialize.py` that defines a
simple `Dog` class . We will refer to a class that defines the structure of an
object that we wish to serialize as a **model**. Notice we have a new import
`pprint`, which provides support to recursively pretty-print lists, tuples, and
dictionaries.

```py
# lib/serialize.py

from pprint import pprint

# model

class Dog:
    def __init__(self, name, breed, tail_wagging = False):
        self.name = name
        self.breed = breed
        self.tail_wagging = tail_wagging

# create model instance

dog = Dog(name="Snuggles", breed="Beagle", tail_wagging=True)
print(dog)
```

If you run the code, you'll see output that indicates something about the
object's memory location:

```console
$ python lib/serialize.py
<__main__.Dog object at 0x100826810>
```

To print the state of the `Dog` object in a format that is easy to read, we will
define a `marshmallow` schema named `DogSchema` and then use an instance of that
schema to serialize the object.

Edit the code as shown below to define the `DogSchema` class and create an
instance of the class. You will also need to add a new import statement.

```py
# lib/serialize.py

from pprint import pprint
from marshmallow import Schema, fields

# model

class Dog:
    def __init__(self, name, breed, tail_wagging = False):
        self.name = name
        self.breed = breed
        self.tail_wagging = tail_wagging

    def give_treat(self):
        self.tail_wagging = True

    def scold(self):
        self.tail_wagging = False

# schema

class DogSchema(Schema):
    name = fields.String()
    breed = fields.String()
    tail_wagging = fields.Boolean()

# create model and schema instances

dog = Dog(name="Snuggles", breed="Beagle", tail_wagging=True)
dog_schema = DogSchema()
```

- `Schema` and `fields` are imported from the `marshmallow` library.
- `DogSchema` defines the same 3 fields as the `Dog` model class. Each field is
  assigned a marshmallow type.

The `DogSchema` instance can be used to serialize the state of the `Dog`
instance. We'll do that using two inherited methods for dumping object state:

- `dump()` serializes an object to a dictionary
- `dumps()` serializes an object to a JSON-encoded string

Models represent what the object is; schemas define how the object should be serialized.

#### Step 2: Serializing/dumping to a dictionary using `dump()`

Let's first serialize the `Dog` instance to a dictionary using the `dump()`
method and pretty-print the result. Add the following to the code:

```py
# serialize object to dictionary with schema.dump()

dog_dict = dog_schema.dump(dog)
pprint(dog_dict)
# => {'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True}
```

Run the code to see the dog's fields printed as a dictionary with the fields as
keys:

```console
$ python lib/serialize.py
{'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True}
```

#### Step 3: Serializing/dumping to JSON using `dumps()`

We can also serialize to a JSON-encoded string using `dumps()`. Update the code
to add the following:

```py
# serialize object to JSON-encoded string with schema.dumps()

dog_json = dog_schema.dumps(dog)
pprint(dog_json)
# => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
```

Run the code again and confirm an additional line of output containing a
JSON-encoded string for the fields and values. Notice the JSON data contains the
boolean value `true` instead of the Python value `True`.

```console
'{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
```

#### Step 4: Filtering

We can specify which fields to output by passing either an `only` or an
`exclude` parameter to the dump methods. Each parameter takes a tuple of strings
corresponding to field names. For example:

```py
# specify which fields to output with the only parameter, passed as a tuple.

dog_summary = DogSchema(only=("name", "breed")).dumps(dog)
pprint(dog_summary)
# => '{"name": "Snuggles", "breed": "Beagle"}'

# omit fields by passing the exclude parameter (note the comma in the single-value tuple).

dog_summary = DogSchema(exclude=("tail_wagging", )).dumps(dog)
pprint(dog_summary)
# => '{"name": "Snuggles", "breed": "Beagle"}'
```

#### Step 5: Serialize a collection

A collection can be serialized by instantiating the schema with the parameter
`many=True`. The `dump()` method returns a list of dictionaries, while the
`dumps()` method returns a string containing a JSON array literal.

Update the code to serialize a list of `Dog` instances as shown:

```py
# serialize a collection with many=True

dogs = [Dog(name="Snuggles", breed="Beagle", tail_wagging=True),
        Dog(name="Wags", breed = "Collie", tail_wagging=False)]
dictionary_list = DogSchema(many=True).dump(dogs)   # dump returns list of dictionaries
pprint(dictionary_list)
# => [{'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True},
# =>  {'breed': 'Collie', 'name': 'Wags', 'tail_wagging': False}]

json_array = DogSchema(many=True).dumps(dogs)       # dumps returns JSON-encoded array
pprint(json_array)   # NOTE: String is enclosed in parenthesis to print across multiple lines
# => ('[{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}, {"name": '
# =>  '"Wags", "breed": "Collie", "tail_wagging": false}]')
```

Without `many=True`, Marshmallow expects a single object. With `many=True`, it knows to treat the input as a collection.

#### Step 6: Pre-dump processing

The marshmallow library provides decorators for registering schema
pre-processing and post-processing methods. We define a method to execute prior
to serialization using the `@pre_dump` decorator and after serialization using
`@post_dump`.

Consider the code in `lib/pre_dump.py`, which defines an `Album` model and
corresponding schema named `AlbumSchema`. We can easily create and serialize
model instances as shown:

```py
from pprint import pprint
from marshmallow import Schema, fields, pre_dump

# model

class Album():
    def __init__(self, title, artist, num_sold):
        self.title = title
        self.artist = artist
        self.num_sold = num_sold

# schema

class AlbumSchema(Schema):
    title = fields.String(required=True)
    artist = fields.String(required=True)
    num_sold = fields.Int(required=True)

# create model and schema instances
album_1 = Album("The Wall", "Pink Floyd", 19000000)
album_2 = Album("Renaissance", "Beyonce", 332000)
schema = AlbumSchema()

# deserialize model instances

pprint(schema.dumps(album_1))
# => '{"title": "The Wall", "artist": "Pink Floyd", "num_sold": 19000000}'

pprint(schema.dumps(album_2))
# => '{"title": "Renaissance", "artist": "Beyonce", "num_sold": 332000}'
```

Let's suppose we would like to include in the serialized output a boolean named
`big_hit` that indicates if the album sold more than a million copies. We'll add
a field named `big_hit` to the schema, along with a method decorated with
`@pre_dump()` that assigns a value based on the `num_sold` field. The method
receives the object to be serialized and returns the processed object.

```py
class AlbumSchema(Schema):
    title = fields.String(required=True)
    artist = fields.String(required=True)
    num_sold = fields.Int(required=True)
    big_hit = fields.Boolean(dump_only = True)

    # compute field prior to serialization
    @pre_dump()
    def get_data(self, data, **kwargs):
        data.big_hit = data.num_sold > 1000000
        return data
```

Computed fields like `big_hit` allow you to add dynamic metadata at serialization 
time, without modifying your original Python model.

Run the code again to confirm the `big_hit` field is included in the serialized
result. Recall that Python may print a long string across multiple lines by
enclosing it in parentheses.

```console
$ python lib/pre_dump.py
('{"title": "The Wall", "artist": "Pink Floyd", "num_sold": 19000000, '
 '"big_hit": true}')
('{"title": "Renaissance", "artist": "Beyonce", "num_sold": 332000, "big_hit": '
 'false}')
```

Let's update the comments to reflect the new output:

```py
# deserialize model instances

pprint(schema.dumps(album_1))
# => '{"title": "The Wall", "artist": "Pink Floyd", "num_sold": 19000000, "big_hit": true}'

pprint(schema.dumps(album_2))
# => '{"title": "Renaissance", "artist": "Beyonce", "num_sold": 332000, "big_hit": 'false}'
```

#### Step 7: Verify your Code

Solution Code: 

```py
# lib/serialize.py

from pprint import pprint
from marshmallow import Schema, fields

# model

class Dog:
    def __init__(self, name, breed, tail_wagging = False):
        self.name = name
        self.breed = breed
        self.tail_wagging = tail_wagging

    def give_treat(self):
        self.tail_wagging = True

    def scold(self):
        self.tail_wagging = False

# schema

class DogSchema(Schema):
    name = fields.String()
    breed = fields.String()
    tail_wagging = fields.Boolean()

# create schema and model instances

dog_schema = DogSchema()
dog = Dog(name="Snuggles", breed="Beagle", tail_wagging=True)

# serialize object to dictionary with schema.dump()

dog_dict = dog_schema.dump(dog)
pprint(dog_dict)
# => {'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True}

# serialize object to JSON-encoded string with schema.dumps()

dog_json = dog_schema.dumps(dog)
pprint(dog_json)
# => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'

# specify which fields to output with the only parameter, passed as a tuple.

dog_summary = DogSchema(only=("name", "breed")).dumps(dog)
pprint(dog_summary)
# => '{"name": "Snuggles", "breed": "Beagle"}'

# omit fields by passing the exclude parameter. Note the comma in the tuple.

dog_summary = DogSchema(exclude=("tail_wagging", )).dumps(dog)
pprint(dog_summary)
# => '{"name": "Snuggles", "breed": "Beagle"}'

# serialize a collection with many=True

dogs = [Dog(name="Snuggles", breed="Beagle", tail_wagging=True),
        Dog(name="Wags", breed = "Collie", tail_wagging=False)]
dictionary_list = DogSchema(many=True).dump(dogs)   # dump returns list of dictionaries
pprint(dictionary_list)
# => [{'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True},
# =>  {'breed': 'Collie', 'name': 'Wags', 'tail_wagging': False}]

json_array = DogSchema(many=True).dumps(dogs)       # dumps returns JSON-encoded list
pprint(json_array)   # NOTE: String is enclosed in parenthesis to print across multiple lines
# => ('[{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}, {"name": '
# =>  '"Wags", "breed": "Collie", "tail_wagging": false}]')
```

```py
# lib/pre_dump.py

from pprint import pprint
from marshmallow import Schema, fields, pre_dump

# model

class Album():
    def __init__(self, title, artist, num_sold):
        self.title = title
        self.artist = artist
        self.num_sold = num_sold

# schema

class AlbumSchema(Schema):
    title = fields.String()
    artist = fields.String()
    num_sold = fields.Int()
    big_hit = fields.Boolean()

    # compute field prior to serialization
    @pre_dump()
    def get_data(self, data, **kwargs):
        data.big_hit = data.num_sold > 1000000
        return data

# create model and schema instances
album_1 = Album("The Wall", "Pink Floyd", 19000000)
album_2 = Album("Renaissance", "Beyonce", 332000)
schema = AlbumSchema()

# deserialize model instances

pprint(schema.dumps(album_1))
# => '{"title": "The Wall", "artist": "Pink Floyd", "num_sold": 19000000, "big_hit": true}'

pprint(schema.dumps(album_2))
# => '{"title": "Renaissance", "artist": "Beyonce", "num_sold": 332000, "big_hit": 'false}'
```

#### Step 8: Commit and Push Git History

Commit and push your final code to GitHub.

```bash
git add .
git commit -m "final solution"
git push
```

If you used a feature branch, remember to open a PR and merge to main.

### Task 4: Document and Maintain

Best Practice documentation steps:
* Add comments to the code to explain purpose and logic, clarifying intent and functionality of your code to other developers.
* Update README text to reflect the functionality of the application following https://makeareadme.com. 
  * Add screenshot of completed work included in Markdown in README.
* Delete any stale branches on GitHub
* Remove unnecessary/commented out code
* If needed, update git ignore to remove sensitive data

## Considerations

When building a serialization layer for real-world systems, keep in mind:

### Data Privacy
Only expose fields that are safe to share externally. Sensitive data (like passwords or internal IDs) should be excluded explicitly.

### Consistency
Define your schemas carefully so all outputs conform to a predictable structure, minimizing downstream integration issues.

### Error Handling
Marshmallow can validate fields automatically, but it’s good practice to define rules like required=True on important fields to avoid silent failures.

### Performance
Serialization and deserialization add some overhead. When working with large collections, prefer efficient operations (many=True) and filter out unnecessary fields.

### Versioning
Over time, serialized formats evolve. Plan for future compatibility by being cautious about removing or changing fields in your schemas.

### Extensibility
As your models grow in complexity, Marshmallow supports nested schemas, validation, transformations, and more — but start simple!