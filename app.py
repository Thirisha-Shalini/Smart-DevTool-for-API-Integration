from flask import Flask, render_template, request, jsonify
from extractor import get_api_info
from codegen import generate_wrapper
import os
import zipfile
from utils.downloader import create_zip

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if request.is_json:
            data = request.get_json()
            url = data.get('url', '')
            usecase = data.get('usecase', '')
            lang = data.get('lang', 'python')
        else:
            url = request.form['url']
            usecase = request.form['usecase']
            lang = request.form['lang']

        print(f"Processing: URL={url}, Lang={lang}")
        
        api_info = get_api_info(url)
        print(f"API Info: {api_info}")

        if api_info.get('error'):
            error_message = api_info['error']
            print(f"API info error: {error_message}")
            if request.is_json:
                return jsonify({'error': error_message}), 400
            return render_template('index.html', error=error_message)

        code = generate_wrapper(api_info['endpoints'], api_info['auth_methods'], usecase, lang)
        print(f"Code generated: {len(code)} chars")

        if request.is_json:
            response_data = {
                'endpoints': api_info.get('endpoints', []),
                'auth_methods': api_info.get('auth_methods', []),
                'sdks': api_info.get('sdks', []),
                'generated_code': code,
                'lang': lang
            }
            print(f"Returning JSON response: {response_data}")
            return jsonify(response_data)

        return render_template('results.html', api_info=api_info, code=code, lang=lang)
    
    except Exception as e:
        print(f"Error in /generate: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    usecase = request.form['usecase']
    lang = request.form['lang']

    api_info = get_api_info(url)
    code = generate_wrapper(api_info['endpoints'], api_info['auth_methods'], usecase, lang)

    # Create a zip file with the generated code
    zip_filename = create_zip(api_info, code, lang)
    
    return jsonify({'zip_file': zip_filename})

if __name__ == '__main__':
    app.run(debug=True)