# Home Assistant Configuration 

| **Master Build** | **Develop Build** |
| --- | --- |
| [![Master Build Status](https://travis-ci.org/mrreyes512/HomeAssistant.svg?branch=master)](https://travis-ci.org/mrreyes512/HomeAssistant) | [![Master Build Status](https://travis-ci.org/mrreyes512/HomeAssistant.svg?branch=develop)](https://travis-ci.org/mrreyes512/HomeAssistant) |
| [![GitHub last commit (master)](https://img.shields.io/github/last-commit/google/skia/infra/config.svg)](https://github.com/mrreyes512/HomeAssistant/) | [![GitHub last commit (develop)](https://img.shields.io/github/last-commit/google/skia/infra/config.svg)](https://github.com/mrreyes512/HomeAssistant/tree/develop) |

My [Home Assistant](https://home-assistant.io/) Configuration Files

## Devices

- Vera
- Google Chromecast
- Apple TV
- Rachio

---
### Google Assistant Integration
> For a full walkthrough reference [HomeAssistant.io](https://home-assistant.io/components/google_assistant/)

The below processes are brief notes used to set up my Google Assistant Integration with Home Assistant\
**Home Assistant to Google Assistant workflow:**
![Home Assistant to Google Assistant workflow](www/workflow-GAtoHA.png "Mark is awesome" )

**Google Assistant Interaction**
![Google Assistant Interaction](www/screenshot-FrontLights.jpeg "Google Assistant" )

#### Home Assistant Configuration
<details> 
  <summary>Click to Expand...</summary>
  <ol>
    <li>Enable the `google_assistant` component in your [HA config](configuration.yaml) file
    <li>Choose which components to expose from HA to GA. *(I chose to expose Lights, Scenes, and Climate Control)*
    <li>Test config and **reset HA Service**, this will enable the GA API into HA
  </ol>
</details>

#### Home Assistant -to- Google Assistant
<details> 
  <summary>Click to Expand...</summary>
  <ol>
    <li>Download <a href="https://developers.google.com/actions/tools/gactions-cli">gactions CLI</a> in your <a href="bin">bin directory</a>
    <li>Create a new <code>project.json</code> file following the <a href="https://home-assistant.io/components/google_assistant/">HA Guide</a>.
     This will be used to generate a secret for the Google project in the preceding step. 
    <li>Create a new Google Developer Project through the <a href="https://console.actions.google.com/u/0/">Developer Console</a>.
    <li>Link your Environment via the gactions: (my evn is a Pi, your env could be a docker or virtPython) 
    <ul>
        <li><code>cd bin; chmod +x gactions</code>
        <li><code>./gactions update --action_package project.json --project YourProjectName-2d0b8</code>
        <li>The <code>gactions</code> script will pause and issue a url to authenticate against your Google ID. Once you open the link in a browser, it will give you a key to continue with the <code>gactions</code> script.
        <li>You should now notice a <code>creds.data</code> file is now created in the <a href="bin">bin directory</a>. This is specific key between your environment and the Google Project.
    </ul>
    <li>Finish out the required Account Linking within your Google Project following the <a href="https://home-assistant.io/components/google_assistant/">HA Guide</a>.
    <ul>
        <li>This step is rather lengthy. 
        <li>Ensure your <b>Authorization URL</b> has the proper URL: <code>https://[site.com]:8123/api/google_assistant/auth</code>
    </ul>
    <li>Look for the <b>TEST DRAFT</b> button, once you're project is in the <i>testing</i> phase, you should be able to add your project on your phone's Google Assistant by:
    <ul>
        <li>Google Assistant > Settings > Home Control > Add Devices(+)
        <li>look for: <code>[test] ProjectName</code>
        <li>Once selected, you should start to see the devices that you allowed GA to know about from the Home Assistant configuration section above.
    </ul>
  </ol>
</details>

#### Configuration Setup

configuration.yaml

    google_assistant: !include includes/google_assistant.yaml

includes/google_assistant.yaml

    project_id:     !secret ga_project_id
    client_id:      !secret ga_client_id
    access_token:   !secret ga_token
    agent_user_id:  !secret ga_user
    api_key:        !secret ga_api
    exposed_domains:
      - light
      - scene
      - climate

secrets.yaml

    ga_project_id:  project-id
    ga_client_id:   long-string (used in GProject > Account linking > Client ID)
    ga_token:       this-is-a-token (random token)
    ga_user:        user (used for request_sync services)
    ga_api:         api-key (used for request_sync services)

#### New Environment Setup
  1. Download [gactions CLI](https://developers.google.com/actions/tools/gactions-cli)
  2. Create a new `project.json`
  3. Link new env: `./gactions update --action_package project.json --project YourProjectName-2d0b8`
  4. Unlink - Relink within Google Assistant phone app (step 6 above).

#### Google Assistant devices refresh after HA change
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


[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
[workflow-HA2GA]: www/workflow-GAtoHA.png