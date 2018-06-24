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

Run: `sudo apt-get update`  
Install the following packages:  
`sudo apt-get install apt-transport-https`  
`sudo apt-get install ca-certificates`  
`sudo apt-get install curl`  
`sudo apt-get install software-properties-common`  
These allow apt to use a repository over HTTPS

Add Docker's official GNU Privacy Guard (GPG) key  
`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`  
This should print, "OK" to the terminal.

Run: `sudo apt-key fingerprint 0EBFCD88`  
Verify that the Key Fingerprint line shows: 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88

Set up the stable Docker repository:  
`
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
`
Run: `sudo apt-get update` again.  
Install the latest version of Docker CE: `sudo apt-get install docker-ce`

If there were problems during the installation, try removing docker and starting over.  
`sudo apt-get purge docker-ce`  
`sudo rm -rf /var/lib/docker`

Run: `sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose`

Add executable permissions to the docker-compose binary: `sudo chmod +x /usr/local/bin/docker-compose`

Run `docker-compose --version` to verify it installed correctly. It should show a version and build number similar to:
"docker-compose version 1.21.2, build 1719ceb"

If the docker-compose command doesn't work, add the following line to your ~/.bashrc file  
`export PATH="/usr/bin/docker-compose:$PATH"`  
Close and reopen your terminal(s) to apply the changes.

#### Extra Installation Steps for Windows
I was unable to get Kinematic to work on Docker Toolbox, so I would recommend skipping that. Make sure virtualization is enabled in the BIOS. After changing those settings, do a full reboot cycle,
otherwise Windows may not report that the settings have changed. If you're running Windows 10 Professional, you'll need to make sure Hyper-V is enabled in the "Turn Windows Features On or Off" dialog.
If you're using Docker Toolbox on Windows Home edition, when you start Windows, you'll want to start the VirtualBox instance manually before starting Docker or Docker will complain about not having an IP address.

### Docker Setup
#### Windows
For Docker Toolbox on Windows Home, go to the environment variables section in the control panel. Look for a variable called DOCKER_HOST. Add another variable called DOCKER_IP which is the same as DOCKER_HOST,
but with the tcp prefix and the port number removed. For example, if DOCKER_HOST is `tcp://192.168.1.11:2376`, DOCKER_IP should be `192.168.1.11`. Add another variable called DB_CLIENT_IP with a value of `localhost`.
For Docker on Windows Professional, do those same steps, except both DOCKER_IP and DB_CLIENT_IP should be `localhost`.

#### Mac
Add the lines `export DOCKER_IP=localhost` and `export DB_CLIENT_IP=localhost` to your `~/.bashrc` file. If you haven't used your `.bashrc` file before, you may need to source it. To do so, add  
```
if [ -f ~/.bashrc ]; then  
   source ~/.bashrc  
fi  
```
to your `~/.bash_profile`.

#### Linux
Add the lines `DOCKER_IP=localhost` and `DB_CLIENT_IP=localhost` to `/etc/environment`. This file may be in a different location on some distros.

### Running Docker
If you are using Linux, all of the subsequent Docker commands in this guide must be run with `sudo`. If you would like to be able to use Docker without `sudo`, look through the answers [here](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo). You will also need to move your environment variables to your `~/.bashrc` file if you go this route.

Verify that Docker installed correctly with: `docker run hello-world`. You should see, "Hello from Docker!"

After setting the environment variables, close all terminals and every editor or process that's running Python. This is needed to ensure that your Python environment correctly reloads your environment variables.
The DOCKER_IP variable is necessary because the versions of Docker that run on VirtualBox generate an IP address that is dependent on the host's configuration,
so the code will read this variable to know where to make HTTP requests. The DB_CLIENT_IP variable is necessary because the client needs to run on 0.0.0.0 inside the Docker container,
which is the internal IP address that Docker containers use to communicate with each other, but it needs to run on localhost outside the container.

Open a Docker terminal on Windows Home, Powershell on Windows Professional, or a normal terminal otherwise, and `cd` into the Git repo. Run `docker-compose build` then `docker-compose up`.

Download Robo 3T from [here](https://robomongo.org/download) using the link on the right. You can use another MongoDB client if you'd prefer. When you start Robo 3T, a popup to configure connections should appear.
If you're on Windows Home, right click on the New Connection row and click "Edit". Change localhost to your Docker IP and hit "Save". Now press "Connect". Otherwise, leave the settings alone.
It should connect successfully and you should see a database called Clipboard on the pane on the right. The database should contain a collection called "event" and an index that includes the start and end timestamp, along with other field(s).

On Linux, you'll probably want to move the extracted Robo 3T folder to `/opt/your-extracted-folder-name` and run `sudo ln -s /opt/your-extracted-folder-name/bin/robo3t /usr/local/bin/robo3t`. Then you can run `robo3t` from the command line.

### Running scrapers
`cd` into the ClipboardApp repository. If you're using Anaconda, open up an Anaconda terminal and run `conda install --file anaconda-requirements-conda.txt` and `pip install -r anaconda-requirements-pip.txt`.
Otherwise, run `pip3 install -r requirements.txt`. Use `pip` instead of `pip3` if Python 3 is your default Python version. Now, run `python3 runner.py`. You should see data being sent to the output window.
When the program is finished running, go to your Robo 3T instance, right click on the "event" collection, and click "View Documents". The screen should populate with data.

For development, you'll want to open the `data_engine` folder in an IDE or text editor of your choice. Any editor should work as long as the `data_engine` folder is set as the base folder for the project.
This is important because the imports will not work if the base folder for the project is different.

## Development Guide
Our current development tasks and bugs are kept in the issues list [here](https://github.com/ClipboardProject/ClipboardApp/issues).  
The easiest way to learn the code base and get started contributing is to add a new scraper as defined in [this](https://github.com/ClipboardProject/ClipboardApp/issues/14) issue.  
The issue contains instructions on how to pick a specific site.

### Technical Overview
This project consists of four parts
- **Data Engine**:
This is the heart of the application. It asynchronously scrapes websites and pulls in data from APIs, cleans and formats the data, then sends it to the MongoDB client.

- **Database Client**:
This is a standalone service that receives data from the data engine for insertion into MongoDB and processes requests from the clipboard site to display data to the user.  
Any time data is received from a website, the old data from that site is deleted and refreshed with the new data.

- **MongoDB Instance**:
This holds a single collection of all data from the sites. Only the database client interacts with the database.

- **Clipboard Site**:
This is not integrated with the Clipboard App yet. Soon, this will be used to display all of the data gathered by the data engine.

### Getting Started
As stated previously, adding a scraper is the best way to start contributing. If you're not familiar with web scraping,
[this](https://www.upwork.com/hiring/for-clients/web-scraping-tutorial/) gives a decent overview about what web scraping is.
We're using Scrapy for this project, which is a complex and sophisticated web scraping framework. If you'd to start with a tutorial that will help you learn more about how to write a scraper without worrying about the complexities of Scrapy,
take a look at [this](https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/) guide which uses a library called BeautifulSoup.
If you're comfortable with the concepts used in web scraping, take a look at [this](https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/) tutorial.
Ignore the installation instructions because you should have installed Scrapy earlier in this guide.

#### Knowing when to use a scraper and when to use an API
Most websites that we're dealing with will need to be scraped because the data on them is statically loaded from the server as html. However, some sites use APIs to dynamically load data.
We should use these whenever possible because scrapers are fragile and need to be changed any time the content on the page changes. APIs are more stable and are less likely to have breaking changes introduced often.

Here is an example of how to detect if a site has an API we can use. 
1. Go to https://chipublib.bibliocommons.com/events/search/index in Google Chrome
2. Open the developer tools using F12 on Windows/Linux and Command+Option+I on Mac
3. Click on the "Network" tab at the top of the toolbox
4. Reload the page. The grid should be populated with data.
5. Click on the "Name" column for any of the requests. A detailed view should appear and the "Headers" tab should be selected.
6. Click on the "Response" tab. There could be a variety of data in here. This view can have a variety of data.  
    For resource requests like images, it will say there is no data available, javascript files will show the javascript code, css files will show the stylesheet, etc.
    The only response data we care about right now is json. 
7. Look for a request name that starts with "search?". Looking through the response, you should see a json object.
8. Click on the "Headers" tab. The Request URL is what was requested by your browser to retrieve the json data. We can use that same url to get that data in our application.
9. If you keep clicking through more requests, you should see several more that also returned json data.

[This](https://github.com/ClipboardProject/ClipboardApp/blob/master/data_engine/data_aggregators/apis/library_events.py) is the code that was used to create an API client for that site.  
You can use this as a guide if you need to create your own API client. Some sites have APIs that are well-documented and designed for external use. These should be used if they are available.

Some sites may provide an iCalendar feed. Try to use the [iCal reader](https://github.com/ClipboardProject/ClipboardApp/blob/master/data_engine/data_aggregators/apis/ical_reader.py) if it is possible to do so. 

### How to integrate new scrapers and API clients with the core code
All new scrapers should inherit from [SpiderBase](https://github.com/ClipboardProject/ClipboardApp/blob/master/data_engine/spider_base.py)
All new API clients should inherit from [ApiBase](https://github.com/ClipboardProject/ClipboardApp/blob/master/data_engine/api_base.py)

The end goal of all scrapers and API clients is to transform the raw data into event objects that conform to [this class](https://github.com/ClipboardProject/ClipboardApp/blob/master/data_engine/event.py).  
For each item, you'll want to parse out the following data (as much as is available). You'll notice that these fields correspond to the first parameter in the extract methods in `SpiderBase.py`.
- **`organization`**: The name of the organization that's putting on the event
- **`title`**: The name of the event
- **`description`**: Detailed description of the event
- **`address`**: Location of the event (okay if exact address is not known)
- **`url`**: Link to url for event. Link to specific event is preferred, but a link to a page containing general event listings is okay.
- **`price`**: Cost to attend, if provided
- **`category`**: Category of event, as defined [here](https://github.com/ClipboardProject/ClipboardApp/blob/master/data_engine/categories.py). (Work in progress. We'll flesh out categories more eventually)  
- **Start/End Time and Date**: Dates and times can be supplied with several parameters. Choose one date formate and one time format. Eventually, all dates and times will be converted into Unix timestamps.
    - **`time`**: Use if only one time is supplied for the event (not time range)
    - **`start_Time` and `End_Time`**: Use if the site supplies distinct data for these two values
    - **`time_Range`**: Use if the start and end time is supplied in a single string ex: 6:00-8:00 PM
    - **`date`**:  Use if the event could be one day or multiple days but it is contained in a single string. This is done this way because some sites have data that could be single days or multiple days.
    - **`start_date` and `end_date`**: Use if the site supplies distinct data for these two values
    - **`start_timestamp` and `end_timestamp`**: Use if the data is formatted like a Unix timestamp (Unlikely for scrapers but possible for an API)

Once you've decided how to find these fields for your site, look at the methods in `SpiderBase.py` or `ApiBase.py` and how they're used in existing spiders and API clients to see how to process the data.