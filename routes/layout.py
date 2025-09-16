from flask import Blueprint, request

layout_bp = Blueprint('layout', __name__)

def density(device):
  return round(float(device['consumption']) / device['size'], 2)

def can_fit(device, rack):
  return rack['space_left'] >= device['size'] and rack['power_left'] >= device['consumption']

def add_to_rack(device, rack):
  rack['space_left'] -= device['size']
  rack['power_left'] -= device['consumption']
  rack['devices'].append(device['id'])

def utilization(rack):
  return round(((rack['max_consumption'] - rack['power_left']) * 100.0) / rack['max_consumption'], 2)

def naive_layout(racks, devices):
  racks = racks
  for rack in racks:
    rack['space_left'] = rack['size']
    rack['power_left'] = rack['max_consumption']
    rack['devices'] = []

  devices = devices
  for device in devices:
    device['density'] = density(device)

  racks   = sorted(racks,   key = lambda x: ( x['size'],  x['max_consumption']))
  devices = sorted(devices, key = lambda x: (-x['size'], -x['density']))

  for device in devices:
    rack = next((r for r in racks if can_fit(device, r)), None)
    if rack == None:
      return None
    else:
      add_to_rack(device, rack)

  print(racks)

  layout = {}
  for rack in racks:
    layout[rack['id']] = {
      'devices': rack['devices'],
      'utilization': utilization(rack),
    }

  return layout

@layout_bp.route('/layout', methods=['GET'])
def get_layout():
  data = request.get_json()

  if not 'racks' in data:
    return { 'msg': 'No racks' }, 400
  if not 'devices' in data:
    return { 'msg': 'No devices' }, 400
  # TODO: check if data[racks|devices] is at least [{id: str, size: int, consumption|max_consumption: float}]

  layout = naive_layout(data['racks'], data['devices'])
  if layout == None:
    return { 'layout': None, 'msg': "Couldn't calculate a layout that would fit all of the devices" }

  return { 'layout': layout }
