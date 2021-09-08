import os


def random_hex_str(len):
    hex_str = ''.join(
        [('0'+hex(ord(os.urandom(1)))[2:])[-2:] for _ in range(len // 2)])
    return hex_str


def get_file_size(file_path):
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    else:
        return 0


def get_entire_html(block):
    tpml = """
        <!DOCTYPE html>
        <html>
            <head> <title>ESP32 Web Server</title> </head>
            <body>$$</body>
        </html>
    """

    html = tpml.replace('$$', block)
    return html


def init_config():
    pass
