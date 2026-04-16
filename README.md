# Smart API Integration Tool

## Overview
The Smart API Integration Tool is a web application designed to simplify the process of integrating with various APIs. It allows users to extract API information from documentation, generate wrapper classes in their preferred programming language, and provides a user-friendly interface for interaction.

## Features
- Extracts API endpoints and authentication methods from documentation.
- Suggests SDKs or REST integration based on the documentation.
- Auto-generates wrapper classes in Python or Node.js.
- Simple and clean web interface for user input.
- Displays extracted endpoints, authentication details, and detected SDKs in a structured format.
- Syntax-highlighted code output for better readability.
- Users can easily copy or download the generated code.
- Swagger/OpenAPI auto-detection for accurate parsing.
- Downloadable project files in ZIP format.
- AI-generated API summaries for concise overviews.
- Optional enhancements for testing API endpoints or exporting a Postman collection.

## Setup
1. Clone the repository:
   
   git clone <repository-url>
   cd api-integration-tool
   

2. Install the required dependencies:

   pip install -r requirements.txt
   python -m playwright install


3. Run the application:
   
   python app.py
   

4. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage
- Enter the API documentation URL in the provided input field.
- Specify your use case in the designated area.
- Select your preferred programming language (Python or Node.js).
- Click the "Generate" button to process the input.
- View the extracted API information and generated code on the results page.
- Copy or download the generated code as needed.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.