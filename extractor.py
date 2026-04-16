import re
import requests


def get_api_info(url):
    """Extract API info from OpenAPI/Swagger JSON URL"""
    try:
        # Try to fetch the URL directly
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Try parsing as JSON (OpenAPI spec)
        try:
            spec = response.json()
        except:
            content = response.text
            spec = None
        
        if spec and isinstance(spec, dict):
            # Parse OpenAPI/Swagger spec
            endpoints = []
            paths = spec.get('paths', {})
            
            for path, methods in paths.items():
                for method in methods.keys():
                    if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
                        endpoints.append((method.upper(), path))
            
            # Extract auth methods from spec
            auth_methods = []
            security_schemes = spec.get('components', {}).get('securitySchemes', {})
            for scheme_name, scheme_def in security_schemes.items():
                scheme_type = scheme_def.get('type', '').lower()
                if scheme_type == 'apikey':
                    auth_methods.append('API Key')
                elif scheme_type == 'http':
                    auth_methods.append('Bearer Token')
                elif scheme_type == 'oauth2':
                    auth_methods.append('OAuth2')
            
            return {
                "endpoints": [f"{method} {path}" for method, path in endpoints],
                "auth_methods": list(set(auth_methods)) if auth_methods else [],
                "sdks": []
            }
        else:
            # Fallback: regex extraction from HTML content
            content = response.text
            endpoints = re.findall(r'(GET|POST|PUT|DELETE)\s+(/[^\s"<]+)', content)
            auth_methods = re.findall(r'(API Key|Bearer Token|OAuth2|Basic Auth)', content, re.IGNORECASE)
            
            return {
                "endpoints": list(set(endpoints)),
                "auth_methods": list(set(auth_methods)),
                "sdks": []
            }
    
    except Exception as e:
        print(f"Error extracting API info: {str(e)}")
        return {
            "endpoints": [],
            "auth_methods": [],
            "sdks": []
        }
