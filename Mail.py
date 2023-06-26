from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

def Send_Listing(title, URL, price, query):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = 'YOUR-API-KEY'

    link = URL

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = f"{query}: {title}"
    html_content = f"<html><body><h1> Title: {query} \n Price: {price} \n URL: {link} </h1></body></html>"
    sender = {"name":"Facebook Bot","email":"examplesender@gmail.com"}
    to = [{"email":"example@gmail.com","name":"Prime Example"}]
    cc = [{"email":"example2@gmail.com","name":"Secondary Example"}]
    reply_to = {"email":"replyto@domain.com","name":"DO NOT REPLY"}
    headers = {"Some-Custom-Name":"unique-id-1234"}
    params = {"parameter":"My param value","subject":"New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, cc=cc reply_to=reply_to, headers=headers, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        response = api_response
    except ApiException as e:
        response = "Exception when calling SMTPApi->send_transac_email: %s\n" % e
    return response

