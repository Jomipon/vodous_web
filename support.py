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
    client.perform()
    status = client.getinfo(pycurl.RESPONSE_CODE)
    client.close()
    body = buffer.getvalue()
    body = body.decode("utf-8")
    return {"status": status, "data": body}
