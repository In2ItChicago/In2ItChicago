# In2It App

View these docs [here](https://clipboardproject.github.io/ClipboardApp/) if you like pretty colors.

## Table of Contents
 * [In2It App](readme.md#in2it-app)
      * [Setup](readme.md#setup)
         * [Get the Code](readme.md#get-the-code)
         * [Install Docker](readme.md#install-docker)
            * [Extra Installation Steps for Linux](readme.md#extra-installation-steps-for-linux)
            * [Extra Installation Steps for Windows](readme.md#extra-installation-steps-for-windows)
         * [Setting Up Docker](readme.md#setting-up-docker)
         * [Running the Code](readme.md#running-the-code)
         * [Setting up your development environment](readme.md#setting-up-your-development-environment)
         * [Settings](readme.md#settings)
            * [Command Line Arguments](readme.md#command-line-arguments)
            * [Other Settings](readme.md#other-settings)
      * [Development Guide](readme.md#development-guide)
         * [Technical Overview](readme.md#technical-overview)
         * [Getting Started](readme.md#getting-started)
            * [Knowing when to use a scraper and when to use an API](readme.md#knowing-when-to-use-a-scraper-and-when-to-use-an-api)
         * [How to integrate new scrapers and API clients with the core code](readme.md#how-to-integrate-new-scrapers-and-api-clients-with-the-core-code)

## Setup

### Get the Code
Clone the ClipboardApp repository into your preferred directory with Git Bash on Windows or a normal terminal otherwise: `git clone https://github.com/ClipboardProject/ClipboardApp.git`

### Install Docker
For Windows Home, download from [here](https://docs.docker.com/toolbox/toolbox_install_windows/). Documentation is [here](https://docs.docker.com/toolbox/overview/).  
For Windows Professional or Enterprise, download from [here](https://www.docker.com/docker-windows). Documentation is [here](https://docs.docker.com/docker-for-windows/).  
For Mac, download from [here](https://www.docker.com/docker-mac). Documentation is [here](https://docs.docker.com/docker-for-mac/).  
For Linux, download from your package manager. Documentation is [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/) (Other distros have links on the left side of the page).  
Make sure you follow any OS and distro-specific instructions for setting up Docker. It may be helpful to go through the getting started guide [here](https://docs.docker.com/get-started/).  

#### Extra Installation Steps for Linux (Ubuntu)
These steps are for Ubuntu. Arch Linux has Docker available in pacman without any manual steps required. Other distros may require different steps.

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
I was unable to get Kinematic to work on Docker Toolbox, so I would recommend skipping that. Make sure virtualization is enabled in the BIOS. If you need to change virtualization settings, do a full reboot cycle,
otherwise Windows may not report that the settings have changed. If you're running Windows 10 Professional, you'll need to make sure Hyper-V is enabled in the "Turn Windows Features On or Off" dialog.
If you're using Docker Toolbox on Windows Home edition, you'll want to start the VirtualBox instance manually before starting Docker every time or Docker will complain about not having an IP address.

Additionally, once Docker is installed, you'll need to tweak the VirtualBox settings slightly. Port forwarding must be configured manually to allow the host system to communicate with Docker over `localhost`
instead of `192.168.99.100`.
First, right click on the machine title "default" and select "Settings".
![Settings](images/settings.png?raw=true "Settings")

Once in the settings menu, select "Network" and then "Port Forwarding".
![Network](images/network.png?raw=true "Network")

Finally, click the green plus on the top right corner and add a new port forwarding rule. The new rule should be configured exactly like "Rule 1" in the following picture, but you can name it whatever.
This is the minimum amount of configuration needed for the application to work, but you can add the other ports used by the application later if you'd like to be able to connect to everything via `localhost`.
![PortForwaring](images/portforwarding.png?raw=true "Port Forwarding")

### Setting Up Docker
If you are using Linux, all of the subsequent Docker commands in this guide might have to be run with `sudo`. 
If you would like to be able to use Docker without `sudo`, look through the answers [here](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo). **If you're using Docker Toolbox on Windows Home, 
all subsequent statements that mention `localhost` should be replaced with `192.168.99.100`**. This is because the Docker engine can't bind to localhost when using Docker Toolbox.

Verify that Docker installed correctly with: `docker run hello-world`. You should see, "Hello from Docker!"

### Running the Code
The startup process runs a Python script to check if any docker images are out of date, so you will need python >=3.6 installed for that script to run properly. If you do not, it will throw an error,
but it won't affect the rest of the process, so this part can be skipped if you want.
If you're on Windows and do not have Python set up, you should install Anaconda from [here](https://www.anaconda.com/download/#windows/). During set up, you should check the box that says to add Python to your system path. 
If you do not, you'll need to add it to your path later. Without Python being accessible in the system path, Python commands won't be visible to terminals like the Docker Terminal or Git Bash. On Mac or Linux, you can install Python directly 
from your system's package manager. If your Python version is too old, I recommend using [pyenv](https://github.com/pyenv/pyenv) to manage your Python versions.

Once Python is set up, run `scripts/install.sh` from the root of the Github repo to install necessary Python dependencies.

Open a Docker terminal on Windows Home, Git Bash or some kind of bash emulator on Windows Professional, or a normal terminal otherwise, and `cd` into the Git repo. Run `./start.bash`. 
If you get a permissions error, you may need to run `chmod +x start.bash`. This will grant execution permissions to the file. 
If all goes well, the database will be created, the scrapers will start running, and the website will start up. This process will take some time.
Eventually, you should start seeing messages about events being saved. Once a message says `Data retrieved successfully`, the code is done running. 
Several components should be visible now:
- `localhost` and `localhost:3000` will show the site
- `localhost:5000/docs` will show a frontend for viewing the data and testing the API
- `localhost:9000` will show a frontend for managing the Docker containers. Create whatever username and password you want.

### Setting up your development environment

If you want to see more details about the data in the database, download NoSQL Booster from [here](https://nosqlbooster.com/downloads). You can use another MongoDB client if you'd prefer. Create a connection to `localhost:27017` and 
you should see the data show up. 

For debugging, we've set up configurations to allow for remote debugging in Docker using VS Code. This allows you to set breakpoints and step through code remotely while it's running in Docker.
You can use another editor if you'd like, but you'll have to set up remote debugging yourself. Whenever you open VS Code, it creates a directory called `.vscode` which stores local configurations.

This repo contains all of the components needed to run the system in separate folders:
- `clipboardapp/in2it_site` contains all code pertaining to the site itself
- `clipboardapp/event_processor` contains the web scrapers
- `clipboardapp/event_service` contains the API that the site and the event processor both call to interface with the database

When you're developing, you'll want to think of those folders as separate projects and open a separate instance of VS Code in each of those subdirectories. This is important because the remote debugger requires
the folder structure of the remote and local repository to match. To do so, you can launch VS Code, then choose `File -> Open Folder` or open it from the command line like this: `code ./in2it_site`. 

Once you have VS Code open, you should see a bug icon on the left panel. This contains the debugger settings. If you click the gear icon near the top right of the submenu, it will open a prompt to choose an environment.
It doesn't matter which one you choose because we'll overwrite this file in a minute. In this repo, there is a folder called `sample_vscode_config` with one config per component. Replace the entire `launch.json` file with
whatever config matches your current folder. As the comment in the files explain, you will need to replace `localhost` with `192.168.99.100` for Docker Toolbox. 
Once you have the configuration saved, you'll be able to select it from the debug menu. When you have the code running in Docker, click the green arrow to attach to the running process.

All of the code is running through a program called [nodemon](https://nodemon.io/) which allows you to use hot reloading while debugging. Hot reloading means that any time you change the source code in your editor,
nodemon will detect the change and automatically restart the attached process. This way, testing your changes requires no manual intervention.

### Settings
#### Command Line Arguments
The following parameters can be passed to `start.bash` to change its runtime behavior. 
- `-d or --processor-debug`:
This parameter is needed when using the debugger with the event processor. When passed in, `runner.py` will pause at the start of execution until you connect to it from the VS Code debugger.
This isn't needed by the other components because you can attach to a Node process without any special configuration.

- `-v or --verbose-output`
This tells scrapy to send verbose output to the logs. Otherwise, only errors will be displayed. Scrapy generates a lot of output so this is only useful when debugging odd behavior.

- `-s or --run-scheduler`
This tells the event processor to run the scrapers on a schedule (currently once a minute in dev and once every two hours in prod). It's easier to test without this flag since it will run them all at once
when this is not passed in.

#### Other Settings
The following settings are defined in `event_processor/config.py`:  

- **enable_api_cache**:
If `True`, any API calls made will be cached to a local file. This is useful to speed up development and to prevent hitting sites repeatedly.

- **api_cache_expiration**:
Time in seconds that API data will be cached for.

- **api_delay_seconds**:
The amount of time between API calls. This is used by calling `ApiBase.wait()`. This is necessary when making large amounts of API calls in quick succession so as not to overrun the server.

- **enable_scrapy_cache**:
If `True`, any Scrapy calls made will be cached using Scrapy's builtin cache system. This is useful to speed up development and to prevent hitting sites repeatedly.

- **scrapy_cache_expiration**:
Time in seconds that Scrapy data will be cached for.

## Development Guide
Our current development tasks and bugs are kept in the issues list [here](https://github.com/ClipboardProject/ClipboardApp/issues).  
The easiest way to learn the code base and get started contributing is to add a new scraper as defined in [this](https://github.com/ClipboardProject/ClipboardApp/issues/14) issue.  
The issue contains instructions on how to pick a specific site.

### Technical Overview
This project consists of four parts
- **Event Processor**:
This is the heart of the application. It asynchronously scrapes websites and pulls in data from APIs, cleans and formats the data, then sends it to the MongoDB client.

- **Event Service**:
This is a standalone service that receives data from the event processor for insertion into MongoDB and processes requests from the clipboard site to display data to the user.  
Any time data is received from a website, the old data from that site is deleted and refreshed with the new data.

- **MongoDB Instance**:
This holds a single collection of all data from the sites. Only the database client interacts with the database.

- **In2It Site**:
The website that displays the aggregated data. Interacts with the database via the database client.

### Getting Started
As stated previously, adding a scraper is the best way to start contributing. If you're not familiar with web scraping,
[this](https://www.upwork.com/hiring/for-clients/web-scraping-tutorial/) gives a decent overview about what web scraping is.
We're using Scrapy for this project, which is a complex and sophisticated web scraping framework. If you'd to start with a tutorial that will help you learn more about how to write a scraper without worrying about the complexities of Scrapy,
take a look at [this](https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/) guide which uses a library called BeautifulSoup.
If you're comfortable with the concepts used in web scraping, take a look at [this](https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/) tutorial.
Ignore the installation instructions because you should have installed Scrapy earlier in this guide.

Scrapy uses the CssSelect module to implement css selectors. Docs can be found [here](https://cssselect.readthedocs.io/en/latest/).
CssSelect defines its selectors according to the w3 specification [here](https://www.w3.org/TR/2011/REC-css3-selectors-20110929/) with a few exceptions that are listed in CssSelect's documentation.

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

[This](https://github.com/ClipboardProject/ClipboardApp/blob/master/event_processor/apis/library_events.py) is the code that was used to create an API client for that site.  
You can use this as a guide if you need to create your own API client. Some sites have APIs that are well-documented and designed for external use. These should be used if they are available.

Some sites may provide an iCalendar feed. Try to use the [iCal reader](https://github.com/ClipboardProject/ClipboardApp/blob/master/event_processor/apis/ical_reader.py) if it is possible to do so. 
Some sites may also provide an RSS feed. [This](https://github.com/ClipboardProject/ClipboardApp/blob/master/event_processor/apis/lwv_chicago.py) is an example of how to use the `feedparser` module to parse a feed.

### How to integrate new scrapers and API clients with the core code
All new scrapers should inherit from one of the classes listed [here](https://github.com/ClipboardProject/ClipboardApp/blob/master/event_processor/custom_spiders.py)
All new API clients should inherit from ApiSpider and scrapers should inherit from ScraperSpider or ScraperCrawlSpider, depending on if the spider needs to visit multiple urls or not.

The end goal of all scrapers and API clients is to transform the raw data into event objects that conform to the Event class in [this file](https://github.com/ClipboardProject/ClipboardApp/blob/master/event_processor/event.py).  
For each item, you'll want to parse out the following data (as much as is available). 
- **`organization`**: The name of the organization that's putting on the event
- **`title`**: The name of the event
- **`description`**: Detailed description of the event
- **`address`**: Location of the event (okay if exact address is not known)
- **`url`**: Link to url for event. Link to specific event is preferred, but a link to a page containing general event listings is okay.
- **`price`**: Cost to attend, if provided
- **`category`**: Category of event, as defined [here](https://github.com/ClipboardProject/ClipboardApp/blob/master/event_processor/categories.py). (Work in progress. We'll flesh out categories more eventually)  
- **Start/End Time and Date**: Dates and times can be supplied with several parameters. Choose one date formate and one time format. Eventually, all dates and times will be converted into Unix timestamps.
    - **`time`**: Use if only one time is supplied for the event (not time range)
    - **`start_Time` and `End_Time`**: Use if the site supplies distinct data for these two values
    - **`time_Range`**: Use if the start and end time is supplied in a single string ex: 6:00-8:00 PM
    - **`date`**:  Use if the event could be one day or multiple days but it is contained in a single string. This is done this way because some sites have data that could be single days or multiple days.
    - **`start_date` and `end_date`**: Use if the site supplies distinct data for these two values
    - **`start_timestamp` and `end_timestamp`**: Use if the data is formatted like a Unix timestamp (Unlikely for scrapers but possible for an API)

Once you've decided how to find these fields for your site, look at the existing examples to see what methods to use to extract the data.
