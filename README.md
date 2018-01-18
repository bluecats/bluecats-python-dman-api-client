# bluecats-python-api-client


### Obtaining Credentials
This is an example of using the BlueCats Web API. Once you download the script, you will need to give the API some credentials. To obtain those credentials:

1. Go to the [BlueCats Web App](https://app.bluecats.com)
2. Create an app. 
3. Give a name to your app. For your API credentials: 
4.  Once you create your app, click "Show App Token/Secret"
5. Write down the *APP Token*


Add your BlueCats Web App email, password, and your recently acquired app-token as strings. For example:

```python
app_token="nas29204uasidjasoidnas"
email="email@gmail.com"
password="sajdopasjqf"
```


### Obtaining IDs 
Once you enter the app token and username, password, run the 
script in your preferred way of running it. 

```python
python api_main.py
```


You will get a list of all team names and ids. For obtaining other types of information, pick ONLY one parameter as string leave the rest as *None*.

- Set the team_id={team id} as a *string* for all Beacons in that team
- Set the site_id={site id} as a *string* for for all Beacons in that site
- Set the list_sites={team id} as a *string* for to list all site names and the site ids
- Set team id, site id, list sites to *None* for to list all team names and team ids

For example:

```python
team_id = "apsodnapsofnaspofn"
site_id = None
list_sites = None
```

After calling the script with a site_id or team_id, you will receive a list of Beacons. After the Beacons are processed and paginated, this line is called to filter a lot of the data. 

```python
flat_device = BCObjectFlatteners.flatten_beacon(device)
print flat_device 
```

If you want all of the information for the Beacons and to filter it yourself, remove or comment out that function and add print device like so:

```python
#flat_device = BCObjectFlatteners.flatten_beacon(device)
#print flat_device
print device
```

This is a very simple example to show you how to use the BlueCats API. If you have any questions email: ernie@bluecats.com



