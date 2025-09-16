# API

base_url: 0.0.0.0:3193


# DEVICES

## Overview 

GET    /devices
GET    /devices/{id}
POST   /devices
PUT    /devices/{id}
DELETE /devices/{id}
PUT    /devices/{id}/remove_from_rack
PUT    /devices/{id}/add_to_rack/{rack_id}


# GET    /devices
Retrieves a list of devices

return value 200: 
  [
    {
      id: str, 
      name: str,
      description: str,
      size: int,
      consumption: float,
      rack: str|null,
    }
  ]

# GET    /devices/{id}
Retrieves a device with {id}

return value 200: 
  {
    id: str, 
    name: str,
    description: str,
    size: int,
    consumption: float,
    rack: str|null,
  }
return value 404: { 'msg': 'Device not found' }

# POST   /devices
Creates a new device

data:
  {
    id: str, 
    name: str,
    description: str,
    size: int,
    consumption: float,
  }

return value 200: {}
return value 400: { 'msg': Error message }
  error messages:
    "Missing required field"
    "Device with same ID already exists"
    "Bad parameters"

# PUT    /devices/{id}
Makes changes to device with {id}

data:
  {
    name: str,
    description: str,
    size: int,
    consumption: float,
  }

return value 200: {}
return value 404: { 'msg': 'Device not found' }
return value 400: { 'msg': Error message }
  error messages:
    "Updated device cannot be supported by the current rack"
    "Bad parameters"

# DELETE /devices/{id}
Deletes device with {id} if it exists

return value 200: {}

# PUT    /devices/{id}/remove_from_rack
Removes device with {id} from rack, if it was in the rack

return value 200: {}
return value 404: { 'msg': 'Device not found' }

# PUT    /devices/{id}/add_to_rack/{rack_id}
Adds device with {id} to the rack with {rack_id}, if possible

return value 200: {}
return value 404: { 'msg': 'Device not found' }
return value 400: { 'msg': Error message }
  error messages:
    "Not enough space left in the rack"
    "Not enough power left in the rack"


# RACKS

## Overview 

GET    /racks
GET    /racks/{id}
POST   /racks
PUT    /racks/{id}
DELETE /racks/{id}

# GET    /racks
Retrieves a list of devices

return value 200: 
[
  {
    id: str,
    name: str,
    description: str,
    size: int,
    max_consumption: float,
    
    devices: [device_id: str],
    free_space: int,    
    consumption: float, -- sum consumption of all devices on the rack
    utilisation: float, -- 0% -> 100% consumption
  }
]

# GET    /racks/{id}
Retrieves a rack with {id}

return value 200: 
{
  id: str,
  name: str,
  description: str,
  size: int,
  max_consumption: float,
  
  devices: [device_id: str],
  free_space: int,    
  consumption: float, -- sum consumption of all devices on the rack
  utilisation: float, -- 0% -> 100% consumption
}
return value 404: { 'msg': 'Rack not found' }

# POST   /racks
Creates a new rack

data:
  {
    id: str, 
    name: str,
    description: str,
    size: int,
    max_consumption: float,
  }

return value 200: {}
return value 400: { 'msg': Error message }
  error messages:
    "Missing required field"
    "Rack with same ID already exists"
    "Bad parameters"

# PUT    /racks/{id}
Makes changes to rack with {id}

data:
  {
    name: str,
    description: str,
    size: int,
    max_consumption: float,
  }

return value 200: {}
return value 404: { 'msg': 'Rack not found' }
return value 400: { 'msg': Error message }
  error messages:
    "Updated rack can't support current devices"
    "Bad parameters"

# DELETE /racks/{id}
Deletes rack with {id} if it exists

# LAYOUT

# GET /layout
Given a list of racks and devices, calculates the layout that optimizes rack utilization.

data:
  {
    racks: [
      {
        id: str,
        size: int,
        max_consumption: float,
      }
    ],
    devices: [
      {
        id: str,
        size: int,
        consumption: float,
      }
    ]
  }

return value 400: { 'msg': Error message } - badly formated data
return value 200:  
  { layout: null, msg: "Couldn't calculate a layout that would fit all of the devices" }
  { 
    layout: {
      rack_id: {
        devices: [device_id],
        utilization: float,
      }
    } 
  }
