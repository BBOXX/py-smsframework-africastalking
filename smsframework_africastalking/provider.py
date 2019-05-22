import africastalking
import phonenumbers
from smsframework import IProvider

from .error import AfricasTalkingProviderError


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
        super().__init__(gateway, name)

        africastalking.initialize(username, api_key)
        self.sms_client = africastalking.SMS

    def send(self, message):
        """
        Send a single text message.
        TODO: Add a batch send feature.

        :param message: (smsframework.OutgoingMessage) The message to send.
        :return: (smsframework.OutgoingMessage) The sent message, updated with msgid.
        """

        try:
            phone_number = phonenumbers.parse(
                message.dst,
                message.provider_params['target_country']
            )

            formatted_number = phonenumbers.format_number(
                phone_number,
                phonenumbers.PhoneNumberFormat.E164
            )
        except:
            raise AfricasTalkingProviderError('PHONE_NUMBER_PARSE_ERROR')

        try:
            api_response = self.sms_client.send(
                message.body,
                [formatted_number],
                message.provider_options.senderId
            )

            sent_message = api_response['SMSMessageData']['Recipients'][0]

            if sent_message['status'] != 'Success':
                raise Exception
        except:
            raise AfricasTalkingProviderError('API_ERROR')

        message.msgid = sent_message['messageId']
        return message