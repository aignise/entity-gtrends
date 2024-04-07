import os
import time
import openai
import pandas as pd
from pytrends.request import TrendReq
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

cookies = {
    '__utma': '10102256.2146871208.1707922624.1711719334.1711725532.4',
    '__utmc': '10102256',
    '__utmz': '10102256.1711725532.4.2.utmcsr=trends.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
    'HSID': 'A1de4X_w0GEi_NkKV',
    'SSID': 'Ax_41s9rj8otaRc8E',
    'APISID': 'rILdZwcyEAnlkfJ0/AcVgoNduJGYG8kWMc',
    'SAPISID': 'I2KLbxpPWmmi9ixn/AAg1_div5IrJ9SghS',
    '__Secure-1PAPISID': 'I2KLbxpPWmmi9ixn/AAg1_div5IrJ9SghS',
    '__Secure-3PAPISID': 'I2KLbxpPWmmi9ixn/AAg1_div5IrJ9SghS',
    'SEARCH_SAMESITE': 'CgQI2poB',
    'SID': 'g.a000hwiztq70QhGIBCca9jq4mZjl7HQE2ypQDHLSytp_yBqobshxaru-1znfO_MiTNHZmi4fPgACgYKAR8SAQASFQHGX2MiRnkRvowhZOM9p4q5SiRWwRoVAUF8yKrFD9buxCeCS1Pnz3bKx_Fq0076',
    '__Secure-1PSID': 'g.a000hwiztq70QhGIBCca9jq4mZjl7HQE2ypQDHLSytp_yBqobshx-wSi-5YB9G1kyqVaMygO0gACgYKATkSAQASFQHGX2MiXFkcIq3KnjlEIX5Bc9L3qBoVAUF8yKom4SjLKHHpeBYmM7c8XwRw0076',
    '__Secure-3PSID': 'g.a000hwiztq70QhGIBCca9jq4mZjl7HQE2ypQDHLSytp_yBqobshxlLxEwKFlu23Mw_TbihtPJQACgYKATgSAQASFQHGX2MiUGeDxku6Tq_1AFpj4QWKyBoVAUF8yKqd1H34YWLH4s68HpyEtu_G0076',
    'AEC': 'Ae3NU9NMm4909XoaPjP0Km09LTZlW5WaUcGYyBv42ajQ7URm3jIstJ9Xkw',
    '_gid': 'GA1.3.238406708.1711719334',
    '1P_JAR': '2024-03-29-14',
    'OTZ': '7490358_34_34__34_',
    'NID': '512=Cy5pqYJ5rpgiymW5RkZ8llI4sWjLKkdE3MP6dpBFqwU8ffXX5LvxsktAbH1zGzv6g8HCOe3FoY91TYeNVvzBCtyjW6BDOE1hjTXqGf4HVPSW417Vz4braqCrdRDUpRN3dw5T-L8Qd8h9BkfHh5vnuZQxCehXBpubnfkY5NpIvNVh32fmP9Vd3yZaS5CKvcS5sr7An8lDJx_Sy8ffdHvqORD2KMozxb0MuJWL-9uW1nbznez7WkAOnB33g-jb5vbKKiC7UoAw-p0duGkRLTkINdztuO-wzZZoESSTGi0Qedr24MASyIrZyQ2FX_xNp6T5HYwIvdQP0t0DfoaHPbQNJFYAyzIv57OV8imhVFAvLAyyu1KyEUfAb2eliOMCvuPu8OpSMb3fP8h750YE4ACuccqnyHVc0PZSs0etvt7DH1Zj8R9Rcg8RmV7A91S3rl01G6AvGcIs-FJoyIuzBXrZ2byCtly5hXnjdk6Fr8X2tHNDK6mcW3YEb3cmXLl7cFFkv0Nw7Ke59tPVs3eLnkeJk3iLzzswYL7Eyivd3fU0OqHn7X1Yvj0poBbJPgjvhE2LLyoAScgfmvPmsXpcSLExKbzLzxIT2nGXwxLArk-V6vv6dXwmvkz5ROfvnNaVHruQjJ0lW_7LtHD_61KgfHwMO-cxh0Zm',
    '_ga': 'GA1.3.1962284024.1707922624',
    '__Secure-1PSIDTS': 'sidts-CjEB7F1E_EUKKDIhN_Jzcw3eDYnDuXGekhE_cQejFqRX8bsaaYN9BoqcJEk1drZ6zVudEAA',
    '__Secure-3PSIDTS': 'sidts-CjEB7F1E_EUKKDIhN_Jzcw3eDYnDuXGekhE_cQejFqRX8bsaaYN9BoqcJEk1drZ6zVudEAA',
    '_gat_gtag_UA_4401283': '1',
    'SIDCC': 'AKEyXzV9gphZvu4sVuYwNlhJY3qhn11FY550KSw9ueXQrlZ2teVT7q5qu7soi8Nu2xPeMfm6NFI',
    '__Secure-1PSIDCC': 'AKEyXzURF-X5xDVSVBnDEiYFx86fgiaz0FDAJoI57RbutW7m-qVPB6KNbDOokL8GkHlaxpk0iicm',
    '__Secure-3PSIDCC': 'AKEyXzWMbsisbSjq-MyaVFZNCDl4KKrl6VCKlsZ5wI_pcuZNQQO4ZfdjwlO1T34sN6LwqyeRfe8',
    '_ga_VWZPXDNJJB': 'GS1.1.1711730121.5.1.1711730359.0.0.0',
}
requests_args = {
    'headers': os.getenv("HEADERS")
}

# Custom TrendReq subclass to handle Google Trends cookies
class CookieTrendReq(TrendReq):
    def GetGoogleCookie(self):
        # Return only the NID cookie
        return {"NID": cookies.get("NID", "")}

# Function to fetch Google Trends data for a list of keywords
def fetch_google_trends(keywords, timeframe='today 5-y', geo='US', verbose=True):
    dff = None
    df_related_topics_rising = pd.DataFrame()
    df_related_topics_top = pd.DataFrame()
    df_related_queries_rising = pd.DataFrame()
    df_related_queries_top = pd.DataFrame()
    
    # Create an instance of the custom TrendReq subclass
    pytrends = CookieTrendReq(hl='en-US', tz=360)
    
    for keyword in keywords:
        try:
            pytrends.build_payload(kw_list=[keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
            
            temp = pytrends.interest_over_time().reset_index()
            temp.drop('isPartial', axis=1, inplace=True)
            if dff is None:
                dff = temp
            else:
                dff = pd.merge(dff, temp, on="date")
            
            related_topics = pytrends.related_topics()
            if not related_topics[keyword]['rising'].empty:
                rising = related_topics[keyword]['rising']
                rising = rising[['value', 'topic_title']].rename(columns={'value': f'{keyword}_value', 'topic_title': f'{keyword}_topic'})
                df_related_topics_rising = pd.concat([df_related_topics_rising, rising], axis=1)

            if not related_topics[keyword]['top'].empty:
                top = related_topics[keyword]['top']
                top = top[['value', 'topic_title']].rename(columns={'value': f'{keyword}_value', 'topic_title': f'{keyword}_topic'})
                df_related_topics_top = pd.concat([df_related_topics_top, top], axis=1)

            related_queries = pytrends.related_queries()
            if related_queries[keyword]['rising'] is not None:
                rising = related_queries[keyword]['rising'].rename(columns={'query': f'{keyword}_query', 'value': f'{keyword}_query_value'})
                df_related_queries_rising = pd.concat([df_related_queries_rising, rising], axis=1)
            
            if related_queries[keyword]['top'] is not None:
                top = related_queries[keyword]['top'].rename(columns={'query': f'{keyword}_query', 'value': f'{keyword}_query_value'})
                df_related_queries_top = pd.concat([df_related_queries_top, top], axis=1)
        
        except Exception as e:
            if verbose:
                print(f"Error fetching data for '{keyword}': {e}")
    
    return dff, df_related_topics_rising, df_related_topics_top, df_related_queries_rising, df_related_queries_top
