import pytest
from helper import req, print_state

device_id = '01AB'
rack_id   = 'WWK8'

@pytest.fixture(scope="module", autouse=True)
def setup_and_cleanup():
  req('POST', '/devices', {
    'id': device_id,
    'name': 'Switch',
    'description': 'a switch.',
    'size': 4,
    'consumption': 60,
  })

  req('POST', '/racks', {
    'id': rack_id,
    'name': 'Rack',
    'description': 'a rack.',
    'size': 20,
    'max_consumption': 300,
  })

  req('PUT', f"/devices/{device_id}/add_to_rack/{rack_id}")

  yield

  req('DELETE', f"/devices/{device_id}")
  req('DELETE', f"/racks/{rack_id}")

def test_device_update_invalid_size():
  code, res = req('PUT', f"/devices/{device_id}", { 'size': 22 })
  assert (code == 400 and res == { 'msg': 'Updated device cannot be supported by the current rack' })

def test_device_update_invalid_consumption():
  code, res = req('PUT', f"/devices/{device_id}", { 'consumption': 320 })
  assert (code == 400 and res == { 'msg': 'Updated device cannot be supported by the current rack' })

def test_device_update():
  code, res = req('PUT', f"/devices/{device_id}", { 'size': 18, 'consumption': 280 })
  assert (code == 200 and res == {})

def test_rack_update_invalid_size():
  code, res = req('PUT', f"/racks/{rack_id}", { 'size': 10 })
  assert (code == 400 and res == {  'msg': "Updated rack can't support current devices" })

def test_rack_update_invalid_consumption():
  code, res = req('PUT', f"/racks/{rack_id}", { 'max_consumption': 100 })
  assert (code == 400 and res == {  'msg': "Updated rack can't support current devices" })

def test_rack_update():
  code, res = req('PUT', f"/racks/{rack_id}", { 'size': 20, 'max_consumption': 290 })
  assert (code == 200 and res == {})
