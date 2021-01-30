import urllib.robotparser
from urllib.parse import urlparse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def robot_can_fetch(url) -> bool:
    parsed = urlparse(url)
    try:
        # 1. Create RobotFileParser instance
        rp = urllib.robotparser.RobotFileParser()
        # 2. Set URL
        # Robots.txt is always there after the root url
        rp.set_url(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
        # 3. Read and interpret robots.txt
        rp.read()

        # Return True if the url is allowed to be fetch
        return rp.can_fetch("*", url)
    except urllib.error.URLError:
        return True
