![logo](/extras/logo.png)

Active reconaissance, information gathering and OSINT built in a portable web application

[![Build Status](https://travis-ci.org/ex0dus-0x/D0xk1t.svg)](https://travis-ci.org/ex0dus-0x/D0xk1t)

![screenshot](/extras/screenshot.png)

### CHANGELOG

11/24/17

* Added YAML support for Dox
* Added DNS Enumeration
* Refactored code, added comments
* Jinja filters for more intuitive interactions

#### TODO:

* Add webNmap function
* Change screenshot / wallpaper
* Cut down HTML templating

---

## 1.0 Introduction

1. __What is this?__

D0xk1t is an __open-source__, __self-hosted__ and __easy to use__ OSINT and active reconaissance web application for penetration testers. Based off of the prior command-line script, D0xk1t is now fully capable of conducting reconaissance and penetration testing for security researchers who need a framework without the 
head-scratching.

2. __Is this a website / webapp ?__

Yes and no. In essence, it is not a typical website. D0xk1t is self-hosted. There is no server stack, cloud-based service, SaaS, etc. that is holding it up. You can have the option of deploying D0xk1t on a local network, or deploying
your own instance on any infrastructure / technology as you wish (although not recommended).

3. __Is this free ?__

Yes. D0xk1t will forever be open-source. If you wish to contribute, you can make a fork, add any changes, and send a pull request on Github.

4. __How else can I develop on this?__

I have created API endpoints, and more will be coming soon.

---

## 2.0 Features

* Easy-to-build, risk-free installation
* Simple Bootstrap Admin Dashboard
* Deployable to the Internet
* Serverless (at the moment)
* Expansive to any OS

---

## 3.0 Installation 

Since D0xk1t is self-hosted, it does not work immediately out-of-box. It is recommended that you use a `virtualenv` container due to the sheer number of dependencies that can run into conflict with your Python configuration.

### 3.1 Building

Lucky for you, there are two ways to build D0xk1t. The __quick 'n easy way__, and the __manual way__.

__Quick 'n Easy Way:__

     $ curl https://raw.githubusercontent.com/ex0dus-0x/D0xk1t/master/extras/install | sudo /bin/bash 

__Manual Way:__

    $ git clone https://github.com/ex0dus-0x/D0xk1t && cd D0xk1t
    $ # Start virtualenv if you wish
    $ pip install -r requirements.txt
    $ python run.py

### 3.2 Configuration

Open `config.py`. Here, you will see all the environmental variables that the application utilizes. Three important fields you __MUST__ be aware of if you plan to deploy to the web.

    GOOGLEMAPS_API_KEY = "YOUR_API_KEY_HERE"

    SECRET_KEY = 'SECRET_KEY_HERE'
    
`GOOGLEMAPS_API_KEY` denotes the Google Maps API Key. This is essential for the GeoIP module. You can obtain it [here](https://developers.google.com/maps/) and change the variable accordingly.

`SECRET_KEY` is the private key utilized by WTForm's CSRF protection feature. If deployed, change it to your liking.

### 3.3 Deployment

Once installed, run with `python run.py`. The application will run a first-time boot, and will then be accessible at `127.0.0.1:5000`. 

Of course, this is self-hosting on localhost. Although work-in-progress, D0xk1t will soon support hosting on a variety of SaaS and server stacks of your choice.

* [Heroku](https://www.heroku.com/) - __TODO__: build a `Procfile`, as well as bash scripts for automatic deployment
* [ngrok](https://ngrok.com/) - __TODO__: build a script for deployment to ngrok

---

## 4.0 Modules

#### D0x Module

The D0x module is a comprehensive info-gathering database that enables the pentester to write "D0x", or a file that holds a collection of data of a certain target, or targets.
Using this data, the tester will be able to effectively understand their target, which is a critical point in the attacker's kill chain. D0xing is usually deemed malicious and black-hat in nature. However, with the D0x module, we aim to help security researchers gain momentum when conducting in-the-field pentesting. 

The D0x module does come with several features, improved upon based off of the prior revision. 

* Secure database support, with delete and export (as `.csv`) options

#### GeoIP Module 

When working with metadata, IP addresses often pop up as a point-of-interest. Using Maxmind and Google Map's APIs, the GeoIP module aims to collect geolocation information on public IP addresses, in order to gather data on physical location during
the reconaissance stage of the killchain.

* Google Maps support for accurate GeoIP visualization
* API endpoint support for command-liners or developers.

### DNS Enumeration Module

Targets, whether it be a company or a person, may utilize domains in order to display web content. Domains, especially those that are not properly configured, give penetration testers great opportunity to gather sensitive information in the
form of metadata, whether it be an address from a WHOIS lookup, or nameservers.

---

## 5.0 How to Contribute

Contributing is easy! Send a pull request if you feel that anything should be changed, removed, optimized, etc. Issues are also great for reporting bugs. 

# License

D0xk1t is distributed under a [MIT  License](https://choosealicense.com/licenses/mit/).
