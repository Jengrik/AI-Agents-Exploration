from openai import OpenAI
from core.config_loader import GeneralConfig

def test_openai_request(prompt):
  """
  Sends a direct request to OpenAI using the provided prompt.

  Args:
      prompt (str): The input message to send to OpenAI.

  Returns:
      str: The response content from OpenAI, or an error message if the request fails.
  """
  
  #* Loading configuration
  config = GeneralConfig().get_full_config()
  openai_config = config.get("api_keys", {}).get("openai", {})
  api_key = openai_config.get("api_key", "undefined")

  if api_key == "undefined":
      return "Error: API Key not found in the configuration."

  #* OpenAI cliente creation
  client = OpenAI(api_key=api_key)

  try:
    chat_completion = client.chat.completions.create(
      messages=[
        {"role": "user", "content": prompt}
      ],
      model="gpt-4o",
    )
    return chat_completion.choices[0].message.content
  except Exception as e:
      return f"OpenAI Error: {str(e)}"

def main():
  config = GeneralConfig().get_client_config()
  print(config)

if __name__ == "__main__":
  main()
