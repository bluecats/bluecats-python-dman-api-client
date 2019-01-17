from bcdmanapiclient import BCDmanAPIClient
import json
import requests
import csv

app_token = ""
api_client = BCDmanAPIClient.login_from_app_token(app_token, save=False)
def main(): 
	beacons = []
	claim_code = "H6mXwre2" 

	if claim_code:
	    status_code, pack = api_client.get_pack(claim_code=claim_code)
	    if status_code == requests.codes.ok:
	        beacons.extend(pack["beacons"])
	        print "pack contains " + str(len(beacons)) + " beacon(s)"

	template_out(beacons, claim_code + ".csv")



def template_out(fileTemplate, fileTemplateName):

    # creates json file template 
    if "json" in fileTemplateName: 
        if isinstance(fileTemplate, dict):
            fileList = []
            fileList.append(fileTemplate)
        else:
            fileList = fileTemplate
        with open(fileTemplateName, "w") as outfile: 
            json.dump(fileList, outfile, indent=4, sort_keys=True)

    # creates csv file template
    elif "csv" in fileTemplateName:
        csvfile = csv.writer(open(fileTemplateName, "w"))

        if isinstance(fileTemplate, dict):
            csvfile.writerow(fileTemplate.keys())
            csvfile.writerow(fileTemplate.values())

        else: 
            csvfile.writerow(fileTemplate[0].keys())
            for items in fileTemplate: 
                csvfile.writerow(items.values())

    print("\n created file", fileTemplateName)

main()