import requests
from lxml import html
import re
from urllib.parse import urlparse

'''
从南大图书馆电子资源页提取南大购买的各类电子资源域名或IP地址
http://lib.nju.edu.cn/dzzy/dzzy_sjkdh.jsp?urltype=tree.TreeTempUrl&wbtreeid=1013
'''


def extract_domain_or_ip(url):
    parsed_url = urlparse(url)
    
    domain_or_ip = parsed_url.netloc.split(':')[0] if parsed_url.netloc else parsed_url.path.split('/')[0]
    
    return domain_or_ip
    
def get_urls(url):
    # Send a GET request to the target page
    response = requests.get(url)
    
    # Create an HTML tree from the response content
    tree = html.fromstring(response.content)
    
    # Define the XPath expression to select the <a> elements containing the URLs
    xpath_expression = '//*[@id="jiansuo"]/div/div[4]/table/tbody/tr/td/p/a'
    
    # Use the XPath expression to retrieve all matching elements
    elements = tree.xpath(xpath_expression)
    
    # Extract the URLs from the href attributes of the <a> elements
    pattern = r"'(https?://[^']*)'"
    urls = [extract_domain_or_ip(re.search(pattern, element.get('onclick')).group(1)) for element in elements]
    urls = set(urls)
    
    return urls

target_url = 'http://lib.nju.edu.cn/dzzy/dzzy_sjkdh.jsp?urltype=tree.TreeTempUrl&wbtreeid=1013'
urls = get_urls(target_url)

with open('sites.txt', 'w') as f:
  for url in urls:
    f.write(url + '\n')
    print(url)
