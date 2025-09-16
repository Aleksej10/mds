import pytest
from helper import req, print_state

device_id = '01AB'
rack_id   = 'WWK8'

@pytest.fixture(scope="module", autouse=True)
def setup_and_cleanup():
  yield

  req('DELETE', f"/devices/{device_id}")
  req('DELETE', f"/racks/{rack_id}")

def test_get_devices_empty():
  code, res = req('GET', '/devices')
  assert code == 200 and res == []

def test_get_device_404():
  code, _ = req('GET', '/devices/BAD_ID')
  assert code == 404


def test_create_device():
  code, _ = req('POST', '/devices', {
    'id': device_id,
    'name': 'Switch',
    'description': 'a switch.',
    'size': 4,
    'consumption': 60,
  })

  assert code == 200

def test_create_device_missing_field():
  code, res = req('POST', '/devices', {
    'id': 'something',
  })

  assert code == 400 and res == { 'msg': 'Missing required field: name' }

def test_create_device_same_id():
  code, res = req('POST', '/devices', {
    'id': device_id,
    'name': 'Switch',
    'description': 'a switch.',
    'size': 4,
    'consumption': 60,
  })

  assert code == 400 and res == { 'msg': 'Device with same ID already exists' }

def test_create_rack():
  code, _ = req('POST', '/racks', {
    'id': rack_id,
    'name': 'Rack',
    'description': 'a rack.',
    'size': 20,
    'max_consumption': 300,
  })

  assert code == 200

def test_add_device_to_rack():
  code, _ = req('PUT', f"/devices/{device_id}/add_to_rack/{rack_id}")

  assert code == 200

def test_get_racks():
  code, res = req('GET', '/racks')

  exp_res = [
    {
      'consumption': 60.0,
      'description': 'a rack.', 
      'devices': [device_id], 
      'free_space': 16, 
      'id': rack_id, 
      'max_consumption': 300.0, 
      'name': 'Rack', 
      'size': 20, 
      'utilisation': 20.0,
    }
  ]

  assert code == 200 and res == exp_res

  code, res = req('GET', f"/devices/{device_id}")
  assert code == 200 and res['rack'] == rack_id

def test_remove_device_from_rack():
  code, _ = req('PUT', f"/devices/{device_id}/remove_from_rack")
  assert code == 200

  code, res = req('GET', f"/devices/{device_id}")
  assert code == 200 and res['rack'] == None
