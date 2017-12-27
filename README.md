# Home Assistant Configuration 

|  |  |
| --- | --- |
| **Build** | [![Master Build Status](https://travis-ci.org/mrreyes512/HomeAssistant.svg?branch=master)](https://travis-ci.org/mrreyes512/HomeAssistant) |
| **Last Commit** | [![GitHub last commit](https://img.shields.io/github/last-commit/google/skia.svg)]() | 

My [Home Assistant](https://home-assistant.io/) Configuration Files

## Devices

- Vera
- Google Chromecast
- Apple TV
- Rachio


### Google Assistant Integration
> For a full walkthrough reference [HomeAssistant.io](https://home-assistant.io/components/google_assistant/)

The below process are brief notes used to set up my Google Assistant Integration with Home Assistant
  
  + Home Assistant Configuration
    1. Enable the `google_assistant` component in your [HA config](configuration.yaml) file
    2. Choose which components to expose from HA to GA
      - I chose to expose Lights, Scenes, and Climate Control.
    3. Test config and **reset HA Service**, this will enable the GA API into HA
  + Home Assistant -to- Google Assistant
    1. Download [gactions CLI](https://developers.google.com/actions/tools/gactions-cli) in your [bin directory](bin)
    2. Create a new `project.json` file following the [HA Guide](https://home-assistant.io/components/google_assistant/).
        This will be used to generate a secret for the Google project in the preceding step. 
    3. Create a new Google Developer Project through the [Developer Console](https://console.actions.google.com/u/0/).
    4. Link your Environment via the gactions: (my evn is a Pi, your env could be a docker or virtPython) 
      - `cd bin; chmod +x gactions`
      - `./gactions update --action_package project.json --project YourProjectName-2d0b8`
      - The `gactions` script will pause and issue a url to authenticate against your Google ID. Once you open the link in a browser, it will give you a key to continue with the `gactions` script.
      - You should now notice a `creds.data` file is now created in the [bin directory](bin). This is specific key between your environment and the Google Project.
    5. Finish out the required Account Linking within your Google Project following the [HA Guide](https://home-assistant.io/components/google_assistant/).
      - This step is rather lengthy. 
      - Ensure your **Authorization URL** has the proper URL: `https://[site.com]:8123/api/google_assistant/auth`
    6. Look for the **TEST DRAFT** button, once you're project is in the *testing* phase, you should be able to add your project on your phone's Google Assistant by:
      - Google Assistant > Settings > Home Control > Add Devices(+)
      - look for: `[test] ProjectName`
      - Once selected, you should start to see the devices that you allowed GA to know about from the Home Assistant configuration section above.
        > ga_project_id:  project-id\
          ga_client_id:   long-string (used in GProject > Account linking > Client ID)\
          ga_token:       this-is-a-token (random token)\
          ga_user:        user (used for request_sync services)\
          ga_api:         api-key (used for request_sync services)
  + New Environment Setup
    1. Download [gactions CLI](https://developers.google.com/actions/tools/gactions-cli)
    2. Create a new `project.json`
    3. Link new env: `./gactions update --action_package project.json --project YourProjectName-2d0b8`
    4. Unlink - Relink within Google Assistant phone app (step 6 above).
  + Google Assistant devices refresh after HA change
    1. Test HA config / Restart HA service
    2. Select your app in [Google Console](https://console.actions.google.com/u/0/).
    3. Press **TEST DRAFT** to resync GA -to- HA
    4. Unlink / Relink your [test] App on Google Assistant in your phone. 

## Inspiration and Support

- [Instagraeme](https://github.com/Instagraeme/Home-Assistant-Configuration/raw/master/HomeAssistant.gif)
- [Dale3h](https://github.com/dale3h/homeassistant-config) 
- [Teagan42](https://github.com/Teagan42/HomeAssistantConfig)
- [CBulock](https://github.com/cbulock/home-assistant-configs)
- [chrom3](https://github.com/chrom3)

Thanks to all the people in the [gitter](https://gitter.im/home-assistant/home-assistant) community for listening and help

And thanks to *all* the devs that create the Home Assistant magic
