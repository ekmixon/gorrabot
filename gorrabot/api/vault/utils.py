import hvac
from hvac.exceptions import InvalidRequest
from . import FARADAY_VAULT_SERVER, ROLE_ID, SECRET_ID

ERROR_MESSAGE = "VaultError: {}"

try:
    ***REMOVED*** = hvac.Client(url=FARADAY_VAULT_SERVER)
    ***REMOVED***.auth.approle.login(role_id=ROLE_ID, secret_id=SECRET_ID)
except InvalidRequest as e:
    message = f"Cannot connect to Vault server, {e}"
    print(ERROR_MESSAGE.format(message))
    exit(1)


def get_secret(secret_name):
    """ Gets a given secret from Vault

    :param secret_name: Name of the secret stored in Vault
    :type secret_name: str
    :return: Secret's content
    :rtype: str if secrets exists, Exception otherwise
    """
    try:
        if ***REMOVED*** and ***REMOVED***.is_authenticated():
            secret_response = ***REMOVED***.secrets.kv.v2.read_secret_version(
                mount_point='secrets',
                path='gorrabot'
            )
            return secret_response['data']['data'][secret_name]
    except KeyError as e:
        message = f"Secret {e} could not be found"
        print(ERROR_MESSAGE.format(message))
        exit(1)
