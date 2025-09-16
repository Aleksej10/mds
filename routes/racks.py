from flask import Blueprint, request
from peewee import DoesNotExist
import models

racks_bp = Blueprint('racks', __name__)

@racks_bp.route('/state', methods=['GET'])
def state():
  racks   = list(map(lambda x: x.serialize(), models.Rack.select()))
  devices = list(map(lambda x: x.serialize(), models.Device.select()))
  return { "racks": racks, "devices": devices }

@racks_bp.route('/racks', methods=['GET'])
def get_racks():
  return list(map(lambda x: x.serialize(), models.Rack.select()))

@racks_bp.route('/racks/<id>', methods=['GET'])
def get_racks_id(id: str):
  try:
    rack = models.Rack[id]
  except DoesNotExist:
    return { 'msg': 'Rack not found' }, 404

  return rack.serialize()

@racks_bp.route('/racks', methods=['POST'])
def post_racks():
  ok, msg = models.Rack.create_from_data(request.get_json())
  if ok:
    return {}, 200
  else:
    return { 'msg': msg }, 400

@racks_bp.route('/racks/<id>', methods=['PUT'])
def put_racks_id(id):
  try:
    rack = models.Rack[id]
  except DoesNotExist:
    return { 'msg': 'Rack not found' }, 404

  ok, msg = rack.update_data(request.get_json())
  if ok:
    return {}, 200
  else:
    return { 'msg': msg }, 400

@racks_bp.route('/racks/<id>', methods=['DELETE'])
def delete_racks_id(id):
  try:
    rack = models.Rack[id]
  except DoesNotExist:
    return {}

  for device in rack.devices():
    device.rack = None
    device.save()

  rack.delete_instance()
  return {}
