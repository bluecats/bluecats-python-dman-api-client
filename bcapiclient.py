import requests
import base64
import json
import getpass

class BCAPIClient(object):

    base_url = "https://api.bluecats.com/"
    headers = None
    authorized = False

    @staticmethod
    def build_client_from_client_id_secret(client_id, client_secret, verbose = True):
         api_client = BCAPIClient(verbose=verbose)
         return api_client.build_from_client_id_secret(client_id, client_secret)

    @staticmethod
    def build_client_from_username_password(app_token, username, password, verbose = True):
         api_client = BCAPIClient(verbose=verbose)
         return api_client.build_from_username_password(app_token, username, password)
    
    def __init__(self, verbose = False):
        self.verbose = verbose

    def print_error(self, message, status_code, parsed = None):
        if parsed: 
            print message + " - response: " + json.dumps(parsed, sort_keys=True, indent=4)
        else:
            print message + " - status_code: " + str(status_code)

    def build_from_client_id_secret(self, client_id, client_secret):
        raw_auth = client_id + ":" + client_secret
        auth_header_val = "BlueCats " + base64.b64encode(raw_auth)
        print(auth_header_val)
        self.headers = {
        'Content-Type': "application/json",
        'Authorization': auth_header_val,
        'X-Api-Version': "3"
        }
        return self

    def build_from_username_password(self, app_token, username, password):
        raw_auth = app_token + ":" + username + ":" + password
        auth_header_val = "BlueCats " + base64.b64encode(raw_auth)
        print(auth_header_val)
        self.headers = {
        'Content-Type': "application/json",
        'Authorization': auth_header_val,
        'X-Api-Version': "3"
        }
        return self

    def check_authorization(self):
        if self.verbose: 
            print "checking bluecats dman api authorization"

        url = self.base_url + "account/verifycredentials"
        r = requests.get(url, headers=self.headers, verify=True)
        self.authorized = r.status_code == requests.codes.ok
        
        if self.verbose:
            if self.authorized:
                print "authorized"
            else:
                print "authorization failed - status_code:" + str(r.status_code)
        
        return self.authorized

    def get_team(self, team_id):
        url = self.base_url + "teams/" + team_id
        return self.get_object("team", team_id, url)

    def get_teams(self, page=1, per_page=100):
        url = self.base_url + "teams?page=" + str(page) + "&perPage=" + str(per_page)
        return self.get_objects("teams", url)

    def paginate_teams(self):
        url_lambda = lambda page,per_page: self.base_url + "teams?page=" + str(page) + "&perPage=" + str(per_page)
        return self.paginate_objects("teams", url_lambda)

    def get_site(self, site_id):
        url = self.base_url + "sites/" + site_id
        return self.get_object("site", site_id, url)

    def get_sites(self, team_id, page=1, per_page=100):
        url = self.base_url + "sites?teamID=" + team_id + "&page=" + str(page) + "&perPage=" + str(per_page)
        return self.get_objects("sites", url)

    def paginate_sites(self, team_id):
        url_lambda = lambda page,per_page: self.base_url + "sites?teamID=" + team_id + "&page=" + str(page) + "&perPage=" + str(per_page)
        return self.paginate_objects("sites", url_lambda)

    def get_beacon(self, beacon_id):
        url = self.base_url + "beacons/" + beacon_id
        return self.get_object("beacon", beacon_id, url)

    def get_milk(self, beacon_id, water, encrypted_status):
        url = "%sbeacons/%s/milk?water=%s&status=%s" % (
                self.base_url, beacon_id, 
                base64.b64encode(water),
                base64.b64encode(encrypted_status)
                )
        print 'get_milk, url =', url
        return self.get_object("milk", beacon_id, url)

    def get_firmware(self, beacon_id, version, encrypted_status):
        url = "%sbeacons/%s/firmware/%s/hex?status=%s" % (
                self.base_url, beacon_id, version, base64.b64encode(encrypted_status)
                )
        print 'get firmware, url =', url
        r = requests.get(url, headers=self.headers, verify=True)
        return (r.status_code, r.content)

    def get_beacons(self, team_id=None, site_id=None, page=1, per_page=100):
        url = self.base_url + "beacons?page=" + str(page) + "&perPage=" + str(per_page)
        if team_id:
            url += "&teamID=" + team_id
        elif site_id:
            url += "&siteID=" + site_id
        return self.get_objects("beacons", url)

    def paginate_beacons(self, team_id=None, site_id=None):
        url = self.base_url + "beacons"
        if team_id:
            url += "?teamID=" + team_id + "&"
        elif site_id:
            url += "?siteID=" + site_id + "&"
        else:
            url += "?"
        url_lambda = lambda page,per_page: url + "page=" + str(page) + "&perPage=" + str(per_page)
        return self.paginate_objects("beacons", url_lambda)

    def patch_beacon(self, beacon_id, body):
        if self.verbose: 
            print "puting beacon " + beacon_id

        parsed = None
        try:
            url = self.base_url + "beacons/" + beacon_id
            r = requests.patch(url=url, data=body, headers=self.headers, verify=True)
            parsed = r.json()

            return (r.status_code, parsed["beacon"])
        except:
            self.print_error("put beacon " + beacon_id + " failed", r.status_code, parsed) 
            return (r.status_code, None)

    def put_beacon(self, beacon_id, body):
        if self.verbose: 
            print "putting beacon " + beacon_id

        parsed = None
        try:
            url = self.base_url + "beacons/" + beacon_id
            r = requests.put(url=url, data=body, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed["beacon"])
        except:
            self.print_error("patch beacon " + beacon_id + " failed", r.status_code, parsed) 
            return (r.status_code, None)

    def get_pack(self, claim_code):
        if self.verbose: 
            print "getting pack " + claim_code

        parsed = None
        try:
            url = self.base_url + "packs/" + claim_code
            r = requests.get(url, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed["starterPack"]) 
        except:
            self.print_error("get pack " + claim_code + " failed", r.status_code, parsed)
            return (r.status_code, None)

    def get_beacon_modes(self, beacon_id):
        if self.verbose: 
            print "getting beacon modes for beacon " + beacon_id

        parsed = None
        try:
            url = self.base_url + "beacons/" + beacon_id + "/beaconmodes"
            r = requests.get(url, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed["beaconModes"])
        except:
            self.print_error("get beacon modes for beacon " + beacon_id + " failed", r.status_code, parsed) 
            return (r.status_code, None)

    def get_beacon_regions(self, region_id):
        if self.verbose: 
            print "checking beacon region IDs for beacon " + region_id

        parsed = None
        try:
            url = self.base_url + "beaconRegions/" + region_id
            r = requests.get(url, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed["beaconRegion"]["id"])
        except:
            self.print_error("Beacon Region " + region_id + " failed", r.status_code, parsed) 
            return (r.status_code, None)


    def get_target_speeds(self, beacon_id):
        if self.verbose: 
            print "getting target speeds for beacon " + beacon_id

        try:
            url = self.base_url + "beacons/" + beacon_id + "/targetspeeds"
            r = requests.get(url, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed["targetSpeeds"])
        except:
            self.print_error("get target speeds for beacon " + beacon_id + " failed", r.status_code, parsed) 
            return (r.status_code, None)

    def get_beacon_loudnesses(self, beacon_id):
        if self.verbose: 
            print "getting beacon loudnesses for beacon " + beacon_id

        try:
            url = self.base_url + "beacons/" + beacon_id + "/beaconloudnesses"
            r = requests.get(url, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed["beaconLoudnesses"])
        except:
            self.print_error("get beacon loudnesses for beacon " + beacon_id + " failed", r.status_code, parsed) 
            return (r.status_code, None)

    def get_beacon_futuresettings(self, beacon_id, encrypted_status):
        if self.verbose: 
            print "getting future settings for beacon " + beacon_id

        try:
            url = self.base_url + "beacons/" + beacon_id + "/versions/latest/futuresettings?status=" + \
                        base64.b64encode(encrypted_status) + "&firmwareVersion=latest"
            r = requests.get(url, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed["settings"])
        except:
            self.print_error("get future settings for beacon " + beacon_id + " failed", r.status_code, parsed) 
            return (r.status_code, None)

    def get_beacon_settings(self, beacon_id, encrypted_status):
        if self.verbose: 
            print "getting settings for beacon " + beacon_id

        try:
            url = self.base_url + "beacons/" + beacon_id + "/versions/latest/settings?status=" + base64.b64encode(encrypted_status)
            r = requests.get(url, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed["settings"])
        except:
            self.print_error("get settings for beacon " + beacon_id + " failed", r.status_code, parsed) 
            return (r.status_code, None)

    def confirm_beacon_settings(self, beacon_id, encrypted_status):
        if self.verbose: 
            print "confirming settings for beacon " + beacon_id

        try:
            url = self.base_url + "beacons/" + beacon_id + "/versions/confirm?status=" + base64.b64encode(encrypted_status)
            r = requests.put(url, headers=self.headers, verify=True)
            return (r.status_code, r.status_code == requests.codes.accepted)
        except:
            self.print_error("confirm settings for beacon " + beacon_id + " failed", r.status_code, None) 
            return (r.status_code, False)

    def confirm_beacon_firmware(self, beacon_id, encrypted_status):
        if self.verbose: 
            print "confirming firmware for beacon " + beacon_id

        try:
            print "encrypted_status:", encrypted_status
            print "base64 encrypted_status:" + base64.b64encode(encrypted_status)
            url = self.base_url + "beacons/" + beacon_id + "/firmware/confirm?status=" + base64.b64encode(encrypted_status)
            print "the URL is: ", url
            r = requests.put(url, headers=self.headers, verify=True)
            return (r.status_code, r.status_code == requests.codes.accepted)
        except:
            self.print_error("confirm settings for beacon " + beacon_id + " failed", r.status_code, None) 
            return (r.status_code, False)

    def get_device(self, device_id):
        url = self.base_url + "devices/" + device_id
        return self.get_object("device", device_id, url)

    def get_devices(self, team_id=None, site_id=None, page=1, per_page=100):
        if self.verbose: 
            print "getting devices"

        parsed = None
        try:
            url = self.base_url + "devices?page=" + str(page) + "&perPage=" + str(per_page)
            if(team_id is not None):
                url += "&teamID=" + team_id
            if(site_id is not None):
                url += "&siteID=" + site_id
            r = requests.get(url, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed["devices"], parsed["pagination"])
        except:
            self.print_error("get devices failed", r.status_code, parsed) 
            return (r.status_code, None, None)

    def paginate_devices(self, team_id=None, site_id=None):
        return self.paginate_objects("device", lambda page,per_page: self.get_devices(team_id=team_id, site_id=site_id, page=page, per_page=per_page))

    def patch_device(self, device_id, body):
        if self.verbose: 
            print "patching device " + device_id

        parsed = None
        try:
            url = self.base_url + "devices/" + device_id
            r = requests.patch(url=url, data=body, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed["device"])
        except:
            self.print_error("patch device " + device_id + " failed", r.status_code, parsed) 
            return (r.status_code, None)
    
    def get_object(self, object_key, object_id, get_object_url):
        if self.verbose: 
            print "getting " + object_key + " " + object_id

        parsed = None
        try:
            r = requests.get(get_object_url, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed[object_key])
        except:
            self.print_error("get " + object_key + " " + object_id + " failed", r.status_code, parsed) 
            return (r.status_code, None)

    def get_objects(self, objects_key, get_objects_url):
        if self.verbose: 
            print "getting " + objects_key

        parsed = None
        try:
            r = requests.get(get_objects_url, headers=self.headers, verify=True)
            parsed = r.json()
            return (r.status_code, parsed[objects_key], parsed["pagination"])
        except:
            self.print_error("get " + objects_key + " failed", r.status_code, parsed) 
            return (r.status_code, None, None)


    def paginate_objects(self, objects_key, get_objects_url_lambda):
        if self.verbose: 
            print "paginating " + objects_key

        objects = []
        next_page = 1
        page_count = 1
        per_page = 100
        while next_page <= page_count:
            url = get_objects_url_lambda(page=next_page, per_page=per_page)
            status_code, next_objects, pagination = self.get_objects(objects_key=objects_key, get_objects_url=url)
            if status_code == requests.codes.ok:
                objects.extend(next_objects)
                next_page = pagination["page"] + 1
                page_count = pagination["pageCount"]
                if self.verbose:
                    print "page " + str(next_page - 1) + " of " + str(page_count) + " contains " + str(len(next_objects)) + " " + objects_key
            else:
                return (False, objects)

        return (True, objects)
