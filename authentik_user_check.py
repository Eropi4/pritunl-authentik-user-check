import requests
from pritunl import logger

# Constants for Authentik configuration
AUTHENTIK_BASE_URL = 'https://authentik.company'  # Replace with your actual keycloak url
AUTHENTIK_API_TOKEN = 'API_TOKEN'  # Replace with Authentik API token
DEBUG = False  # Set to True to enable debug logging
SEARCH_BY_EMAIL = False  # Set to True to search by email, False to search by username


# Function to log debug information
def debug_log(message):
    if DEBUG:
        logger.debug(message)


# Function to determine if access should be denied based on user's status in Keycloak
def should_deny_access(user_identifier):
    # Determine the search parameter based on the setting
    search_param = 'email' if SEARCH_BY_EMAIL else 'username'

    # Headers with the authorization token
    headers = {'Authorization': f'Bearer {AUTHENTIK_API_TOKEN}'}
    user_url = f"{AUTHENTIK_BASE_URL}/api/v3/core/users/?include_groups=false&{search_param}={user_identifier}"
    try:
        # Making a GET request to check the user's status
        debug_log(f"Checking user status: URL={user_url}, Headers={headers}")
        response = requests.get(user_url, headers=headers)

        # Logging response body for debugging
        debug_log(f"Response Body: {response.text}")

        response.raise_for_status()  # Raises an exception for HTTP errors

        resp_json = response.json()
        if not resp_json or 'results' not in resp_json:
            return 'Invalid Authentik response'

        if len(resp_json.get('results')) == 0:
            return 'User not found in Authentik'

        user = resp_json.get('results')[0]
        if not user.get('is_active'):
            return 'User is not active in Authentik'

        return None  # User is allowed
    except requests.RequestException as e:
        logger.error("Error in requesting user information", "user_check", error=str(e))
        return 'Error checking user status'
    except ValueError as e:
        # Error parsing JSON
        logger.error("Error parsing JSON from Authentik response", "json_parse_error", error=str(e))
        return 'Error parsing server response'


# user_connect hook
def user_connect(user_name, **kwargs):
    # Determine if access should be denied
    status = should_deny_access(user_name)
    if status:
        # Return False if the user should be denied access
        logger.info(f"Access denied for user \"{user_name}\". Reason: {status}")
        return False, status

    # Return True, None to allow connection if the user is allowed
    return True, None
