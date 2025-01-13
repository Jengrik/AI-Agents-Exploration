import yaml
import json
from threading import Lock
from utils.file_loader import load_file


class GeneralConfig:
  """
  Singleton class to manage application configurations. Provides access to the
  full configuration and the LLM-specific configuration, ensuring they are
  loaded only once during the application's lifecycle.
  """

  _instance = None
  _lock = Lock()

  def __new__(cls, *args, **kwargs):
    """
    Ensures only one instance of GeneralConfig is created. Thread-safe implementation using a lock.
    """
    if not cls._instance:
      with cls._lock:
        if not cls._instance:
          cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self):
      """
      Initializes the GeneralConfig instance by loading and caching configurations.
      Ensures that initialization logic runs only once.
      """
      if not hasattr(self, "_initialized"):
        self._initialized = True
        self._config = load_file("src/config/config.yaml", loader=yaml.safe_load)
        self._secrets = load_file("src/config/secrets.json", loader=json.load)
        self._full_config = self._build_full_config()
        self._llm_config = self._build_llm_config()

  def _replace_placeholders(self, config_section, secrets_section, parent_keys=None):
      """
      Recursively replaces placeholders ('load_from_secrets') in the configuration
      with corresponding values from the secrets.

      Args:
          config_section (dict): The configuration section, possibly nested.
          secrets_section (dict): The secrets section, possibly nested.
          parent_keys (list): List of keys representing the current nested path.

      Returns:
          dict: The configuration with placeholders replaced.
      """
      parent_keys = parent_keys or []

      for key, value in config_section.items():
        current_path = parent_keys + [key]

        if isinstance(value, dict):
          config_section[key] = self._replace_placeholders(value, secrets_section, current_path)
        elif value == "load_from_secrets":
          secrets_cursor = secrets_section
          for part in current_path[1:]:
            if isinstance(secrets_cursor, dict) and part in secrets_cursor:
              secrets_cursor = secrets_cursor[part]
            else:
              secrets_cursor = "undefined"
              break
          config_section[key] = secrets_cursor
      return config_section

  def _build_full_config(self):
      """
      Resolves all placeholders in the base configuration using secrets
      and builds the full configuration object.

      Returns:
          dict: The full configuration object.
      """
      return self._replace_placeholders(self._config, self._secrets)

  def _build_llm_config(self):
      """
      Builds the LLM configuration required by AutoGen, resolving placeholders
      specifically for the LLM section.

      Returns:
          dict: The LLM configuration in the format required by AutoGen.
      """
      # Access model and API key from the resolved configuration
      openai_config = self._full_config.get("api_keys", {}).get("openai", {})
      model = openai_config.get("model", "undefined")  # Default to "undefined" if not found
      api_key = openai_config.get("api_key", "undefined")

      return {
        "config_list": [
          {
            "model": model,
            "api_key": api_key
          }
        ]
      }

  def get_full_config(self):
      """
      Returns the full resolved configuration.

      Returns:
          dict: The full configuration.
      """
      return self._full_config

  def get_llm_config(self):
      """
      Returns the LLM-specific configuration.

      Returns:
          dict: The LLM configuration.
      """
      return self._llm_config
