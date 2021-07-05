# simple_KFHL_dash_app
A simple dash app for running the KFHL bleeding model.

## Usage instructions
Follow these steps to get the app up and running with a clean install of Ubuntu 20.04 LTS:

1. Create a fresh server.  If using Google Cloud, I recommend something small like: N1 type, f1 micro instance
2. Install the following using `apt`: 
```
sudo apt install python3-pip build-essential nginx make gfortran
```

3. Git clone this repository onto the server
4. Upload KFHL model files (from BitBucket if available) into the app directory
5. Delete the executable `KFHLT_forward` in the model file, and the `KFHLT_param` in the param_backup file
6. Run the makefile for each folder, be sure to then run the new param function
7. Install the following with `pip`: 
```
sudo pip install dash uwsgi numpy pandas
```
8. Test out with `python3 myapp.py`.  Should see the stanard debug web server for Dash.
9. Make the `wsgi.py` file inside app directory with the following contents:
```
from myapp import server as application
if __name__ == '__main__':
    application.run()
```

10. Make the `startup.ini` file inside the app directory with the following contents:
```
[uwsgi]
module = wsgi:application
master = true
processes = 5
socket = index.sock
chmod-socket = 664
vacuum = true
die-on-term = true
logto=/var/log/wsgi.log
```
Be sure to replace the username with YOUR username.  

Test out with: `uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi`.  There should not be any errors.

11. Make `dash_app_startup.service` file in /etc/systemd/system/ with the following contents:
```
[Unit]
Description=uWSGI instance to serve startup
After=network.target

[Service]
User=mstobb
Group=www-data
WorkingDirectory=/home/mstobb/simple_KFHL_dash_app
ExecStart=uwsgi --force-cwd /home/mstobb/simple_KFHL_dash_app --ini startup.ini

[Install]
WantedBy = multi-user.target
```
Again, be sure to replace the username with YOUR username.

12. Start the process: 

    1. To start: `sudo systemctl restart dash_app_startup.service`

    2. To check: `sudo systemctl status dash_app_startup.service`

13. Make reverse proxy file `dash_app` in `/etc/nginx/sites-available/` with the following contents:
```
server {
    listen 80;

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/home/mstobb/simple_KFHL_dash_app/index.sock;
    }
}
```

14. Copy the reverse proxy file to `sites-enabled`: 
```
sudo ln -s /etc/nginx/sites-available/dash_app /etc/nginx/sites-enabled
```

15. Remove default proxy setting in `/etc/nginx/sites-enabled`:
```
sudo rm /etc/nginx/sites-enabled/default
```

16. Activate the proxy:

    1. To start: `sudo service nginx restart`

    2. To check: `sudo service nginx status`

17. Visit IP address - your app should be visible!

