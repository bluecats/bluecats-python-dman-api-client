import requests
import base64
import json
import getpass
import os
import shutil

class BCDmanAPIClient(object):

    base_url = "https://api.bluecats.com/"
    headers = None

    @staticmethod
    def login_from_app_token(app_token, configs_dir=None, verbose=False):
        username = None
        password = None
        authorized = False
        while not authorized:
            if not username:
                username = raw_input("enter bluecats dman api username/email:")
            if username and not password:
                password = getpass.getpass("enter bluecats dman api password:")
            if not username or not password:
                print "sorry, try again or use Ctrl-D to exit"
            else:
                api_client = BCDmanAPIClient.build_client_from_app_token_username_password(app_token, username, password, verbose=verbose)
                if api_client:
                    authorized = api_client.check_user_authorization()
                    if authorized:
                        answer = raw_input("do you want to save your credentials? YES/no:")
                        if not answer or len(answer) > 0 and answer.lower() == 'yes':
                            BCDmanAPIClient.save_user_config(app_token, username, password, configs_dir=configs_dir)
                    return api_client
                if not authorized:
                    print "sorry, try again or use Ctrl-D to exit"
                    username = None
                    password = None

    def login_from_client_id(client_id, configs_dir=None, verbose=False):
        username = None
        password = None
        authorized = False
        while not authorized:
            if not username:
                username = raw_input("enter bluecats dman api username/email:")
            if username and not password:
                password = getpass.getpass("enter bluecats dman api password:")
            if not username or not password:
                print "sorry, try again or use Ctrl-D to exit"
            else:
                api_client, access_token = BCDmanAPIClient.build_client_from_client_id_username_password(client_id, username, password, verbose=verbose)
                if api_client:
                    authorized = api_client.check_user_authorization()
                    if authorized:
                        if access_token:
                            answer = raw_input("do you want to save your access token? YES/no:")
                            if not answer or len(answer) > 0 and answer.lower() == 'yes':
                                BCDmanAPIClient.save_access_token_config(access_token, configs_dir=configs_dir)
                        return api_client
                if not authorized:
                    print "sorry, try again or use Ctrl-D to exit"
                    username = None
                    password = None

    @staticmethod
    def save_user_config(app_token, username, password, configs_dir=None):
        try:
            data = {
                'app_token':app_token,
                'username':username,
                'password':password
            }
            if configs_dir is None:
                configs_dir = get_default_configs_dir()
            if not os.path.exists(configs_dir):
                os.makedirs(configs_dir)
            filename = os.path.join(configs_dir, 'user_config.json')
            with open(filename, 'w') as f:
                json.dump(data, f)
            print "saved user config"
        except:
            print "failed to save user config"

    @staticmethod
    def save_access_token_config(access_token, configs_dir=None):
        try:
            data = {'access_token':access_token}
            if configs_dir is None:
                configs_dir = get_default_configs_dir()
            if not os.path.exists(configs_dir):
                os.makedirs(configs_dir)
            filename = os.path.join(configs_dir, 'access_token_config.json')
            with open(filename, 'w') as f:
                json.dump(data, f)
            print "saved access token config"
        except:
            print "failed to save access token config"

    @staticmethod
    def save_client_config(client_id, client_secret, configs_dir=None):
        try:
            data = {'client_id':client_id,'client_secret':client_secret}
            if configs_dir is None:
                configs_dir = get_default_configs_dir()
            if not os.path.exists(configs_dir):
                os.makedirs(configs_dir)
            filename = os.path.join(configs_dir, 'client_config.json')
            with open(filename, 'w') as f:
                json.dump(data, f)
            print "saved client config"
        except:
            print "failed to save client config"

    @staticmethod
    def login_from_user_config(configs_dir=None, verbose=False):
        try: 
            if configs_dir is None:
                configs_dir = get_default_configs_dir()
            if os.path.exists(configs_dir):
                filename = os.path.join(configs_dir, 'user_config.json')
                config = json.load(open(filename))
                if 'app_token' in config and 'username' in config and 'password' in config:
                    api_client = BCDmanAPIClient.build_client_from_app_token_username_password(config['app_token'], config['username'], config['password'])
                    if api_client.check_user_authorization():
                        return api_client
                    else:
                        print "user not authorized"
                else:
                    print "app_token, username, and password required"
            else:
                print "configs directory not found"
        except:
            print "failed to load user_config.json in configs directory"

    def login_from_acess_token_config(configs_dir=None, verbose=False):
        try: 
            if configs_dir is None:
                configs_dir = get_default_configs_dir()
            if os.path.exists(configs_dir):
                filename = os.path.join(configs_dir, 'access_token_config.json')
                config = json.load(open(filename))
                if 'access_token' in config:
                    api_client = BCDmanAPIClient.build_client_from_auth_token(config['access_token'])
                    if api_client.check_user_authorization():
                        return api_client
                    else:
                        print "user not authorized"
                else:
                    print "access_token required"
            else:
                print "configs directory not found"
        except:
            print "failed to load acess_token_config.json in configs directory"

    @staticmethod
    def login_from_client_config(configs_dir=None, verbose=False):
        try: 
            if configs_dir is None:
                configs_dir = get_default_configs_dir()
            if os.path.exists(configs_dir):
                filename = os.path.join(configs_dir, 'client_config.json')
                config = json.load(open(filename))
                if 'client_id' in config and 'client_secret' in config:  
                    return BCDmanAPIClient.build_client_from_client_id_secret(config["client_id"], config["client_secret"])
                else:
                    print "client_id and client_secret required"
            else:
                print "configs directory not found"
        except:
            print "failed to load client_config.json in configs directory"      

    @staticmethod
    def remove_configs_dir(configs_dir=None):
        try:
            if configs_dir is None:
                configs_dir = get_default_configs_dir()
            if os.path.exists(configs_dir):
                shutil.rmtree(configs_dir)
            print "removed configs dir"
        except:
            print "failed to remove configs dir" 

    staticmethod
    def get_default_configs_dir():
        cur_dir = os.getcwd()
        return os.path.join(cur_dir,'configs')

    @staticmethod
    def build_client_from_client_id_secret(client_id, client_secret, verbose=True):
         api_client = BCDmanAPIClient(verbose=verbose)
         return api_client.build_from_client_id_secret(client_id, client_secret)

    @staticmethod
    def build_client_from_app_token_username_password(app_token, username, password, verbose=True):
         api_client = BCDmanAPIClient(verbose=verbose)
         return api_client.build_from_app_token_username_password(app_token, username, password)

    @staticmethod
    def build_client_from_client_id_username_password(client_id, username, password, verbose=True):
         api_client = BCDmanAPIClient(verbose=verbose)
         return api_client.build_from_client_id_username_password(client_id, username, password)
    
    def __init__(self, verbose=False):
        self.verbose = verbose

    def print_error(self, message, status_code, parsed = None):
        if parsed: 
            print message + " - response: " + json.dumps(parsed, sort_keys=True, indent=4)
        else:
            print message + " - status_code: " + str(status_code)

    def build_from_client_id_secret(self, client_id, client_secret):
        raw_auth = client_id + ":" + client_secret
        auth_header_val = "BlueCats " + base64.b64encode(raw_auth)
        self.headers = {
        'Content-Type': "application/json",
        'Authorization': auth_header_val,
        'X-Api-Version': "3"
        }
        return self

    def build_from_app_token_username_password(self, app_token, username, password):
        raw_auth = app_token + ":" + username + ":" + password
        auth_header_val = "BlueCats " + base64.b64encode(raw_auth)
        self.headers = {
        'Content-Type': "application/json",
        'Authorization': auth_header_val,
        'X-Api-Version': "3"
        }
        return self

    def build_from_client_id_username_password(self, client_id, username, password):

        data = {'client_id':client_id, 'grant_type': 'password', 'username': username, 'password':password }
        url = self.base_url + "token"
        r = requests.post(url, data=data, verify=True)
        if r.status_code == requests.codes.ok:
            parsed = r.json()
            access_token = parsed['access_token']
            auth_header_val = "Bearer " + access_token
            self.headers = {
            'Content-Type': "application/json",
            'Authorization': auth_header_val,
            'X-Api-Version': "3"
            }
            return (self, access_token)
        else:
            print "user auth failed"
            return (None, None)

    def build_from_access_token(self, caccess_token):
        auth_header_val = "Bearer " + parsed['access_token']
        self.headers = {
        'Content-Type': "application/json",
        'Authorization': auth_header_val,
        'X-Api-Version': "3"
        }
        return self

    def check_user_authorization(self):
        if self.verbose: 
            print "checking bluecats dman api authorization"

        url = self.base_url + "account/verifycredentials"
        r = requests.get(url, headers=self.headers, verify=True)
        authorized = r.status_code == requests.codes.ok
        
        if self.verbose:
            if authorized:
                print "authorized"
            else:
                print "authorization failed - status_code:" + str(r.status_code)
        
        return authorized

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

    def get_sites(self, team_id=None, site_id=None, page=1, per_page=100):
        url = self.base_url + "sites?page=" + str(page) + "&perPage=" + str(per_page)
        if team_id:
            url += "&teamID=" + team_id
        elif site_id:
            url += "&siteID=" + site_id
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
            print "patching beacon " + beacon_id

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
