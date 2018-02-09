from distutils.core import setup 
setup(
	name="bcdmanapiclient", 
	version="0.6",
	packages=["bcdmanapiclient"],
	description="This is a BlueCats device management api client using python",
	url = "https://github.com/bluecats/bluecats-python-dman-api-client",
	author = "BlueCats",
	author_email = "support@bluecats.com",
	install_requires =["requests"]
)