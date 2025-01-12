import yaml
import json

def replace_placeholders(config_section, secrets_section):
    """
    Recursively replaces placeholders ("load_from_secrets") in a configuration section
    with corresponding values from a secrets section. If a secret is not found,
    it is set to "undefined".

    Args:
        config_section (dict): Section of the configuration (can be nested).
        secrets_section (dict): Section of the secrets (can be nested).

    Returns:
        dict: Updated configuration section with secrets resolved.
    """
    for key, value in config_section.items():
        if isinstance(value, dict):
            config_section[key] = replace_placeholders(value, secrets_section.get(key, {}))
        elif value == "load_from_secrets":
            config_section[key] = secrets_section.get(key, "undefined")
    return config_section

def load_config():
    """
    Loads configuration from 'config.yaml' and secrets from 'secrets.json',
    dynamically replacing any placeholder ("load_from_secrets") with its
    corresponding value from 'secrets.json'.

    Returns:
        dict: The final combined configuration with updated keys.
    """

    config_path = "src/config/config.yaml"
    secrets_path = "src/config/secrets.json"

    with open(config_path, "r") as yaml_file:
        config = yaml.safe_load(yaml_file)

    with open(secrets_path, "r") as json_file:
        secrets = json.load(json_file)

    config["api_keys"] = replace_placeholders(config.get("api_keys", {}), secrets)

    return config
