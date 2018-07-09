# Home Assistant Configuration

Home Assistant is an open-source home automation platform running on Python 3. Track and control all devices at home and automate control.  
I have mine running on with HASSIO on a Raspberry Pi 3, but will be integrating it into a Docker Service across a Swarm of 6 Pi's for redundancy in future iterations. This repository represents my configuration files to make my Home Automation magic happen. I run a CICD pipeline w/ Travis CI successes being pushed to my 'production Pi'.

[![Master Build Status](https://travis-ci.org/mrreyes512/HomeAssistant.svg?branch=master)](https://travis-ci.org/mrreyes512/HomeAssistant)

![My Home Assistant Layout](www/layout-Smarthome.png)

## Home Assistant Components Used

| **CONTROLLED COMPONENTS** | **INPUT COMPONENTS** | **NOTIFICATION COMPONENTS** | **MEDIA COMPONENTS** |
|---|----|---|---|
| ![Philips Hue][philips_hue] | ![Google Home][google_home] | Slack | Google Chromecast |
| ![Vera][vera] | IFTTT | Pushbullet | Apple TV |
| ![Rachio][rachio] | Netamo | Cisco Webex Teams | |
| Arduino | | | |

[philips_hue]: www/logo-Hue.png
[vera]: www/logo-Vera.png
[rachio]: www/logo-Rachio.png

[google_home]: www/logo-Google_Assistant.png

## Routines
Routines are designed to move with your life flow. They are made to meet the day to day needs to interact with your house.
Examples could be thought of as: I'm out of bed and need to:
* Turn on my normal morning lights
* Make Coffee
* Wake the kids
* Listen to the news

For my configuration, I'm using a conversation with Google Home to execute the below:

| TITLE | HOW TO EXECUTE | DESCRIPTION |
|---|---|---|
| Morning | I'm up / Good Morning | Execute Morning Automation |
| Going to bed | I'm going to bed | Execute Goodnight Automation |
| In Bed | I'm in bed / Goodnight | Execute **INSIDE LIGHTS OFF** Scene
| Fresca Hours | Sandra's still working | Execute **FRESCA SCENE** |
| Leaving | I'm leaving | Turn all lights off, set Upstairs and Downstairs to 85 |

## Scenes
Scenes can be thought of as a static snapshot to set a mood. You can use them at times when you need a specific group of lights to be on. Another use is that it may be too dark in the house due to an overcast. These could also be used when trying to view a Movie, or set a Holiday mood.

| TITLE | DESCRIPTION |
|---|---|
| Morning Scene | Set morning lights |
| Goodnight Scene | Turn off all **INSIDE LIGHTS** except MASTER |
| Inside Lights  | Toggle of **INSIDE LIGHTS** |
| Outside Lights | Toggle of **OUTSIDE LIGHTS** |
| Fresca Scene | Turn off all **INSIDE LIGHTS** except FRESCA Lamp |

## Automations and Triggers
Automations are a blend of a Routine and a static Scene. A morning Routine could trigger the _Morning Lights Scene_ **PLUS** make you coffee **AND** wake the kids! Or, a trigger could be considered to turn on the _Inside Lights Scene_ 30 minutes prior to sunset, and turn off 30 minutes before sunrise.

| TITLE | TRIGGER | DESCRIPTION |
|---|---|---|
| Auto Lights | -30m Sunset | Turn on **INSIDE LIGHTS** |
| Evening Lights | +10m Sunset | Turn on **OUTSIDE LIGHTS** |
| Sunrise Lights | -30m Sunrise | Turn off **OUTSIDE LIGHTS** |
| Morning | Morning Routine | **MORNING SCENE**, Boil water kettle, Broadcast: "Good Morning", Play the news in the Master |
| Goodnight | G2B Routine | **GOODNIGHT SCENE**, Turn off TV, Broadcast: "Goodnight" |

## Inspiration and Support

- [Instagraeme](https://github.com/Instagraeme/Home-Assistant-Configuration/raw/master/HomeAssistant.gif)
- [Dale3h](https://github.com/dale3h/homeassistant-config)
- [Teagan42](https://github.com/Teagan42/HomeAssistantConfig)
- [CBulock](https://github.com/cbulock/home-assistant-configs)
- [chrom3](https://github.com/chrom3)

Thanks to all the people in the [gitter](https://gitter.im/home-assistant/home-assistant) community for listening and help

And thanks to *all* the devs that create the Home Assistant magic
