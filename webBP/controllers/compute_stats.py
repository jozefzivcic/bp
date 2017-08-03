import time

def compute_stats(handler):
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    handler.send_header('Location', '/groups')
    handler.end_headers()
    time.sleep(2)
    return