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

## Solution Approach

### Core Workflow
1. **API Information Extraction** (`extractor.py`)
   - Fetches API documentation from provided URL using `requests`
   - Parses OpenAPI/Swagger JSON specifications automatically
   - Falls back to regex-based extraction from HTML documentation
   - Extracts endpoints, HTTP methods, paths, authentication schemes (API Key, Bearer Token, OAuth2)

2. **Intelligent Code Generation** (`codegen.py`)
   - Generates language-specific wrapper classes (Python or Node.js)
   - Creates auto-generated methods for each API endpoint
   - Automatically integrates detected authentication methods
   - Python: Returns `APIWrapper` class with `requests.Session` for HTTP requests
   - Node.js: Returns async class with `fetch` API

3. **User Interface** (`app.py`)
   - Flask backend processes user requests via `/generate` endpoint
   - Displays extracted endpoints, authentication details, and generated code
   - Supports code download as ZIP packages

### Example Output
- Python: Generates class with methods like `get_users()`, `post_users()` with built-in auth handling
- Node.js: Generates async methods compatible with modern JavaScript

The solution simplifies API integration by automating the extraction and code generation process, reducing manual integration effort.



Author : Thirisha Shalini 
License : MIT
