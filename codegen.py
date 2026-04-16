def generate_python_wrapper(endpoints, auth_methods, usecase):
    auth_code = ""
    if "Bearer Token" in auth_methods:
        auth_code = "headers={'Authorization': f'Bearer {token}'}"
    elif "API Key" in auth_methods:
        auth_code = "headers={'x-api-key': api_key}"
    else:
        auth_code = ""

    methods = []
    for endpoint in endpoints:
        # Parse endpoint string format "METHOD /path"
        if isinstance(endpoint, str):
            parts = endpoint.split(' ', 1)
            method = parts[0] if len(parts) > 0 else 'GET'
            path = parts[1] if len(parts) > 1 else '/'
        else:
            method, path = endpoint
        
        func_name = path.strip('/').replace('/', '_').replace('-', '_').replace('{', '').replace('}', '')
        methods.append(f"""
    def {func_name}(self, params=None, data=None):
        \"\"\"Auto-generated for {method} {path}\"\"\"
        url = self.base_url + '{path}'
        response = self.session.request('{method}', url, params=params, json=data, {auth_code})
        return response.json()
        """)
    methods_code = "\n".join(methods)

    return f"""
import requests

class APIWrapper:
    def __init__(self, base_url, token=None, api_key=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = token
        self.api_key = api_key

    {methods_code}
# Usage: wrapper = APIWrapper(base_url, token='...', api_key='...')
"""

def generate_nodejs_wrapper(endpoints, auth_methods, usecase):
    auth_code = ""
    if "Bearer Token" in auth_methods:
        auth_code = "'Authorization': `Bearer ${token}`"
    elif "API Key" in auth_methods:
        auth_code = "'x-api-key': apiKey"
    else:
        auth_code = ""

    methods = []
    for endpoint in endpoints:
        # Parse endpoint string format "METHOD /path"
        if isinstance(endpoint, str):
            parts = endpoint.split(' ', 1)
            method = parts[0] if len(parts) > 0 else 'GET'
            path = parts[1] if len(parts) > 1 else '/'
        else:
            method, path = endpoint
        
        func_name = path.strip('/').replace('/', '_').replace('-', '_').replace('{', '').replace('}', '')
        methods.append(f"""
  async {func_name}(params = {{}}, data = {{}}, token = '', apiKey = '') {{
    // Auto-generated for {method} {path}
    const url = this.baseUrl + '{path}';
    const headers = {{{auth_code}}};
    const res = await fetch(url, {{
      method: '{method}',
      headers,
      body: JSON.stringify(data)
    }});
    return res.json();
  }}
        """)
    methods_code = "\n".join(methods)

    return f"""
class APIWrapper {{
  constructor(baseUrl) {{
    this.baseUrl = baseUrl;
  }}
  {methods_code}
}}
// Usage: const wrapper = new APIWrapper(baseUrl);
"""


def generate_wrapper(endpoints, auth_methods, usecase, lang):
    if lang == "python":
        return generate_python_wrapper(endpoints, auth_methods, usecase)
    elif lang == "nodejs":
        return generate_nodejs_wrapper(endpoints, auth_methods, usecase)
    else:
        return "# Language not supported"