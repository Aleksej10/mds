from peewee import (
  Model,
  SqliteDatabase,
  CharField,
  TextField,
  IntegerField,
  FloatField,
  ForeignKeyField,
  IntegrityError,
)

database = 'app.db'

db = SqliteDatabase(database)

class BaseModel(Model):
  class Meta:
    database = db

class Rack(BaseModel):
  id = CharField(primary_key=True)
  name = CharField()
  description = TextField(null=True)
  size: int = IntegerField() # type: ignore
  max_consumption: float = FloatField() # type: ignore

  def devices(self):
    return Device.select().where(Device.rack == self)

  def used_space(self):
    sizes = map(lambda x: x.size, self.devices())
    return sum(sizes)

  def consumption(self):
    consumptions = map(lambda x: x.consumption, self.devices())
    return sum(consumptions)

  def serialize(self):
    data = {}

    data['id']              = self.id
    data['name']            = self.name
    data['description']     = self.description
    data['size']            = self.size
    data['max_consumption'] = self.max_consumption

    consumption = self.consumption()
    utilisation = (consumption * 100.0) / self.max_consumption

    data['devices']     = list(map(lambda x: x.id, self.devices()))
    data['free_space']  = self.size - self.used_space()
    data['consumption'] = consumption
    data['utilisation'] = round(utilisation, 2)

    return data

  @staticmethod
  def create_from_data(data = {}):
    if not 'id' in data:
      return  False, "Missing required field: id"

    try:
      Rack.create(
        id              = data['id'],
        name            = data['name'],
        description     = data['description'],
        size            = data['size'],
        max_consumption = data['max_consumption'],
      )
      return True, None
    except IntegrityError:
      return False, "Rack with same ID already exists"
    except KeyError as e:
      return False, f"Missing required field: {e.args[0]}"
    except Exception:
      return False, "Bad parameters, probably"

  def update_data(self, data = {}):
    fields = ['name', 'description', 'size', 'max_consumption']

    try:
      for field in fields:
        if field in data:
          setattr(self, field, data[field])
    except:
      return False, "Bad parameters, probably"

    if not self.is_withing_limits():
      return False, "Updated rack can't support current devices"

    self.save()
    return True, None

  def is_withing_limits(self):
    return (self.size >= self.used_space()) and (self.max_consumption >= self.consumption())

class Device(BaseModel):
  id = CharField(primary_key=True)
  name = CharField()
  description = TextField(null=True)
  size = IntegerField()
  consumption = FloatField()
  rack = ForeignKeyField(Rack, null=True)

  def serialize(self):
    data = {}

    data['id']          = self.id
    data['name']        = self.name
    data['description'] = self.description
    data['size']        = self.size
    data['consumption'] = self.consumption
    data['rack']        = self.rack.id if self.rack else None

    return data

  def remove_from_rack(self):
    self.rack = None
    self.save()

  def add_to_rack(self, rack):
    if rack.used_space() + self.size > rack.size:
      return False, "Not enough space left in the rack"

    if rack.consumption() + self.consumption > rack.max_consumption:
      return False, "Not enough power left in the rack"

    self.rack = rack
    self.save()
    return True, None

  @staticmethod
  def create_from_data(data = {}):
    if not 'id' in data:
      return  False, "Missing required field: id"

    try:
      Device.create(
        id          = data['id'],
        name        = data['name'],
        description = data['description'],
        size        = data['size'],
        consumption = data['consumption'],
      )
      return True, None
    except IntegrityError:
      return False, "Device with same ID already exists"
    except KeyError as e:
      return False, f"Missing required field: {e.args[0]}"
    except Exception:
      return False, "Bad parameters, probably"

  def update_data(self, data = {}):
    fields = ['name', 'description', 'size', 'consumption']

    try:
      for field in fields:
        if field in data:
          setattr(self, field, data[field])
    except:
      return False, "Bad parameters, probably"

    db.begin()
    self.save()
    res = True, None

    if self.rack != None and not self.rack.is_withing_limits():
      db.rollback()
      res = False, 'Updated device cannot be supported by the current rack'

    db.commit()
    return res

db.connect()
db.create_tables([Rack, Device])
