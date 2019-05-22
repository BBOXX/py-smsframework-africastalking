import africastalking
from smsframework import IProvider


class AfricasTalkingProvider(IProvider):
    """Africa's Talking Provider"""

    def __init__(self, gateway, name, username, api_key):
        """
        Configure AfricasTalking Provider

        :param gateway: (smsframework.Gateway) Passed automatically by gateway on add_provider call
        :param name: (str) Uniquely identify the instance of AfricasTalkingProvider registered to the gateway
        :param username: (str) Username for your AfricasTalking account
        :param api_key: (str) API key for your AfricasTalking account
        """
        super(gateway, name)

        africastalking.initialize(username, api_key)
        self.sms_client = africastalking.SMS
