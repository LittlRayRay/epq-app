from selenium import webdriver
from selenium.webdriver.common.by import By

def crawl_site():
    driver=webdriver.Chrome()

    base_url = 'https://www.ifixit.com/Guide'
    
    guide_urls = {}
    visited = []
    url_tc = ["https://www.ifixit.com/Guide"]
    while url_tc:
        curr_url = url_tc.pop(0)
        try: 
            driver.get(curr_url)
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href=link.get_attribute("href")
        
                if href.startswith(base_url) and href not in guide_urls.keys():
                    guide_urls[href] = link.text
                    print(f"{href}: {link.text}")
        

                if href.startswith("https://www.ifixit.com") and href not in visited: 
                    url_tc.append(href)
                    visited.append(href)
        except:
            pass
    with open("save.csv", "w", newline='') as file:
       writer=csv.writer(file)
       field = ["url", "title"]
       for url in guide_urls.keys():
           writer.writerow([url, guide_urls[url]])

crawl_site()
