import requests
import base64
import json
import getpass
import os
import shutil
import logging

class BCDmanAPIClient(object):

    base_url = "https://api.bluecats.com/"
    headers = None

    @staticmethod
    def login_from_app_token(app_token, configs_dir=None, verbose=False, save=True):
        username = None
        password = None
        authorized = False
        while not authorized:
            if not username:
                try:
                    username = raw_input("enter bluecats dman api username/email:")
                except:
                    username = input("enter bluecats dman api username/email:")
            if username and not password:
                password = getpass.getpass("enter bluecats dman api password:")
            if not username or not password:
                print("sorry, try again or use Ctrl-D to exit")
            else:
                api_client = BCDmanAPIClient.build_client_from_app_token_username_password(app_token, username, password, verbose=verbose)
                if api_client:
                    authorized = api_client.check_user_authorization()
                    if authorized and save:
                        try:
                            answer = raw_input("do you want to save your credentials? YES/no:")
                        except:
                            answer = input("do you want to save your credentials? YES/no:")
                        if not answer or (len(answer) > 0 and answer.lower() == 'yes'):
                            BCDmanAPIClient.save_user_config(app_token, username, password, configs_dir=configs_dir)
                    return api_client
                if not authorized:
                    print("sorry, try again or use Ctrl-D to exit")
                    username = None
                    password = None

    def login_from_client_id(client_id, configs_dir=None, verbose=False, save=True):
        username = None
        password = None
        authorized = False
        while not authorized:
            if not username:
                try:
                    username = raw_input("enter bluecats dman api username/email:")
                except:
                    username = input("enter bluecats dman api username/email:")
            if username and not password:
                password = getpass.getpass("enter bluecats dman api password:")
            if not username or not password:
                print("sorry, try again or use Ctrl-D to exit")
            else:
                api_client, access_token = BCDmanAPIClient.build_client_from_client_id_username_password(client_id, username, password, verbose=verbose)
                if api_client:
                    authorized = api_client.check_user_authorization()
                    if authorized and save:
                        if access_token:
                            try:
                                answer = raw_input("do you want to save your credentials? YES/no:")
                            except:
                                answer = input("do you want to save your credentials? YES/no:")
                            if not answer or len(answer) > 0 and answer.lower() == 'yes':
                                BCDmanAPIClient.save_access_token_config(access_token, configs_dir=configs_dir)
                    return api_client
                if not authorized:
                    print("sorry, try again or use Ctrl-D to exit")
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
            configs_dir = configs_dir or BCDmanAPIClient.get_default_configs_dir()
            if not os.path.exists(configs_dir):
                os.makedirs(configs_dir)
            filename = os.path.join(configs_dir, 'user_config.json')
            with open(filename, 'w') as f:
                json.dump(data, f)
            print("saved user config")
        except:
            print("failed to save user config")

    @staticmethod
    def save_access_token_config(access_token, configs_dir=None):
        try:
            data = {'access_token':access_token}
            configs_dir = configs_dir or BCDmanAPIClient.get_default_configs_dir()
            if not os.path.exists(configs_dir):
                os.makedirs(configs_dir)
            filename = os.path.join(configs_dir, 'access_token_config.json')
            with open(filename, 'w') as f:
                json.dump(data, f)
            print("saved access token config")
        except:
            print("failed to save access token config")

    @staticmethod
    def save_client_config(client_id, client_secret, configs_dir=None):
        try:
            data = {'client_id':client_id,'client_secret':client_secret}
            configs_dir = configs_dir or BCDmanAPIClient.get_default_configs_dir()
            if not os.path.exists(configs_dir):
                os.makedirs(configs_dir)
            filename = os.path.join(configs_dir, 'client_config.json')
            with open(filename, 'w') as f:
                json.dump(data, f)
            print("saved client config")
        except:
            print("failed to save client config")

    @staticmethod
    def login_from_user_config(configs_dir=None, verbose=False):
        try: 
            configs_dir = configs_dir or BCDmanAPIClient.get_default_configs_dir()
            if os.path.exists(configs_dir):
                filename = os.path.join(configs_dir, 'user_config.json')
                config = json.load(open(filename))
                if 'app_token' in config and 'username' in config and 'password' in config:
                    api_client = BCDmanAPIClient.build_client_from_app_token_username_password(config['app_token'], config['username'], config['password'])
                    if api_client.check_user_authorization():
                        return api_client
                    else:
                        print("user not authorized")
                else:
                    print("app_token, username, and password required")
            else:
                print("configs directory not found")
        except:
            print("failed to load user_config.json in configs directory")

    def login_from_acess_token_config(configs_dir=None, verbose=False):
        try: 
            configs_dir = configs_dir or BCDmanAPIClient.get_default_configs_dir()
            if os.path.exists(configs_dir):
                filename = os.path.join(configs_dir, 'access_token_config.json')
                config = json.load(open(filename))
                if 'access_token' in config:
                    api_client = BCDmanAPIClient.build_from_access_token(config['access_token'])
                    if api_client.check_user_authorization():
                        return api_client
                    else:
                        print("user not authorized")
                else:
                    print("access_token required")
            else:
                print("configs directory not found")
        except:
            print("failed to load acess_token_config.json in configs directory")

    @staticmethod
    def login_from_client_config(configs_dir=None, verbose=False):
        try: 
            configs_dir = configs_dir or BCDmanAPIClient.get_default_configs_dir()
            if os.path.exists(configs_dir):
                filename = os.path.join(configs_dir, 'client_config.json')
                config = json.load(open(filename))
                if 'client_id' in config and 'client_secret' in config:  
                    return BCDmanAPIClient.build_client_from_client_id_secret(config["client_id"], config["client_secret"])
                else:
                    print("client_id and client_secret required")
            else:
                print("configs directory not found")
        except:
            print("failed to load client_config.json in configs directory")      

    @staticmethod
    def remove_configs_dir(configs_dir=None):
        try:
            configs_dir = configs_dir or BCDmanAPIClient.get_default_configs_dir()
            if os.path.exists(configs_dir):
                shutil.rmtree(configs_dir)
            print("removed configs dir")
        except:
            print("failed to remove configs dir") 

    @staticmethod
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
    
    def __init__(self, verbose=False, logger=None):
        self.logger = logger or logging.getLogger()
        self.verbose = verbose

    def print_error(self, message, status_code, parsed = None):
        if parsed: 
            print(message + " - response: " + json.dumps(parsed, sort_keys=True, indent=4))
        else:
            print(message + " - status_code: " + str(status_code))

    def build_from_client_id_secret(self, client_id, client_secret):
        raw_auth = client_id + ":" + client_secret
        try: 
            auth_header_val = "BlueCats " + base64.b64encode(raw_auth)
        except: 
            auth_header_val = "BlueCats " + base64.b64encode(raw_auth.encode()).decode()
        self.headers = {
        'Content-Type': "application/json",
        'Authorization': auth_header_val,
        'X-Api-Version': "3"
        }
        return self

    def build_from_app_token_username_password(self, app_token, username, password):
        raw_auth = app_token + ":" + username + ":" + password
        try: 
            auth_header_val = "BlueCats " + base64.b64encode(raw_auth)
        except: 
            auth_header_val = "BlueCats " + base64.b64encode(raw_auth.encode()).decode()
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
            print("user auth failed")
            return (None, None)

    def build_from_access_token(self, access_token):
        auth_header_val = "Bearer " + access_token
        self.headers = {
        'Content-Type': "application/json",
        'Authorization': auth_header_val,
        'X-Api-Version': "3"
        }
        return self

    def check_user_authorization(self):
        self.logger.debug("checking bluecats dman api authorization")
        url = self.base_url + "account/verifycredentials"
        r = requests.get(url, headers=self.headers, verify=True)
        authorized = r.status_code == requests.codes.ok
        
        if authorized:
            self.logger.debug("authorized")
        else:
            self.logger.debug("authorization failed - status_code:" + str(r.status_code))
        
        return authorized

    def get_team(self, team_id):
        url = self.base_url + "teams/" + team_id
        return self.dman_api_request("team", team_id, url, "get")

    def get_teams(self, page=1, per_page=100):
        url = self.base_url + "teams?page=" + str(page) + "&perPage=" + str(per_page)
        return self.dman_api_request("teams", "", url, "get", pagination=True)

    def paginate_teams(self):
        url_lambda = lambda page,per_page: self.base_url + "teams?page=" + str(page) + "&perPage=" + str(per_page)
        return self.paginate_objects("teams", url_lambda)

    def get_site(self, site_id):
        url = self.base_url + "sites/" + site_id
        return self.dman_api_request("site", site_id, url, "get")

    def get_sites(self, team_id=None, site_id=None, page=1, per_page=100):
        url = self.base_url + "sites?page=" + str(page) + "&perPage=" + str(per_page)
        if team_id:
            url += "&teamID=" + team_id
        elif site_id:
            url += "&siteID=" + site_id
        return self.dman_api_request("sites", "", url, "get", pagination=True)

    def paginate_sites(self, team_id):
        url_lambda = lambda page,per_page: self.base_url + "sites?teamID=" + team_id + "&page=" + str(page) + "&perPage=" + str(per_page)
        return self.paginate_objects("sites", url_lambda)

    def get_beacon(self, beacon_id, latest=False):
        url = self.base_url + "beacons/" + beacon_id
        if latest:
            url += "?version=latest"
        return self.dman_api_request("beacon", beacon_id, url, "get")

    def get_milk(self, beacon_id, water, encrypted_status):
        url = "%sbeacons/%s/milk?water=%s&status=%s" % (
                self.base_url, beacon_id, 
                base64.b64encode(water),
                base64.b64encode(encrypted_status)
                )
        self.logger.debug('get_milk, url = %s', str(url))
        return self.self.dman_api_request("milk", beacon_id, url, "get")

    def get_firmware_info(self, beacon_id, version):
        url = "%sbeacons/%s/firmware/%s/" % (self.base_url, beacon_id, version)
        self.logger.warn('get firmware info, url = %s', str(url))
        r = requests.get(url, headers=self.headers, verify=True)
        parsed = r.json()
        if 'firmware' in parsed:
            parsed = parsed['firmware']
        return r.status_code == requests.codes.ok, parsed

    def get_firmware(self, beacon_id, version, encrypted_status):
        url = "%sbeacons/%s/firmware/%s/hex?status=%s" % (
                self.base_url, beacon_id, version, base64.b64encode(encrypted_status)
                )
        self.logger.debug('get firmware, url = %s', str(url))
        r = requests.get(url, headers=self.headers, verify=True)
        return (r.status_code, r.content)

    def get_beacons(self, team_id=None, site_id=None, page=1, per_page=100, latest=False):
        url = self.base_url + "beacons?page=" + str(page) + "&perPage=" + str(per_page)
        if team_id:
            url += "&teamID=" + team_id
        elif site_id:
            url += "&siteID=" + site_id
        if latest:
            url += "&version=latest"
        return self.dman_api_request("beacons", "", url, "get")

    def paginate_beacons(self, team_id=None, site_id=None, max_page_count=None, latest=False):
        url = self.base_url + "beacons"
        if team_id:
            url += "?teamID=" + team_id + "&"
        elif site_id:
            url += "?siteID=" + site_id + "&"
        else:
            url += "?"
        if latest:
            url += "version=latest&"
        if max_page_count is None:
            url_lambda = lambda page,per_page: url + "page=" + str(page) + "&perPage=" + str(per_page)
        else:
            url_lambda = lambda page,per_page: url + "page=" + str(page) + "&perPage=" + str(per_page)
        return self.paginate_objects("beacons", url_lambda, max_page_count=max_page_count)

    def patch_beacon(self, beacon_id, body):
        self.logger.debug("patching beacon " + beacon_id)
        url = self.base_url + "beacons/" + beacon_id
        return self.dman_api_request("beacon", beacon_id, url, "patch", data=body)

    def post_team(self, body):
        self.logger.debug("creating team")
        url = self.base_url + "teams"
        return self.dman_api_request("team", "", url, "post", data=body)

    def post_site(self, body):
        self.logger.debug("creating site")
        url = self.base_url + "sites"
        return self.dman_api_request("site", "", url, "post", data=body)

    def post_invite(self, body):
        self.logger.debug("creating invite")
        url = self.base_url + "teamInvites"
        return self.dman_api_request("teamInvite", "", url, "post", data=body)

    def put_beacon(self, beacon_id, body):
        self.logger.debug("putting beacon " + beacon_id)
        url = self.base_url + "beacons/" + beacon_id
        return self.dman_api_request("beacon", beacon_id, url, "put", data=body)

    def transfer_beacons(self, body):
        self.logger.debug("transferring beacons")
        result = None
        try:
            url = self.base_url + "beacontransfer"
            r = requests.post(url=url, data=body, headers=self.headers, verify=True)
            return (r.status_code, None)
        except:
            self.print_error("transfer beacons failed", r.status_code, result) 
            return (r.status_code, None)

    def get_pack(self, claim_code):
        self.logger.debug("getting pack " + claim_code)
        url = self.base_url + "packs/" + claim_code
        return self.dman_api_request("starterPack", claim_code, url, "get")

    def get_beacon_modes(self, beacon_id):
        self.logger.debug("getting beacon modes for beacon " + beacon_id)
        url = self.base_url + "beacons/" + beacon_id + "/beaconmodes"
        return self.dman_api_request("beaconModes", beacon_id, url, "get")

    def get_beacon_region(self, region_id):
        self.logger.debug("checking beacon region IDs for beacon " + region_id)
        url = self.base_url + "beaconRegions/" + region_id
        return self.dman_api_request("beaconRegion", region_id, url, "get")

    def get_all_beacon_regions(self):
        self.logger.debug("checking all beacon region IDs")
        url = self.base_url + "beaconRegions/"
        return self.dman_api_request("beaconRegions", "", url, "get")

    def get_target_speeds(self, beacon_id):
        self.logger.debug("getting target speeds for beacon " + beacon_id)
        url = self.base_url + "beacons/" + beacon_id + "/targetspeeds"
        return self.dman_api_request("targetSpeeds", beacon_id, url, "get")

    def get_beacon_loudnesses(self, beacon_id):
        self.logger.debug("getting beacon loudnesses for beacon " + beacon_id)
        url = self.base_url + "beacons/" + beacon_id + "/beaconloudnesses"
        return self.dman_api_request("beaconLoudnesses", beacon_id, url, "get")

    def get_beacon_futuresettings(self, beacon_id, encrypted_status):
        self.logger.debug("getting future settings for beacon " + beacon_id)
        url = self.base_url + "beacons/" + beacon_id + "/versions/latest/futuresettings?status=" + \
                        base64.b64encode(encrypted_status) + "&firmwareVersion=latest"
        return self.dman_api_request("settings", beacon_id, url, "get")

    def get_beacon_settings(self, beacon_id, encrypted_status): 
        self.logger.debug("getting settings for beacon " + beacon_id)
        url = self.base_url + "beacons/" + beacon_id + "/versions/latest/settings?status=" + \
                        base64.b64encode(encrypted_status)
        return self.dman_api_request("settings", beacon_id, url, "get")

    def confirm_beacon_settings(self, beacon_id, encrypted_status):
        self.logger.debug("confirming settings for beacon " + beacon_id)
        try:
            url = self.base_url + "beacons/" + beacon_id + "/versions/confirm?status=" + base64.b64encode(encrypted_status)
            r = requests.put(url, headers=self.headers, verify=True)
            return (r.status_code, r.status_code == requests.codes.accepted)
        except:
            self.print_error("confirm settings for beacon " + beacon_id + " failed", r.status_code, None) 
            return (r.status_code, False)

    def confirm_beacon_firmware(self, beacon_id, encrypted_status):
        self.logger.debug("confirming firmware for beacon " + beacon_id)
        try:
            print("encrypted_status:", encrypted_status)
            print("base64 encrypted_status:" + base64.b64encode(encrypted_status))
            url = self.base_url + "beacons/" + beacon_id + "/firmware/confirm?status=" + base64.b64encode(encrypted_status)
            print("the URL is: ", url)
            r = requests.put(url, headers=self.headers, verify=True)
            return (r.status_code, r.status_code == requests.codes.accepted)
        except:
            self.print_error("confirm settings for beacon " + beacon_id + " failed", r.status_code, None) 
            return (r.status_code, False)

    def get_device(self, device_id):
        url = self.base_url + "devices/" + device_id
        return self.dman_api_request("device", device_id, url, "get")

    def get_devices(self, team_id=None, site_id=None, page=1, per_page=100): 
        self.logger.debug("getting devices")
        url = self.base_url + "devices?page=" + str(page) + "&perPage=" + str(per_page)
        if team_id:
            url += "&teamID=" + team_id
        elif site_id:
            url += "&siteID=" + site_id

        return self.dman_api_request("devices", "", url, "get", pagination=True)

    def paginate_devices(self, team_id=None, site_id=None, max_page_count=None):
        url = self.base_url + "devices"
        if team_id:
            url += "?teamID=" + team_id + "&"
        elif site_id:
            url += "?siteID=" + site_id + "&"
        else:
            url += "?"
        
        if max_page_count is None:
            url_lambda = lambda page,per_page: url + "page=" + str(page) + "&perPage=" + str(per_page)
        else:
            url_lambda = lambda page,per_page: url + "page=" + str(page) + "&perPage=" + str(per_page)
        return self.paginate_objects("devices", url_lambda, max_page_count=max_page_count)

    def patch_device(self, device_id, body): 
        self.logger.debug("patching device " + device_id)
        url = self.base_url + "devices/" + device_id
        return self.dman_api_request("device", device_id, url, "patch", data=body)

    def dman_api_request(self, object_key, object_id, url, requestType, data=None, pagination=False):
        self.logger.debug(requestType + "ing " + object_key + " " + object_id) 
        # gets the request type and wraps it
        request = getattr(requests, requestType)
        try:
            # checks if there is data to post or patch 
            if data is not None:
                r = request(url, data=data, headers=self.headers, verify=True, timeout=30)
            else: 
                r = request(url, headers=self.headers, verify=True, timeout=30)            
            r.raise_for_status()
            # returns data if good request
            if (r.status_code == requests.codes.ok) or (r.status_code == requests.codes.created):
                if pagination:
                    return (r.status_code, r.json()[object_key], r.json()["pagination"])
                else:
                    return (r.status_code, r.json()[object_key])
            else:
                if pagination:
                    return (r.status_code, None, None)
                else: 
                    return (r.status_code, None)
        # when fails and not a bad request (timeouts, other errors)
        except requests.exceptions.RequestException as err:
            getobjecterror = "Error: " + requestType + object_key + " " + object_id + " failed "
            self.print_error(getobjecterror, "", str(err))
            if pagination: 
                return (-1, None, None)
            else:
                return(-1, None)

    def paginate_objects(self, objects_key, get_objects_url_lambda, max_page_count=None):
        self.logger.debug("paginating " + objects_key)

        objects = []
        next_page = 1
        page_count = 1
        per_page = 100
        while next_page <= page_count:
            url = get_objects_url_lambda(page=next_page, per_page=per_page)
            status_code, next_objects, pagination = self.dman_api_request(objects_key, "", url, "get", pagination=True)
            if status_code == requests.codes.ok:
                objects.extend(next_objects)
                next_page = pagination["page"] + 1
                page_count = pagination["pageCount"]
                self.logger.warning("page " + str(next_page - 1) + " of " + str(page_count) + " contains " + str(len(next_objects)) + " " + objects_key)
            else:
                return (False, objects)

            if max_page_count is not None:
                if next_page > int(max_page_count):
                    return(True, objects)

        return (True, objects)
