# pritunl-authentik-user-check

_Inspired by https://github.com/sample/pritunl-keycloak-user-check. Check repo for more information. Setup process is very similar._

## Description
The `pritunl-authentik-user-check` is a plugin for Pritunl that checks if a user is available in Authentik.

## What the Script Does
The script acts as a middleware between Pritunl and Authentik, performing real-time user status checks during VPN connection attempts. 
It ensures that only users who exist in Authentik and are active are allowed to access the Pritunl VPN.

## Configuration Parameters
Before deploying the script, you need to adjust several parameters to match your Keycloak and Pritunl setup:

- `AUTHENTIK_BASE_URL`: The URL of your Authentik instance.
- `AUTHENTIK_API_TOKEN`: Authentik API token of the user who access to /core/users/
- `DEBUG`: Set to `True` for detailed logging, useful for debugging.
- `SEARCH_BY_EMAIL`: Set to `True` to search users by email, `False` to search by username.

## Installation


### Script installation
Follow these steps to deploy the `pritunl-authentik-user-check` script on your Pritunl server:

1. Ensure you have a Keycloak client set up for your Pritunl server.
2. Place `authentik_user_check.py` to the Pritunl plugins directory. By default, this directory is `/var/lib/pritunl/plugins`.
3. Adjust the parameters in the script as per your Keycloak configuration.
4. sudo `systemctl restart pritunl`.
5. Check the Pritunl logs to ensure that the plugin is loaded correctly and functioning as expected `tail /var/log/pritunl.log -n 100`.
