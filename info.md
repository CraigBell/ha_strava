# Strava Connect for Home Assistant

Strava Connect synchronizes your Strava account with Home Assistant, exposing sensors for up to ten recent activities, summary
statistics, lifetime shoe and bike mileage, and an optional photo carousel. Configure the integration directly from the UI and
choose the number of activities, distance units, update cadence for photos, and an optional geocode.xyz API key. A service is
available to assign gear to activities without leaving Home Assistant.

* Authorization callback domain: `my.home-assistant.io`
* HACS redirect: `https://my.home-assistant.io/redirect/hacs_repository/?owner=your-username&repository=strava_connect&category=integration`
* Config flow redirect: `https://my.home-assistant.io/redirect/config_flow_start/?domain=strava_connect`
* Required Strava scopes: `read`, `profile:read_all`, `activity:read_all`, `activity:write`

This project is distributed under the MIT License.
