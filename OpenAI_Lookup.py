import openai

# Load your API key from an environment variable or secret management service
# open ai API key
openai.api_key = "YOUR-API-KEY"

# Define the system message
system_msg = "You are an assistant that is responsible for taking the title and description of posts from Facebook marketplace and identifying what the item or items are that the user is sellings. Reply only with the items."

def ask_gpt(user_msg):
      # GPT response
    response = openai.ChatCompletion.create(model= "gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                             {"role": "user", "content": user_msg}])
    content = response["choices"][0]["message"]["content"]
    code = response["choices"][0]["finish_reason"]

    return content