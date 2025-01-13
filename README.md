# AI Agents Project

## Overview
The **AI Agents Project** is a modular, extensible, and scalable system designed to facilitate exploration, experimentation, and integration of emerging AI agent technologies. With a primary focus on leveraging the **AutoGen Framework**, this project streamlines the creation, management, and deployment of intelligent agents for diverse use cases.

The project is crafted to uphold flexibility and scalability, ensuring seamless adaptation to various requirements while maintaining a clean and well-structured codebase.

---

## Features
- **Scalable Architecture:** Designed for extensibility with support for nested configurations and future integrations.
- **Dynamic Agent Framework:** Provides a modular structure to implement and manage AI agents efficiently.
- **Secure Configuration Management:** Employs YAML and JSON files to manage project settings and sensitive credentials securely.
- **Readability and Maintainability:** Adheres to Python’s best practices for clean, modular, and well-documented code. 📚

---

## Project Structure
```plaintext
ai-agents-project/
├── env/                      # Virtual environment (excluded from version control)
├── src/                      # Main source code directory
│   ├── agents/               # AI agent implementations
│   ├── utils/                # Reusable helper functions and utilities
│   ├── core/                 # Core logic and configuration handling
│   │   ├── config_loader.py  # Dynamically loads configurations and secrets
│   ├── config/               # Configuration and secret files
│   │   ├── config.yaml       # Main configuration file
│   │   ├── secrets.json      # Stores sensitive information (e.g., API keys)
│   ├── app.py                # Entry point for the project
├── tests/                    # Unit tests
├── docs/                     # Documentation and related resources
├── requirements.txt          # Python dependency file
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

---

## Prerequisites

### System Requirements
- **Python:** Version 3.12.8 (strictly required for compatibility)
- **Operating System:** Compatible with macOS, Linux, and Windows

### Dependencies
All required Python packages are listed in `requirements.txt`. Follow the installation instructions in the next section to set up the environment. 📦

---

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/ai-agents-project.git
cd ai-agents-project
```

### Step 2: Set Up a Virtual Environment
Create a Python virtual environment to isolate project dependencies:
```bash
python3.12 -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows
```

### Step 3: Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Secrets
Set up your sensitive credentials in the `src/config/secrets.json` file. Use the following structure:
```json
{
  "openai": {
    "api_key": "your-api-key",
    "org_name": "your-org-name"
  },
  "google": "your-google-api-key",
  }
}
```

### Step 5: Run the Application
Execute the project using:
```bash
python3.12 src/app.py
```

---

## Usage

### Running the Project
To start the application, run:
```bash
python3.12 src/app.py
```

This will initialize the configured agents and execute the project workflows as defined.

---

## References
- [Python Official Documentation](https://docs.python.org/3/)
- [AutoGen Framework Documentation](https://github.com/microsoft/autogen)

---

## Contributing
Contributions are encouraged! If you wish to contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a clear and detailed description of your changes.

---

## License
This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code with proper attribution.

