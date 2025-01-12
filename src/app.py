from core.config_loader import load_config

def main():
    config = load_config()
    
    print(f"Project Name: {config['project_name']}")
    print(f"Author: {config['author']}")

if __name__ == "__main__":
    main()
