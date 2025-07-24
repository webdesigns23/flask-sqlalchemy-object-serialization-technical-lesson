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

# serialize object to dictionary with schema.dump()
dog_dict = dog_schema.dump(dog)
pprint(dog_dict)

# serialize object to JSON-encoded string with schema.dumps()
dog_json = dog_schema.dumps(dog)
pprint(dog_json)

# specify which fields to output with the only parameter, passed as a tuple.
dog_summary = DogSchema(only=("name", "breed")).dumps(dog)
pprint(dog_summary)

# omit fields by passing the exclude parameter (note the comma in the single-value tuple).
dog_summary = DogSchema(exclude=("tail_wagging", )).dumps(dog)
pprint(dog_summary)



### serialize a collection with many=True
dogs = [Dog(name="Snuggles", breed="Beagle", tail_wagging=True),
        Dog(name="Wags", breed = "Collie", tail_wagging=False)]
dictionary_list = DogSchema(many=True).dump(dogs)   # dump returns list of dictionaries
pprint(dictionary_list)

json_array = DogSchema(many=True).dumps(dogs)       # dumps returns JSON-encoded array
pprint(json_array)   # NOTE: String is enclosed in parenthesis to print across multiple lines
