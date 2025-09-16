import pytest
from helper import req, print_state

def test_no_racks():
  code, res = req('GET', '/layout', {})
  assert code == 400 and res == { 'msg': 'No racks' }

def test_no_devices():
  data = {
    'racks': [
      { 'id': '0', 'size': 10, 'max_consumption': 110 }
    ],
  }

  code, res = req('GET', '/layout', data)
  assert code == 400 and res == { 'msg': 'No devices' }

def test_layout_1():
  data = {
    'racks': [
      { 'id': '0', 'size': 10, 'max_consumption': 110 },
      { 'id': '1', 'size': 20, 'max_consumption': 320 },
    ],
    'devices': [
      { 'id': '0', 'size': 2, 'consumption': 12 },
      { 'id': '1', 'size': 3, 'consumption': 18 },
      { 'id': '2', 'size': 4, 'consumption': 60 },
    ],
  }

  code, res = req('GET', '/layout', data)

  exp_res = { 
    'layout': {
      '0': {
        'devices': ['2', '1', '0'], 
        'utilization': 81.82,
      }, 
      '1': {
        'devices': [], 
        'utilization': 0.0,
      }
    }
  }

  assert code == 200 and res == exp_res

def test_layout_cannot_fit_size():
  data = {
    'racks': [
      { 'id': '0', 'size': 4, 'max_consumption': 110 },
      { 'id': '1', 'size': 4, 'max_consumption': 320 },
    ],
    'devices': [
      { 'id': '0', 'size': 2, 'consumption': 1 },
      { 'id': '1', 'size': 3, 'consumption': 1 },
      { 'id': '2', 'size': 2, 'consumption': 1 },
      { 'id': '3', 'size': 2, 'consumption': 1 },
      { 'id': '4', 'size': 4, 'consumption': 1 },
    ],
  }

  code, res = req('GET', '/layout', data)

  exp_res = { 'layout': None, 'msg': "Couldn't calculate a layout that would fit all of the devices" }
  assert code == 200 and res == exp_res

def test_layout_cannot_fit_power():
  data = {
    'racks': [
      { 'id': '0', 'size': 200, 'max_consumption': 4 },
      { 'id': '1', 'size': 200, 'max_consumption': 4 },
    ],
    'devices': [
      { 'id': '0', 'size': 1, 'consumption': 2 },
      { 'id': '1', 'size': 1, 'consumption': 3 },
      { 'id': '2', 'size': 1, 'consumption': 2 },
      { 'id': '3', 'size': 1, 'consumption': 2 },
      { 'id': '4', 'size': 1, 'consumption': 4 },
    ],
  }

  code, res = req('GET', '/layout', data)

  exp_res = { 'layout': None, 'msg': "Couldn't calculate a layout that would fit all of the devices" }
  assert code == 200 and res == exp_res
