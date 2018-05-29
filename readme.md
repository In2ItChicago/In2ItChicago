# Clipboard App

## Setup

### Python
For Windows, I recommend using [Anaconda](https://www.anaconda.com/download/) to manage your Python environments because it comes with a lot of packages preinstalled that are difficult to set up without Anaconda.
For Mac and Linux, you can choose to use it if you'd like, but it's not as necessary.

### Get the Code
Clone the ClipboardApp repository into your preferred directory with Git Bash on Windows or a normal terminal otherwise: `git clone https://github.com/ClipboardProject/ClipboardApp.git`
Switch to the dockerconfig branch: `git checkout remotes/origin/dockerconfig`

### Setup Docker
For Windows, download from [here](https://docs.docker.com/toolbox/toolbox_install_windows/). Documentation is [here](https://docs.docker.com/toolbox/overview/).
For Mac, download from [here](https://www.docker.com/docker-mac). Documentation is [here](https://docs.docker.com/docker-for-mac/).
For Linux, download from your package manager. Documentation is [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/) (Other distros have links on the left side of the page).
When installing the Windows version, I was unable to get Kinematic to work, so I would recommend skipping that.
Make sure you follow any OS and distro-specific instructions for setting up Docker. It may be helpful to go through the getting started guide [here](https://docs.docker.com/get-started/).

If you're running Windows, make sure virtualization is enabled in the BIOS. After changing those settings, do a full reboot cycle, otherwise Windows may not report that the settings have changed. If you're running Windows 10 Professional, you'll need to disable Hyper-V from the "Turn Windows Features On or Off" dialog. Also, when you start Windows, you'll want to start the VirtualBox instance manually before starting Docker or Docker will complain about not having an IP address.

There is a newer version of Docker for Windows, but it only works on Windows Professional.

Next, we need to set some environment variables. For Windows, go to the environment variables section in the control panel. Look for a variable called DOCKER_HOST. Add another variable called DOCKER_IP which is the same as DOCKER_HOST, 
but with the tcp prefix and the port number removed. For example, if DOCKER_HOST is tcp://192.168.1.11:2376, DOCKER_IP should be 192.168.1.11. Add another one called DB_CLIENT_IP with a value of localhost. 
I believe Mac and Linux can use localhost to connect to Docker. If so, add the lines `export DOCKER_IP=localhost` and `export DB_CLIENT_IP=localhost` to your `.bashrc` file. The DOCKER_IP variable is necessary because the versions of Docker that run on 
VirtualBox generate an IP address that is dependent on the host's configuration, so the code will read this variable to know where to make HTTP requests. The DB_CLIENT_IP variable is necessary because the client needs to 
run on 0.0.0.0 inside the Docker container, which is the internal IP address that Docker containers use to communicate with each other, but it needs to run on localhost outside the container. Open a Docker terminal on Windows or a normal terminal otherwise, and `cd` into the directory that you pulled the code from Git into. Run `docker-compose build` then `docker-compose up`. 

Download Robo 3T from [here](https://robomongo.org/download) using the link on the right. You can use another MongoDB client if you'd prefer. When you start Robo 3T, a popup to configure connections should appear. If you're on Windows, right click on the New Connection row and click "Edit". Change localhost to your Docker IP and hit "Save". Now press "Connect". It should connect successfully and you should see a database called Clipboard on the pane on the right. The database should contain a collection called "event" and an index that includes the start and end timestamp, along with other field(s).

### Running scrapers
If you're using Anaconda, open up an Anaconda terminal and run `conda install scrapy` and `pip install daterangeparser`. Otherwise, `cd` into the `data_engine` folder and run `pip3 install -r requirements.txt`. Use `pip` instead of `pip3` if Python 3 is your default Python version. Now, run `python3 -m runner`. For development, you'll want to open the `data_engine` folder in an IDE or text editor of your choice. Anything should work as long as the `data_engine` folder is set as the base folder for the project.

# Linux Complete Step by Step Setup Process
If you're new to Docker or you're recovering from a failed installation attempt, it's best to start by uninstalling older versions of Docker: `sudo apt-get remove docker docker-engine docker.io`

## Docker Installation
Run: `sudo apt-get update`<br/>
Install the following packages:<br/>
`sudo apt-get install apt-transport-https`<br/>
`sudo apt-get install ca-certificates`<br/>
`sudo apt-get install curl`<br/>
`sudo apt-get install software-properties-common`<br/>
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

Add the lines to the ~/.bashrc file `export DOCKER_IP=localhost` and `export DB_CLIENT_IP=127.0.0.1`

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

Run: `sudo docker-compose build`<br/>
Then run: `sudo docker-compose up`<br/>
Sudo is required for both of the previous commands, if they're not run as sudo, you'll see the following, "ERROR: Couldn't connect to Docker daemon at http+docker://localhost - is it running?"