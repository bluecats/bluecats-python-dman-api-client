from bcdmanapiclient import BCDmanAPIClient
import json


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

api_client = BCDmanAPIClient.login_from_client_config(verbose=True)
if api_client:
	fan_out_beacons()