import base64
import binascii
import os

class BCObjectFlatteners(object):

	@staticmethod
	def flatten_beacon(beacon):
		flat_beacon = dict()
		
		flat_beacon["id"] = beacon["id"].upper()

		serial_number = beacon.get("serialNumber", None)
		flat_beacon["serial_number"] = serial_number.upper() if serial_number else None
		
		eddystone = beacon.get("eddystone", None)
		
		eddystone_namespace_id = eddystone.get("namespaceID", None) if eddystone else None
		flat_beacon["eddystone_namespace_id"] = eddystone_namespace_id.upper() if eddystone_namespace_id else None
		
		eddystone_instance_id = eddystone.get("instanceID", None) if eddystone else None
		flat_beacon["eddystone_instance_id"] = eddystone_instance_id.upper() if eddystone_instance_id else None
		
		flat_beacon["eddystone_url"] = eddystone.get("url", None) if eddystone else None
		
		eddystone_uid = eddystone.get("uid", None) if eddystone else None
		flat_beacon["eddystone_uid"] = eddystone_uid.upper() if eddystone_uid else None
		flat_beacon["eddystone_uid64"] = base64.b64encode(binascii.unhexlify(flat_beacon["eddystone_uid"])) if eddystone_uid else None
		
		ibeacon_proximity_uuid = beacon.get("proximityUUID", None)
		flat_beacon["ibeacon_proximity_uuid"] = ibeacon_proximity_uuid.upper() if ibeacon_proximity_uuid else None
		
		flat_beacon["ibeacon_major"] = beacon.get("major", None)
		flat_beacon["ibeacon_minor"] = beacon.get("minor", None)

		bluetooth_address = beacon.get("bluetoothAddress", None)
		flat_beacon["bluetooth_address"] = bluetooth_address.upper() if bluetooth_address else None
		
		flat_beacon["name"] = beacon.get("name", None)
		
		return flat_beacon

	@staticmethod
	def flatten_device(device):
		flat_device = dict()
		flat_device["id"] = device["id"].upper()
		serial_number = device.get("serialNumber", None)
		flat_device["serial_number"] = serial_number.upper() if serial_number else None
		flat_device["name"] = device.get("name", None)
		return flat_device

	@staticmethod
	def flatten_site(site):
		flat_site = dict()
		flat_site["id"] = site["id"].upper()
		flat_site["name"] = site.get("name", None)
		flat_site["team_id"] = site.get("teamID", None)
		flat_site["team_name"] = site.get("teamName", None)		
		return flat_site

	@staticmethod
	def flatten_team(team):
		flat_team = dict()
		flat_team["id"] = team["id"].upper()
		flat_team["name"] = team.get("name", None)
		return flat_team
