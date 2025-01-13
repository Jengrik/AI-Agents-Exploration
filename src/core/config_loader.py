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
      self._client_config = self._build_client_config()

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

  def _build_client_config(self):
    """
    Constructs the configuration dictionary required by OpenAIChatCompletionClient.
    Dynamically includes only the parameters present in the configuration and secrets.

    Returns:
        dict: The configuration for OpenAIChatCompletionClient.
    """
    #* Base configuration
    base_config = self._full_config.get("api_keys", {}).get("openai", {})

    #* Mapping of available parameters to their values
    raw_config = {
        "model": base_config.get("model"),
        "api_key": base_config.get("api_key"),
        "organization": base_config.get("org_name"),
        "base_url": base_config.get("base_url"),
        "timeout": base_config.get("timeout"),
        "max_retries": base_config.get("max_retries"),
        "frequency_penalty": base_config.get("frequency_penalty"),
        "logit_bias": base_config.get("logit_bias"),
        "max_tokens": base_config.get("max_tokens"),
        "n": base_config.get("n"),
        "presence_penalty": base_config.get("presence_penalty"),
        "response_format": base_config.get("response_format"),
        "seed": base_config.get("seed"),
        "stop": base_config.get("stop"),
        "temperature": base_config.get("temperature"),
        "top_p": base_config.get("top_p"),
        "user": base_config.get("user"),
    }

    filtered_config = {key: value for key, value in raw_config.items() if value is not None}
    return filtered_config

  def get_full_config(self):
    """
    Returns the full resolved configuration.

    Returns:
        dict: The full configuration.
    """
    return self._full_config
  
  def get_client_config(self):
    """
    Returns the client configuration.

    Returns:
        dict: The client configuration.
    """
    return self._client_config
