url1 = "https://accounts.freshworks.com/login"
url2 = "https://tophire.freshteam.com/"

url = "https://tophire.freshteam.com/hire/jobs/3000023633/candidates/listview"

user = "demo@tophire.co"
pwd = "hello123"


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")

chromeDriver = webdriver.Chrome(options=chromeOptions)
chromeDriver.get(url)
# condition = expected_conditions.url_matches("%s.*"%url1)
condition = expected_conditions.presence_of_element_located((By.ID, "loginSlide"))
WebDriverWait(chromeDriver, 25).until(condition)

print(chromeDriver.page_source)
chromeDriver.quit()
