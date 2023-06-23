from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

def Send_Listing(URL):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'

    link = URL

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "NEW POSTING"
    html_content = f"<html><body><h1> {link} </h1></body></html>"
    sender = {"name":"Facebook Bot","email":"pythonnotifier996@gmail.com"}
    to = [{"email":"owenlheron@gmail.com","name":"Owen Lheron"}]
    cc = [{"email":"jemegar@gmail.com","name":"Jackson Megar"}]
    reply_to = {"email":"replyto@domain.com","name":"DO NOT REPLY"}
    headers = {"Some-Custom-Name":"unique-id-1234"}
    params = {"parameter":"My param value","subject":"New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, headers=headers, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        response = api_response
    except ApiException as e:
        response = "Exception when calling SMTPApi->send_transac_email: %s\n" % e
    return response

