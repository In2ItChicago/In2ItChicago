# In2It Chicago

View these docs [here](https://in2itchicago.github.io/In2ItChicago/) if you like pretty colors.

## Table of Contents

- [In2It Chicago](#in2it-Chicago)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Get the Code](#get-the-code)
    - [Install Docker](#install-docker)
      - [Extra Installation Steps for Linux (Ubuntu)](#extra-installation-steps-for-linux-ubuntu)
      - [Extra Installation Steps for Windows](#extra-installation-steps-for-windows)
    - [Setting Up Docker](#setting-up-docker)
    - [Running the Code](#running-the-code)
    - [System Architecture](#system-architecture)
    - [Setting up your development environment](#setting-up-your-development-environment)
    - [Configuring pgAdmin](#configuring-pgadmin)
    - [Settings](#settings)
      - [Command Line Arguments](#command-line-arguments)
      - [Other Settings](#other-settings)
    - [Scheduler](#scheduler)
  - [Development Guide](#development-guide)
    - [Technical Overview](#technical-overview)
    - [Detailed Docs](#detailed-docs)
    - [Getting Started](#getting-started)
      - [Tutorials](#tutorials)
      - [Knowing when to use a scraper and when to use an API](#knowing-when-to-use-a-scraper-and-when-to-use-an-api)
    - [How to integrate new scrapers and API clients with the core code](#how-to-integrate-new-scrapers-and-api-clients-with-the-core-code)
  - [Troubleshooting Guide](#troubleshooting-guide)
  - [Deployment](#deployment)

## Setup

### Get the Code

Clone the In2ItChicago repository into your preferred directory with Git Bash on Windows or a normal terminal otherwise: `git clone https://github.com/In2ItChicago/In2ItChicago.git`

If you have any issues, see the troubleshooting guide further down in this document.

### Install Docker

Note: If you're running Windows Professional, it's recommended you use Docker for Windows over Docker Toolbox. This requires the use of Hyper-V, while Docker Toolbox requires the use of VirtualBox.
Keep in mind that if you're currently using VirtualBox, you can't use Hyper-V at the same time. Make sure you disable one before trying to use the other.

For Windows Home, download the latest version from [here](https://github.com/docker/toolbox/releases). Documentation is [here](https://docs.docker.com/toolbox/overview/).  
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
Verify that the Key Fingerprint line shows: 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88

Set up the stable Docker repository:  
`sudo add-apt-repository \ "deb [arch=amd64] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) \ stable"`
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

I was unable to get Kitematic to work on Docker Toolbox, so I would recommend skipping that. Make sure virtualization is enabled in the BIOS. If you need to change virtualization settings, do a full reboot cycle,
otherwise Windows may not report that the settings have changed. If you're running Windows 10 Professional, you'll need to make sure Hyper-V is enabled in the "Turn Windows Features On or Off" dialog.
**IMPORTANT: If you're using Docker Toolbox on Windows Home edition, you'll want to start the VirtualBox instance manually before starting Docker every time or Docker will complain about not having an IP address.**

Additionally, once Docker is installed, you'll need to tweak the VirtualBox settings slightly. Port forwarding must be configured manually to allow the host system to communicate with Docker over `localhost`
instead of its defualt IP of `192.168.99.100`.
First, right click on the machine title "default" and select "Settings".
![Settings](images/settings.png?raw=true 'Settings')

Once in the settings menu, select "Network" and then "Port Forwarding".
![Network](images/network.png?raw=true 'Network')

Finally, click the green plus on the top right corner and add a new port forwarding rule. The new rule should be configured exactly like "Rule 1" in the following picture, but you can name it whatever.
This is the minimum amount of configuration needed for the application to work, but you can add the other ports used by the application if you'd like to be able to connect to everything via `localhost`. Other ports used by this application are `3000`, `9000`, `5000`, `7000`, and `6800` if you would like to add those now.
![PortForwaring](images/portforwarding.png?raw=true 'Port Forwarding')

### Setting Up Docker

If you are using Linux, all of the subsequent Docker commands in this guide might have to be run with `sudo`.
If you would like to be able to use Docker without `sudo`, look through the answers [here](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo). **If you're using Docker Toolbox on Windows Home,
all subsequent statements that mention `localhost` should be replaced with `192.168.99.100` unless you set up port forwarding for all of the ports mentioned in the previous step**.

Verify that Docker installed correctly with: `docker run hello-world`. You should see, "Hello from Docker!"

### Running the Code

Open a Docker terminal on Windows Home, Git Bash or some kind of bash emulator on Windows Professional, or a normal terminal otherwise, and `cd` into the Git repo. If on Windows, it's probably a good idea to run `scripts/fix-bad-characters.bash` first because Docker behaves strangely when Windows-specific characters are sent to it. You may need to run this again in the future if more Windows characters make it into your files.

Now, run `./start.sh`. If you get a permissions error, you may need to run `chmod +x start.sh`. This will grant execution permissions to the file.
If all goes well, the database will be created, the scrapers will start running, and the website will start up. This process will take some time.
Eventually, you should start seeing messages about events being saved. Once a message says `Data retrieved successfully`, the code is done running.
On subsequent runs, you can run `light-start.sh` instead of `start.sh`. This will skip all of the steps except for just building and running the containers. If you run into any errors while running `light-start.sh`, try running `start.sh` again to clear out any bad cached data.

Several components should be visible now:

- `localhost` and `localhost:3000` will show the site
- `localhost:5000/docs` will show a frontend for viewing the data and testing the API
- `localhost:9000` will show a frontend for managing the Docker containers. Create whatever username and password you want.
- `localhost:7000` will show a frontend for managing the Postgres database. The username is `user@domain.com` and the password is `pgadmin`. Instructions on how to connect to the database will be given later in this document.

### System Architecture

![System Architecture](images/In2ItArchitecture.png?raw=true 'System Architecture')

### Setting up your development environment

For debugging, we've set up configurations to allow for remote debugging in Docker using VS Code. This allows you to set breakpoints and step through code remotely while it's running in Docker.
You can use another editor if you'd like, but you'll have to set up remote debugging yourself. Whenever you open VS Code, it creates a directory called `.vscode` which stores local configurations.

This repo contains all of the components needed to run the system in separate folders:

- `in2it_site` contains all code pertaining to the site itself
- `event_processor` contains the web scrapers
- `event_service` contains the API that the site and the event processor both call to interface with the database

When you're developing, you'll want to think of those folders as separate projects and open a separate instance of VS Code in each of those subdirectories. This is important because the remote debugger requires
the folder structure of the remote and local repository to match. To do so, you can launch VS Code, then choose `File -> Open Folder` or open it from the command line like this: `code ./in2it_site`.

Once you have VS Code open, you should see a bug icon on the left panel. This contains the debugger settings. If you click the gear icon near the top right of the submenu, it will open a prompt to choose an environment.
It doesn't matter which one you choose because we'll overwrite this file in a minute. In this repo, there is a folder called `sample_vscode_config` with one config per component. Replace the entire `launch.json` file with
whatever config matches your current folder. As the comment in the files explains, you will need to replace `localhost` with `192.168.99.100` for Docker Toolbox.
Once you have the configuration saved, you'll be able to select it from the debug menu. When you have the code running in Docker, click the green arrow near the top left of VS Code to attach to the running process.

All of the code is running through a program called [nodemon](https://nodemon.io/) which allows you to use hot reloading while debugging. Hot reloading means that any time you change the source code in your editor,
nodemon will detect the change and automatically restart the attached process. This way, testing your changes requires no manual intervention. You can try it by pressing `CTRL + S` on any source code file while the code is running.

You do not need to have python or node running locally for development since it is running in Docker, but it may help to have local installations to help with autocomplete and linting while developing. See [python for VS Code](https://code.visualstudio.com/docs/languages/python) and [node for VS Code](https://code.visualstudio.com/docs/nodejs/nodejs-tutorial).

### Configuring pgAdmin

This is an optional step to view what's going on with the database. This doesn't need to be done immediately, but it may be useful for debugging if things aren't working as expected.

This step must be done while the code is running and after the database has been initialized (1-2 minutes after the first startup).

Go to pgAdmin at `locahost:7000` and sign in with username `user@domain.com` and password `pgadmin`.
On the left pane, right click on the node called `Servers` and create a new one as shown below.

![Create Server](images/CreateServer.png?raw=true 'Create Server')

Enter whatever name you want for the server. I choose `postgres` because I'm boring.

![Choose Name](images/ChooseName.png?raw=true 'Choose Name')

Now, set up the conenection properties. You should enter the properties exactly as shown in the image. The password is `postgres`.

![Create Connection](images/CreateConnection.png?raw=true 'Create Connection')

If your database was created successfully, you should see three databases in the left pane now: `events`, `postgres`, and `scheduler`.

### Settings

#### Command Line Arguments

The following parameters can be passed to `start.bash` to change its runtime behavior.

- `-d or --processor-debug`:
  This parameter is needed when using the debugger with the event processor. When passed in, the event processor will pause at the start of execution until you connect to it from the VS Code debugger.
  This isn't needed by the other components because you can attach to a Node process without any special configuration.

- `-v or --verbose-output`
  This tells scrapy to send verbose output to the logs. Otherwise, only errors will be displayed. Scrapy generates a lot of output so this is only useful when debugging odd behavior.

- `-s or --run-scheduler`
  This tells the event processor to run the scrapers on a schedule (currently once a minute in dev and once every two hours in prod). More information about the scheduler will be discussed in a subsequent section.

- `-c or --scheduler-debug`
  This is the same behavior as `-d` but for the scheduler. More information about the scheduler will be discussed in a subsequent section.

- `-n or --spider-name`
  Example: `./start.sh -n library`. Only run the specified spider instead of all of them. Must match the `name` variable that's defined on the spider class. No effect when used with `-s`.

- `-p or --profile-queries`
  Log all sql queries to the console along with the execution time.

- `service names`
  Example: `./start.sh -v -n library event_service event_processor postgres`. Trailing keywords indicate which docker services to start if you do not want to start all of them.

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

### Scheduler

We've forked a project from Nextdoor called ndscheduler to use as a scheduling system for this project.
To run the scheduler with this application, the scheduler repository must be checked out into the same parent folder as this one.

To use, run `cd {parent directory of the directory you cloned this repository into}` and `git clone https://github.com/In2ItChicago/ndscheduler`. The startup scripts in this repository check for the existence of the ndscheduler folder when running. Once this is completed, go back to the `In2ItChicago` folder and run `./start.sh -s` to start the application with the scheduler.

If all goes well, you should be able to navigate to `localhost:8888` and see the scheduler. From there, you can let the scrapers run on a schedule or run them manually with the UI. `localhost:6800` is the url for scrapyd, which is the middleman between the scrapers and ndscheduler.

## Development Guide

**IMPORTANT: If you're using Windows, please run `git config --global core.autocrlf input` before committing anything. This prevents carriage returns from getting sent to the remote repository.**

Our current development tasks and bugs are kept in the issues list [here](https://github.com/In2ItChicago/In2ItChicago/issues).  
The easiest way to learn the code base and get started contributing is to add a new scraper as defined in [this](https://github.com/In2ItChicago/In2ItChicago/issues/14) issue.  
The issue contains instructions on how to pick a specific site.

### Technical Overview

This project consists of four parts

- **Event Processor**:
  This is the heart of the application. It asynchronously scrapes websites and pulls in data from APIs, cleans and formats the data, then sends it to the event service.

- **Event Service**:
  This is a standalone service that receives data from the event processor for insertion into MongoDB and processes requests from the site to display data to the user.  
  Any time data is received from a website, the old data from that site is deleted and refreshed with the new data.
  Detailed documentation can be found [here](docs/event_service)

- **PostgreSQL Instance**:
  This holds a single collection of all data from the sites. Only the database client interacts with the database.

- **In2It Site**:
  The website that displays the aggregated data. Interacts with the database via the database client.
  Detailed documentation can be found [here](docs/in2it_site)

- **ndscheduler**:
  Optional scheduling system to run scrapers periodically.

- **scrapyd**
  ndscheduler calls this to request scraper runs. Once a scraper is requested, scrapyd will start the scraper when resouces become available.

### Detailed Docs

- [Event Processor](https://In2ItChicago.github.io/In2ItChicago/docs/event_processor)
- [Event Service](https://In2ItChicago.github.io/In2ItChicago/docs/event_service)
- [In2It Site](https://In2ItChicago.github.io/In2ItChicago/docs/in2it_site)

### Getting Started

As stated previously, adding a scraper is the best way to start contributing.
We're using Scrapy for this project, which is a complex and sophisticated web scraping and crawling framework.
Check out the below tutorials for some introductions to web scraping and Scrapy.

#### Tutorials

- [Basics concepts of web scraping](https://www.upwork.com/hiring/for-clients/web-scraping-tutorial/)
- [Basic web scraping with Python](https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/)
- [More advanced web scraping/crawling with Scrapy](https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/)
- [Adding a scraper to our codebase](https://In2ItChicago.github.io/In2ItChicago/tutorial/scraperTutorial.html)

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

[This](https://github.com/In2ItChicago/In2ItChicago/blob/master/event_processor/apis/library_events.py) is the code that was used to create an API client for that site.  
You can use this as a guide if you need to create your own API client. Some sites have APIs that are well-documented and designed for external use. These should be used if they are available.

Some sites may provide an iCalendar feed. Try to use the [iCal reader](https://github.com/In2ItChicago/In2ItChicago/blob/master/event_processor/apis/ical_reader.py) if it is possible to do so.
Some sites may also provide an RSS feed. [This](https://github.com/In2ItChicago/In2ItChicago/blob/master/event_processor/apis/lwv_chicago.py) is an example of how to use the `feedparser` module to parse a feed.

### How to integrate new scrapers and API clients with the core code

All new scrapers should inherit from one of the classes listed [here](https://github.com/In2ItChicago/In2ItChicago/blob/master/event_processor/custom_spiders.py)
All new API clients should inherit from ApiSpider and scrapers should inherit from ScraperSpider or ScraperCrawlSpider, depending on if the spider needs to visit multiple urls or not.

The end goal of all scrapers and API clients is to transform the raw data into event objects that conform to the Event class in [this file](https://github.com/In2ItChicago/In2ItChicago/blob/master/event_processor/event.py).  
For each item, you'll want to parse out the following data (as much as is available).

- **`organization`**: The name of the organization that's putting on the event
- **`title`**: The name of the event
- **`description`**: Detailed description of the event
- **`address`**: Location of the event (okay if exact address is not known)
- **`url`**: Link to url for event. Link to specific event is preferred, but a link to a page containing general event listings is okay.
- **`price`**: Cost to attend, if provided
- **`category`**: Category of event, as defined [here](https://github.com/In2ItChicago/In2ItChicago/blob/master/event_processor/categories.py). (Work in progress. We'll flesh out categories more eventually)
- **Start/End Time and Date**: Dates and times can be supplied with several parameters. Choose one date formate and one time format. Eventually, all dates and times will be converted into Unix timestamps.
  - **`time`**: Use if only one time is supplied for the event (not time range)
  - **`start_time` and `end_time`**: Use if the site supplies distinct data for these two values
  - **`time_Range`**: Use if the start and end time is supplied in a single string ex: 6:00-8:00 PM
  - **`date`**: Use if the event could be one day or multiple days but it is contained in a single string. This is done this way because some sites have data that could be single days or multiple days.
  - **`start_date` and `end_date`**: Use if the site supplies distinct data for these two values
  - **`start_timestamp` and `end_timestamp`**: Use if the data is formatted like a Unix timestamp (Unlikely for scrapers but possible for an API)

Once you've decided how to find these fields for your site, look at the existing examples to see what methods to use to extract the data.

## Troubleshooting Guide

**Weird errors are occuring when I start up the code**

- First of all, try it at least two or three times. Docker tries to start all services simultaneously and occassionally things just get stuck in a weird state.

- This could obviously be caused by many things, but the common cause of most errors are bad characters in files (on Windows) or bad cache data. Docker can behave strangely sometimes when Windows-specific characters are sent into it. The first thing to try on Windows when weirdness occurs is to run `scripts/fix-bad-characters.bash`. To reduce the chance of this being needed, you can change VS Code's line ending behavior to use only line feed instead of carriage return + line feed. More information on this [here](https://stackoverflow.com/questions/39525417/visual-studio-code-how-to-show-line-endings).

- If bad characters aren't the problem, you can clean up your docker system. First run `docker-compose down` to make sure no containers are running, then run `docker system prune`.
  If that isn't enough, deleting the image of the offending service may be needed. `docker image rm {image name}` will do that. If that doesn't work, you can delete the volume associated with an image by running `docker volume rm {volume name}`. If you don't feel like figuring out which service is causing the issue, `docker system prune -a` will wipe out all images, and `docker volume prune` will wipe out all volumes. Keep in mind that volumes are what stores persistent data so be careful about data loss.

**Services aren't restarting properly with nodemon after saving**

- Sometimes nodemon restarts the service too quickly and doesn't allow time for ports to deallocate before reallocating them. Give it a kick by hitting `CTRL + S` on a source file one or two more times and it should start properly. This is a bug that we hope to resolve sometime soon-ish.

**Docker says that it can't start because ports are already allocated**

- You may have old containers running that weren't stopped previously. Run `docker-compose down` to stop them, or if that doesn't work, stop them manually one by one. If that doesn't work. Other applications may be using those ports and must be stoppped first.

**When starting Docker on Windows, it complains about not having an IP address**

- The VirtualBox VM will likely need to be started manually every time before starting Docker because it takes too long to start up and Docker times out while waiting for it.

**VS Code is complaining about missing dependencies/modules/etc**

- VS Code is only looking at your local system, not what's in Docker. To get rid of the warnings and enable autocomplete, linting, etc, install all of the python/node dependencies on your local machine.

## Deployment

This describes how to deploy the application to the production server. All the following commands assume your current working directory is the root of the repo. Before you do this, you will neeed both an SSH key for the server and the Dockerhub passsword. Ask a member with push access for these.

First, run `deploy/tag-images.sh` with a version number appended to the end. Our current version number scheme is YYYYMMDD.{REVISION}. EX: `deploy/tag-images.sh 20190723.1`. The revision number can be incremented if more than one deployment is done in a day. This will build the production version of the images, tag them, and save them locally on your computer.

Next, open up `docker-compose.prod.yml` and update all of the image versions to point to the new tag. If not all of the images were changed, not all of the tags need to be updated, but we prefer that all of the images get versioned together as that will make it easier to keep everything in sync.

Now, run `./start-prod.sh` and test to make sure everything is working locally.

Once tested, you can push the images to Dockerhub. Before doing this the first time, you have to run `deploy/login.sh` in order to obtain access to push to Dockerhub. Before doing that, you will need to have `dockerhub_in2itchicago.txt` inside your `deploy` folder.

Once logged in, run `deploy/publish-images.sh 20190723.1` to push the images to Dockerhub (replace the version number with the one you used in the earlier step). This will take a few minutes depending on the extent of the changes. Dockerhub does a diff with the current published image to see what needs to be pushed.

After a successful push, you're ready to deploy to the server. First, commit your changes to `docker-compose.prod.yml` so they can be picked up by the server. Then, run `deploy/vultr_deploy.sh`. For this to work, you need to have the ssh private key installed on your computer at `~/.ssh/id_rsa`.

After the deploy script finishes, you can run `deploy/connect_ports.sh`. This will set up port forwarding to the remote server so you can monitor the applications from your local computer. If anything goes awry, you can use `deploy/ssh_vultr.sh` to SSH into the server.
