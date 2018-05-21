# Clipboard Scrapers

This repository contains the code for spiders that scrape the data off calendar source websites.

## Dependencies

Install dependencies with `pip3 install Scrapy DateRangeParser python-dateutil bs4 requests`

## Running scrapers

In command line: `python3 -m runner`
This will print out the results of the scrape. To debug one specific scraper, comment out the other scrapers in runner.py

# Clipboard App

## Setup

### Python
For Windows, I recommend using [Anaconda](https://www.anaconda.com/download/) to manage your Python environments because it comes with a lot of packages preinstalled that are difficult to set up without Anaconda.
For Mac and Linux, it's not nearly as necessary.

### Setup Docker
For Windows, download from [here](https://docs.docker.com/toolbox/toolbox_install_windows/). Documentation is [here](https://docs.docker.com/toolbox/overview/)
For Mac, download from [here](https://www.docker.com/docker-mac). Documentation is [here](https://docs.docker.com/docker-for-mac/).
For Linux, download from your package manager. Documentation is [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/) (Other distros have links on the side)
When installing the Windows version, I was unable to get Kinematic to work, so I would recommend skipping that.
Make sure you follow any OS and distro-specific instructions for setting up Docker. It may be helpful to go through the getting started guide [here](https://docs.docker.com/get-started/).

If you're running Windows, make sure virtualization is enabled in the BIOS. After changing those settings, do a full reboot cycle, otherwise Windows may not report that the settings have changed. If you're running Windows 10 Professional, you'll need to disable Hyper-V from the "Turn Windows Features On or Off" dialog. Also, when you start Windows, you'll want to start the VirtualBox instance manually before starting Docker or Docker will complain about not having an IP address.

There is a newer version of Docker for Windows, but it only works on Windows Professional, and at the time of writing this, currently contains a bug which prevents Couchbase from mounting its storage volume.

Next, we need to set some environment variables. For Windows, go to the environment variables section in the control panel. Look for a variable called DOCKER_HOST. Add another variable called DOCKER_IP which is the same as DOCKER_HOST, 
but with the tcp prefix and the port number removed. For example, if DOCKER_HOST is tcp://192.168.1.11:2376, DOCKER_IP should be 192.168.1.11. Add another one called DB_CLIENT_IP with a value of 127.0.0.1. 
I believe Mac and Linux can use localhost to connect to Docker. If so, add the lines `export DOCKER_IP=localhost` and `export DB_CLIENT_IP=127.0.0.1` to your `.bashrc` file. The DOCKER_IP variable is necessary because the versions of Docker that run on 
VirtualBox generate an IP address that is dependent on the host's configuration, so the code will read this variable to know where to make HTTP requests. The DB_CLIENT_IP variable is because the client needs to 
run on 0.0.0.0 inside the Docker container, which is the internal IP address that Docker containers use to communicate with each other, but it needs to run on 127.0.0.1 outside the container.

Open a Docker terminal on Windows or a normal terminal otherwise, and `cd` into the directory you pulled the code into.
`cd` again into the `build_client_image` directory and run `./build.sh` script to create the base image that will run the Couchbase client. 
This will take a few minutes to run. After it completes, run `docker image ls` and verify that an image called `clipboarddbclient` exists.

`cd ..` to get back to the main directory and run `docker-compose build` then `docker-compose up`. This will eventually throw an error about an invalid username/password combination, but that is only because the database is set up.
Open a web browser and navigate to `your.docker.ip:8091` if on Windows or `localhost:8091` if not. It may take a minute or two, but eventually you should be able to connect and a webpage that says "Couchbase Server" will appear.
Once this happens, `cd` into the `clipboard_db` directory and run `./create_db.sh`. Once that completes, refresh the Couchbase web page. If all went well, you should see a login prompt. Login with username "admin" and password "clipboard".
Click on "Buckets" on the sidebar and verify that a bucket called "event" exists. Now, go back to the command prompt and run `./create_indexes.sh`. Go to the "Indexes" tab on the web page and verify that an index was created. 
This script has to be run after the database creation script because it takes a minute for the index service to initialize and it'll throw an error if you try to create the index too quickly. Once the database is configured, 
press `Ctrl+C` in the terminal running Docker to close the container, then run `docker-compose up` again to start the newly-configued container. 

# Linux Complete Step by Step Setup Process
If you're new to Docker or you're recovering from a failed installation attempt, it's best to start by uninstalling older versions of Docker: `sudo apt-get remove docker docker-engine docker.io`

## Docker Installation
Run: `sudo apt-get update`<br/>
Install the following packages:<br/>
`
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
`<br/>
These allow apt to use a repository over HTTPs

Add Docker's official GNU Privacy Guard (GPG) key<br/>
`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`<br/>
This should print, "OK" to the terminal.

Run: `sudo apt-key fingerprint 0EBFCD88`<br/>
Verify that the Key Fingerprint line shows: 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88

Set up the stable Docker repository:<br/>
`
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
`
Run: `sudo apt-get update` again.<br/>
Install the latest version of Docker CE: `sudo apt-get install docker-ce`

Verify that Docker installed correctly with: `sudo docker run hello-world`<br/>
You should see, "Hello from Docker!"

When docker was installed, the docker user group was created, but no users were added to it, you'll need to run docker commands with sudo.

### Installation Problems
If there were problems during the installation, try removing docker and starting over.<br/>
`sudo apt-get purge docker-ce`<br/>
`sudo rm -rf /var/lib/docker`

## Docker Compose installation
Run: `sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose`

Add executable permissions to the docker-compose binary: `sudo chmod +x /usr/local/bin/docker-compose`

Run `docker-compose --version` to verify it installed correctly. It should show a version and build number similar to:
"docker-compose version 1.21.2, build 1719ceb"

If the docker-compose command doesn't work, add the following line to your ~/.bashrc file<br/>
`export PATH="/usr/bin/docker-compose:$PATH"`<br/>
Close and reopen your terminal(s) to apply the changes.

## Running the ClipboardApp Docker project
Clone the ClipboardApp repository: `git clone https://github.com/ClipboardProject/ClipboardApp.git`<br/>
Switch to the dockerconfig branch: `git checkout remotes/origin/dockerconfig`<br/>
Cd into the build_client_image directory: `cd build_client_image`<br/>
Make the build.sh file executable by running: `chmod +x build.sh`<br/>
Run the build.sh file: `./build.sh`<br/>
The build process will take a few minutes but it should end with:<br/>
  "Successfully built c0a3ca505876<br/>
  Successfully tagged clipboarddbclient:latest"<br/>
To verify that the image was built successfully, run: `sudo docker image ls`<br/>
Make sure that "clipboarddbclient" is present

Cd back into the ClipboardApp root directory and run: `sudo docker-compose build`<br/>
Then run: `sudo docker-compose up`<br/>
Sudo is required for both of the previous commands, if they're not run as sudo, you'll see the following, "ERROR: Couldn't connect to Docker daemon at http+docker://localhost - is it running?"

It may take 1-2mins after running sudo docker-compose up before the server is ready to start serving requests.

Navigate to: `http://localhost:8091` in your browser and when the server is ready, it'll show a webpage that says, "Couchbase Server."

Once you're able to see the webpage, open a new terminal and cd into the clipboard_db directory and make the create_db.sh file executable by running: `chmod +x create_db.sh`<br/>
Then run: `./create_db.sh`<br/>
Refresh the Couchbase webpage and you should see a login prompt.<br/>
Use the following login credentials: `Username: admin, Password: clipboard`

Click on "Buckets" on the sidebar to verify that a bucket called "event" exists. 

Go back to the terminal and make the create_indexes.sh file executable by running: `chmod +x create_indexes.sh`<br/>
Then run: `./create_indexes.sh`<br/>
Go to the "Indexes" tab on the Couchbase web page and verify that an index was created.

Go back to the terminal where the: sudo docker-compose up command is running and close the container: `CTRL + C`<br/>
Run: `sudo docker-compose up` again to restart the newly-configured container.
