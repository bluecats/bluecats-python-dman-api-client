from bcdmanapiclient import BCDmanAPIClient
import json
import requests


def patch_beacons():

	success, paginated_beacons = api_client.paginate_beacons(team_id=None, site_id=None)
	if success:
		beaconList = paginated_beacons
	failed_patches = []	

	for beacon in paginated_beacons:
		body = None
		body = {"name": "hello"}
		#body =  {"customValueList": [{"key": "key", "value": "value"}]}
		status_code, patched_beacon = api_client.patch_beacon(beacon["id"], json.dumps(body))
		if status_code != requests.codes.ok:
			failed_patches.append(beacon)
			failed = True
		else:
			print "patched beacons" 

api_client = BCDmanAPIClient.login_from_client_config()
if api_client:
	patch_beacons()

	







