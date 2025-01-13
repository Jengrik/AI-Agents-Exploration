from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
from core.config_loader import GeneralConfig

class TestAgent:
  """
  A test agent to interact with OpenAI's GPT models using the AutoGen library.
  """

  def __init__(self):
    """
    Initializes the TestAgent by loading configuration and setting up the OpenAI client.
    """
    #* Initialize OpenAI client
    config = GeneralConfig()
    client_config = config.get_client_config()
    self.model_client = OpenAIChatCompletionClient(**client_config)

  async def ask_question(self, question: str) -> str:
    """
    Asks a question to the OpenAI model and returns the response.

    Args:
        question (str): The user's question.

    Returns:
        str: The model's response.
    """
    try:
      user_message = UserMessage(content=question, source="user")
      result = await self.model_client.create([user_message])
      return result.content
    except Exception as e:
      return f"An error occurred: {e}"
