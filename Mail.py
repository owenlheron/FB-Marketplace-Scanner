from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def Send_Listing(email, title, URL, price, description, distance, query):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = 'YOUR-API-KEY'

    link = URL

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = f"{title} ({query})"
    html_content = f"<html><body><h1>Price: {price} <br>Distance: {distance} miles <br>URL: {link} <br>Description: {description} </h1></body></html>"
    sender = {"name":"Facebook Bot","email":"pythonnotifier996@gmail.com"}
    to = [{"email":f"{email}","name":"Subscriber"}]
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
