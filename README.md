# bluecats-python-dman-api-client

This is an example of using the BlueCats Python Device Management Web API. 
To install the bcdmanpiclient module, copy these commands into your terminal. 

```python

git clone https://github.com/bluecats/bluecats-python-dman-api-client.git
cd bluecats-python-dman-api-client
python setup.py install 

```

Once you install the module, you will need to give the API credentials.

### Obtaining Credentials
 To obtain those credentials:

1. Go to the [BlueCats Web App](https://app.bluecats.com)
2. Go to the app tab then "Create a new app" 
3. Give a name to your app. 
4. Select the platform: API Client
5. Once you create your app, click "Show App Token/Secret"
6. Click "Reset Client Secret"
7. Write down the Client Id and Client Secret


Add your client id and clientsecret as strings in the file *client_configs.json* found in your configs folder. For example:

```python
{
	
"client_id": "12093A12093B-10293A10293-1203920",
"client_secret": "123912-219030921-12EF901"

}

```

Save that file and now you are ready to run the module. 

To see an example of using bcdmanapiclient, go to the examples folder. In your favorite python interpreter run the script "fan_out_beacons.py" or run this command in your terminal. 

```python

cd examples 
python fan_out_beacons.py 

```


This is a very simple example to show you how to use the BlueCats API. If you have any questions email: ernie@bluecats.com

