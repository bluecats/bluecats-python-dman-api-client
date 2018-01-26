from bcdmanapiclient import *
from bcobjectflatteners import * 

client_id = "15d87a01-6aa8-d489-be44-68b2be8a5d15"
client_secret = "609b224b-e8e9-4fca-9128-4046b87fc32f"

# devices list
devices = []

def fan_out_beacons():
	sucess, siteList, objectCount = api_client.get_sites()
	teamName = siteList[0]["teamName"]
	teamID = siteList[0]["teamID"]

	siteJSON = {"teamID": teamID, "teamName": teamName, "siteList": []}
	for site in siteList:
		siteDict = {}
		success, paginated_beacons = api_client.paginate_beacons(team_id=None, site_id=site["id"])
		if success:
			beaconList = paginated_beacons
		siteDict["name"] = site["name"]
		siteDict["id"] = site["id"]
		siteDict["beaconList"] = beaconList

		siteJSON["siteList"].append(siteDict)
	
	print json.dumps(siteJSON, indent=4, sort_keys=True)


if (client_id and client_secret) is None:
	print "Go back and enter client id and client secret"
	exit()

elif (client_id and client_secret) is not None:
	api_client = BCDmanAPIClient.build_client_from_client_id_secret(client_id, client_secret)

	if api_client:
		fan_out_beacons()
"""
		failed_patches = []
		for device in devices:
			# to print all beacon info, print device instead of flat device
			flat_device = BCObjectFlatteners.flatten_beacon(device)


			print (json.dumps(device, indent=4, sort_keys=True))

			body = None

			#if name:
			#body = {"name": "hello"}
			body =  {"customValueList": [{"key": "key", "value": "value"}]}

			status_code, patched_beacon = api_client.patch_beacon(flat_device["id"], json.dumps(body))
			if status_code != requests.codes.ok:
				failed_patches.append(flat_device)
				failed = True
			else:
				print "patched device"
"""







