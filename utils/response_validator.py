MAX_CONTENT_SIZE = 50000

class ResponseValidator:
    
    def too_large(resp):
        if resp.raw_response == None:
            return False

        headers = resp.raw_response.headers
        try:
            content_length = int( headers['content-length'] )
            return content_length > MAX_CONTENT_SIZE
        except KeyError:
            return False
    
    def is_empty(resp):
        if resp.raw_response == None:
            return False

        headers = resp.raw_response.headers
        try:
            content_length = int( headers['content-length'] )
            return content_length == 0
        except KeyError:
            return False
    
    def error_code(resp):
        return resp.status != 200

