# Clipboard App

## Setup
Detailed instructions for setup on Ubuntu are described in a separate section below. Other distributions may have slighly different requirements.
### Python
For Windows, I recommend using [Anaconda](https://www.anaconda.com/download/) to manage your Python environments because it comes with a lot of packages preinstalled that are difficult to set up without Anaconda.
For Mac and Linux, you can choose to use it if you'd like, but it's not as necessary.

### Get the Code
Clone the ClipboardApp repository into your preferred directory with Git Bash on Windows or a normal terminal otherwise: `git clone https://github.com/ClipboardProject/ClipboardApp.git`

### Install Docker
For Windows Home, download from [here](https://docs.docker.com/toolbox/toolbox_install_windows/). Documentation is [here](https://docs.docker.com/toolbox/overview/).
For Windows Professional or Enterprise, download from [here](https://www.docker.com/docker-windows). Documentation is [here](https://docs.docker.com/docker-for-windows/).
For Mac, download from [here](https://www.docker.com/docker-mac). Documentation is [here](https://docs.docker.com/docker-for-mac/).
For Linux, download from your package manager. Documentation is [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/) (Other distros have links on the left side of the page).
Make sure you follow any OS and distro-specific instructions for setting up Docker. It may be helpful to go through the getting started guide [here](https://docs.docker.com/get-started/).

#### Extra Installation Steps for Linux
If you're new to Docker or you're recovering from a failed installation attempt, it's best to start by uninstalling older versions of Docker: `sudo apt-get remove docker docker-engine docker.io`

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

If there were problems during the installation, try removing docker and starting over.<br/>
`sudo apt-get purge docker-ce`<br/>
`sudo rm -rf /var/lib/docker`

Run: `sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose`

Add executable permissions to the docker-compose binary: `sudo chmod +x /usr/local/bin/docker-compose`

Run `docker-compose --version` to verify it installed correctly. It should show a version and build number similar to:
"docker-compose version 1.21.2, build 1719ceb"

If the docker-compose command doesn't work, add the following line to your ~/.bashrc file<br/>
`export PATH="/usr/bin/docker-compose:$PATH"`<br/>
Close and reopen your terminal(s) to apply the changes.

#### Extra Installation Steps for Windows
I was unable to get Kinematic to work on Docker Toolbox, so I would recommend skipping that. Make sure virtualization is enabled in the BIOS. After changing those settings, do a full reboot cycle, 
otherwise Windows may not report that the settings have changed. If you're running Windows 10 Professional, you'll need to make sure Hyper-V is enabled in the "Turn Windows Features On or Off" dialog. 
If you're using Docker Toolbox on Windows Home edition, when you start Windows, you'll want to start the VirtualBox instance manually before starting Docker or Docker will complain about not having an IP address.

### Docker Setup
#### Windows
For Docker Toolbox on Windows Home, go to the environment variables section in the control panel. Look for a variable called DOCKER_HOST. Add another variable called DOCKER_IP which is the same as DOCKER_HOST, 
but with the tcp prefix and the port number removed. For example, if DOCKER_HOST is tcp://192.168.1.11:2376, DOCKER_IP should be 192.168.1.11. Add another variable called DB_CLIENT_IP with a value of localhost. 
For Docker on Windows Professional, do those same steps, except both DOCKER_IP and DB_CLIENT_IP should be localhost.

#### Max and Linux
Add the lines `export DOCKER_IP=localhost` and `export DB_CLIENT_IP=localhost` to your `~/.bashrc` file. If you haven't used your `.bashrc` file before, you may need to source it. To do so, add
`
if [ -f ~/.bashrc ]; then
   source ~/.bashrc
fi
`
to your `~/.bash_profile`.

### Running Docker
If you are using Linux, all of the subsequent Docker commands in this guide must be run with `sudo`. If you would like to be able to use Docker without sudo, 
look through the answers [here](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo)

Verify that Docker installed correctly with: `docker run hello-world`. You should see, "Hello from Docker!"

After setting the environment variables, close all terminals and every editor or process that's running Python. This is needed to ensure that your Python environment correctly reloads your environment variables.
The DOCKER_IP variable is necessary because the versions of Docker that run on VirtualBox generate an IP address that is dependent on the host's configuration, 
so the code will read this variable to know where to make HTTP requests. The DB_CLIENT_IP variable is necessary because the client needs to run on 0.0.0.0 inside the Docker container, 
which is the internal IP address that Docker containers use to communicate with each other, but it needs to run on localhost outside the container. 

Open a Docker terminal on Windows Home, Powershell on Windows Professional, or a normal terminal otherwise, and `cd` into the Git repo. Run `docker-compose build` then `docker-compose up`.

Download Robo 3T from [here](https://robomongo.org/download) using the link on the right. You can use another MongoDB client if you'd prefer. When you start Robo 3T, a popup to configure connections should appear. 
If you're on Windows Home, right click on the New Connection row and click "Edit". Change localhost to your Docker IP and hit "Save". Now press "Connect". Otherwise, leave the settings alone. 
It should connect successfully and you should see a database called Clipboard on the pane on the right. The database should contain a collection called "event" and an index that includes the start and end timestamp, along with other field(s).

### Running scrapers
`cd` into the ClipboardApp repository. If you're using Anaconda, open up an Anaconda terminal and run `conda install --file anaconda-requirements-conda.txt` and `pip install -r anaconda-requirements-pip.txt`. 
Otherwise, run `pip3 install -r requirements.txt`. Use `pip` instead of `pip3` if Python 3 is your default Python version. Now, run `python3 runner.py`. You should see data being sent to the output window. 
For development, you'll want to open the `data_engine` folder in an IDE or text editor of your choice. Any editor should work as long as the `data_engine` folder is set as the base folder for the project. 
This is important because the imports will not work if the base folder for the project is different.