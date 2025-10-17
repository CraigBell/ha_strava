# Contributing

## Repo Details

The repo is loosely based on
https://github.com/custom-components/integration_blueprint, which enables
interactive debugging and instantanious testing for thie custom component.

## Installation

### virtualenv

Basic python development dependencies.

```
python3 -m pip install virtualenv
tools/setup_virtualenv.sh
```

### vscode devcontainers

Fully fleshed out dev environment based on remote containers and Visual Studio Code.

1.  Launch Visual Studio Code.
1.  Install [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
1.  Open the folder containing the HA Strava Code Git repo.
1.  When prompted, re-open in the "remote container."

## Manual testing checklist

Whether you are preparing a release or validating a contribution locally, run through the following steps so the
Strava Connect integration stays reliable:

1. `python -m compileall custom_components/strava_connect`
2. Start Home Assistant (for example by running `hass` inside the devcontainer) and complete the Strava Connect config flow.
3. Confirm the Strava authorization dialog lists the `read`, `profile:read_all`, `activity:read_all`, and `activity:write`
   scopes and that the redirect returns to Home Assistant successfully.
4. After the first data sync, check that activity sensors, shoe devices (with distance/primary/retired entities), bike sensors,
   and the photo camera populate with values.
5. Call the `strava_connect.set_activity_gear` service from Developer Tools → Services and verify the gear assignment updates in
   both Home Assistant and the Strava website.
6. Trigger the `strava_connect.refresh_gear` service and confirm it forces an immediate update of shoe mileage and binary
   sensors.
7. Record a new activity (or edit one) on Strava and confirm Home Assistant receives the webhook update (including a
   `strava_connect_gear_updated` event) without needing a manual refresh.

These steps mirror the recommended "next steps" in the README and ensure the integration is ready for a pull request.
