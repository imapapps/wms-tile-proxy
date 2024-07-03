# WMS Tile Proxy
[![python: 3.9.7](https://img.shields.io/badge/python-3.x-lime.svg)](https://www.php.net/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IMapApps: Development](https://img.shields.io/badge/IMapApps-Development-green)](https://imapapps.com)

## Overview

Provide a brief overview of your application here. This template is designed for code repositories. If your repository contains other types of content, such as a collection of notebooks with chapters, consider listing and linking to each chapter.

## Setup and Installation

The installation described here will make use of conda to ensure there are no package conflicts with
existing or future applications on the machine.  It is highly recommended using a dedicated environment
for this application to avoid any issues.

### Recommended
Conda (To manage packages within the applications own environment)

### Environment
- Create the env

```commandline
conda env create -f environment.yml
```

Add a file named data.json in the base directory.  This file will hold a json object containing
specific information to run your application that you might want secret and in this case we include an easy
way to load a sample dataset.  I am using CHIRPS data (/thredds/wms/Agg/ucsb-chirps_global_0.05deg_daily.nc4),
you will need to change that to a dataset you have in your thredds server.  This should be the url with the domain
removed as you see in the example. This will make the url target the application and the proxy will do the work.  
Also, you will need to update the sample_layer_layers and style property to match your specific layer. 

A quick piece of information:  You will need to run this application on the same network as the private data.  If you 
want to test with a public thredds dataset you can point to that in the THREDDS_SERVER_URL.  Keep in mind it is not 
private data if it's exposed publicly.  Our concept is to set up a thredds server on the same network as the application 
server.  Open public access only to the application server, the proxy will access through the local ip address, 
for example 10.0.0.8 or whatever your local network ip address is.
 
The format will be:

```json
{
  "siteID": 3,
  "SECRET_KEY": "(~;|use_random_characters_for_this/:~|",
  "ALLOWED_HOSTS": ["localhost", "127.0.0.1", "your_domain"],
  "CSRF_TRUSTED_ORIGINS": ["http://localhost:8000", "http://127.0.0.1:8000", "https://your_domain.com"],
  "THREDDS_SERVER_URL": "local url to your thredds server on the same network as the deployment server /thredds/wms/",
  "DEBUG": "True",
  "ACCOUNT_DEFAULT_HTTP_PROTOCOL": "http",
  "sample_layer_url": "/thredds/wms/Agg/ucsb-chirps_global_0.05deg_daily.nc4",
  "sample_layer_layers": "precipitation_amount",
  "sample_layer_style": "boxfill/apcp_surface"
}
```

- Google Authentication setup
This example uses Google authentication, you may substitute with any authentication you prefer or even combine multiple.
1. In a browser navigate to https://console.cloud.google.com/projectcreate
2. Follow the prompts to create the project.
3. After you create the project you must select it from the project dropdown in the top menu bar.
4. In the left panel under APIs & Services click the "OAuth consent screen" link, then fill out the form with the 
information for your application. There are a few pages with choices, proceed when finished.
5. In the left panel click "Credentials" link
6. At the top left click + Create Credentials and select "OAuth 2.0 Client ID"
7. In the dropdown select "Web Application" and give a name. 
8. In the App Domain fields use the dev domains for example:
   1. http://127.0.0.1:8000/
   2. http://127.0.0.1:8000/terms-privacy
   3. http://127.0.0.1:8000/terms-privacy
9. Add Authorized JavaScript origins (you may enable multiple)
   1. Examples:
      1. http://localhost:8000
      2. http://127.0.0.1:8000
      3. https://your_domain
10. Add Authorized redirect URIs (you may enable multiple)
   1. Examples:
      1. http://localhost:8000/accounts/google/login/callback/
      2. http://127.0.0.1:8000/accounts/google/login/callback/
      3. https://your_domain/accounts/google/login/callback/
11. Copy and save the Client ID and Client secret to your local machine (you will need these later)
12. Click DOWNLOAD JSON and save
13. Click save

- enter the environment

```shell
conda activate web_tile_proxy
```

- Create database tables and superuser
###### follow prompts to create superuser (do not use your Google account email for the superuser)
```commandline
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

- Start the App
```commandline
python manage.py runserver
```
1. Open a browser, navigate to http://127.0.0.1:8000/admin/ and login with the superuser
2. Click Social applications
3. Click ADD SOCIAL APPLICATION
4. Select Google in the provider
5. Enter your application name in name
6. Enter the Client id from the Google console
7. Enter the Secret Key from the Google console
8. Leave Key empty
9. Select 127.0.0.1 and hit the arrow to move it to Chosen sites
10. Click Save and continue editing
11. If 127.0.0.1 is not still in Chosen sites repeat step 9 and 10.
12. In the right panel click Groups
13. Click add group and enter Private_Data_Viewer for the name
14. Leave permissions ain their default state and click save
15. Click VIEW SITE at the top right of the screen

Your site should be ready to test.  You should be able to view the private data on the map currently because
you are still logged in as the superuser.  You can test the general user functionality by logging out, then 
clicking Login with Google and login with a different Google account.  This user by default will not see the private 
data shown on the map.  Now you will have to log out from the Google account and log back in with your 
superuser by navigating to http://127.0.0.1:8000/admin/ again.  Click Users, click the user that was created, 
then scroll down to Groups.  Select the Private_Data_Viewer group and move it to Chosen Groups.  Click save.
Log out from the superuser and log back in with your Google account and you will see the data on the map.



## Contact
- [Billy Ashmall](https://github.com/billyz313)

### Authors

- [Billy Ashmall](https://github.com/billyz313)



## License and Distribution

WMS Tile Proxy is distributed by IMapApps under the terms of the MIT License. See
[LICENSE](LICENSE) in this directory for more information.

## Privacy & Terms of Use

WMS Tile Proxy abides to all of IMapApps's privacy and terms of use as described
at [https://imapapps.com/Privacy-Terms-of-Use.html](https://imapapps.com/Privacy-Terms-of-Use.html).