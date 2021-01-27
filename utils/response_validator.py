MAX_CONTENT_SIZE = 50000

class ResponseValidator:
    def is_worth_scraping(resp):
        if resp.raw_response == None:
            return True
        
        headers = resp.raw_response.headers

        if ResponseValidator.too_large(headers):
            return False
        
        if ResponseValidator.is_empty(headers):
            return False

        if ResponseValidator.error_code(resp):
            return False

        return True
    
    def too_large(headers):
        try:
            content_length = int( headers['content-length'] )
            return content_length > MAX_CONTENT_SIZE
        except KeyError:
            return False
    
    def is_empty(headers):
        try:
            content_length = int( headers['content-length'] )
            return content_length == 0
        except KeyError:
            return False
    
    def error_code(resp):
        return resp.status != 200

