from bcapiclient import *
from bcobjectflatteners import * 

# App-token login credentials
app_token = None
username = None
password = None

# Pick ONLY one parameter as string. Leave the others as None
# 	team_id={team id} for all Beacons in that team
# 	site_id={site id} for all Beacons in that site
#	list_sites={team id} for all sites 
# 	set team_id, site_id, list_sites to None for all Groups 
team_id = None
site_id = None
list_sites = None


# devices list
devices = []

def beacon_query(team_id=team_id, site_id=site_id): 
	success, paginated_beacons = api_client.paginate_beacons(team_id=team_id, site_id=site_id)
	if success:
		devices.extend(paginated_beacons)

def get_all_sites(all_sites):
	success, siteList = api_client.paginate_sites(all_sites)
	siteDict = {}
	for site in siteList:
		siteName = site['name']
		siteID = site['id']
		siteDict[siteName] = siteID

	print "\nList of Sites and IDs:"
	print json.dumps(siteDict, indent=4, sort_keys=True)
	exit()

def get_team_ids():
	success, teamList = api_client.paginate_teams()
	teamDict = {}
	for team in teamList:
		teamName = team['name']
		teamID = team['id']
		teamDict[teamName] = teamID

	print "\nList of Teams and IDs:"
	print json.dumps(teamDict, indent=4, sort_keys=True)
	print "\nRerun script again with a Team ID"
	exit()

# Checking type of credentials
if (username and password and app_token) is None:
	print "Go back and enter app token, username, and password"
	exit()

elif (username and password and app_token) is not None:
	api_client = BCAPIClient.build_client_from_username_password(app_token, username, password)
	if (team_id is None) and (site_id is None) and (list_sites is None):
		get_team_ids()
	elif list_sites is not None: 
		get_all_sites(list_sites)

	elif api_client:
		if team_id is not None:
			beacon_query(team_id=team_id, site_id=None)
			
		elif site_id is not None:
			beacon_query(team_id=None, site_id=site_id)

		for device in devices:
			# to print all beacon info, print device instead of flat device
			flat_device = BCObjectFlatteners.flatten_beacon(device)
			print flat_device






