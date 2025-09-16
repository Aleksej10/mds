from flask import Blueprint, request
from peewee import DoesNotExist
import models

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/devices', methods=['GET'])
def get_devices():
  return list(map(lambda x: x.serialize(), models.Device.select()))

@devices_bp.route('/devices/<id>', methods=['GET'])
def get_devices_id(id: str):
  try:
    device = models.Device[id]
  except DoesNotExist:
    return { 'msg': 'Device not found' }, 404

  return device.serialize()

@devices_bp.route('/devices', methods=['POST'])
def post_devices():
  ok, msg = models.Device.create_from_data(request.get_json())
  if ok:
    return {}, 200
  else:
    return { 'msg': msg }, 400

@devices_bp.route('/devices/<id>', methods=['PUT'])
def put_devices_id(id):
  try:
    device = models.Device[id]
  except DoesNotExist:
    return { 'msg': 'Device not found' }, 404

  ok, msg = device.update_data(request.get_json())
  if ok:
    return {}, 200
  else:
    return { 'msg': msg }, 400

@devices_bp.route('/devices/<id>', methods=['DELETE'])
def delete_devices_id(id):
  models.Device.delete().where(models.Device.id == id).execute()
  return {}

@devices_bp.route('/devices/<id>/remove_from_rack', methods=['PUT'])
def put_devices_id_remove_from_rack(id):
  try:
    device = models.Device[id]
  except DoesNotExist:
    return { 'msg': 'Device not found' }, 404

  device.remove_from_rack()

  return {}, 200

@devices_bp.route('/devices/<id>/add_to_rack/<rack_id>', methods=['PUT'])
def put_devices_id_add_to_rack(id, rack_id):
  try:
    device = models.Device[id]
  except DoesNotExist:
    return { 'msg': 'Device not found' }, 404

  try:
    rack = models.Rack[rack_id]
  except DoesNotExist:
    return { 'msg': 'Rack not found' }, 400

  ok, msg = device.add_to_rack(rack)
  if ok:
    return {}, 200
  else:
    return { 'msg': msg }, 400
