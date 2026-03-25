from dotenv import load_dotenv
load_dotenv()  # 1. Load environment variables from .env file

from app import create_app # 2. Import the create_app function from the app module
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
