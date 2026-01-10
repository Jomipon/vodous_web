from io import BytesIO
import pycurl

def download_get_url(url):
    """
    Send GET request to server and return status + responce
    
    :param url: URL web address
    """
    client = pycurl.Curl()
    client.setopt(pycurl.URL, url.encode("utf-8"))
    buffer = BytesIO()
    client.setopt(client.WRITEDATA, buffer)
    client.setopt(pycurl.USERAGENT, "VodousApp/1.0 (+tomas.vlasaty8@gmail.cz; https://jomipon-beruska-prototyp.streamlit.app/)")
    try:
        client.perform()
        status = client.getinfo(pycurl.RESPONSE_CODE)
        client.close()
        body = buffer.getvalue()
        try:
            body = body.decode("utf-8")
        except:
            pass
    except:
        status = 500
        body = None
    return {"status": status, "data": body}

def download_post_url(url, post_data, headers):
    """
    Send POST request to server and return status + responce
    
    :param url: URL web address
    :param post_data: Post data
    :param headers: str
    """
    if post_data.strip().startswith("{") or post_data.strip().startswith("["):
        post_data = (
            post_data
            .replace(": True", ": true")
            .replace(": False", ": false")
            .replace(": None", ": null")
        )
    client = pycurl.Curl()
    client.setopt(client.URL, url)
    client.setopt(client.POSTFIELDS, post_data)
    buffer = BytesIO()
    client.setopt(client.WRITEDATA, buffer)
    client.setopt(pycurl.USERAGENT, "VodousApp/1.0 (+tomas.vlasaty8@gmail.cz; https://jomipon-beruska-prototyp.streamlit.app/)")
    if headers is not None and len(headers) > 0:
        client.setopt(pycurl.HTTPHEADER, headers)
    client.perform()
    status_code = client.getinfo(pycurl.RESPONSE_CODE)
    if not str(status_code).startswith("20"):
        return ""
    client.close()
    body = buffer.getvalue()
    return body
