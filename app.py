from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from assignment1.configs import freshTeam
import logging
from parse_csv import getCandidatesData


logger = logging.getLogger(__name__)

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")

chromeDriver = webdriver.Chrome(options=chromeOptions)
chromeDriver.get(freshTeam['LOGIN_URL'])
condition = expected_conditions.presence_of_element_located((By.ID, "loginSlide"))  # this should be configurable
WebDriverWait(chromeDriver, freshTeam['LOGIN_REDIRECT_TIMEOUT']).until(condition)

userNameBox = chromeDriver.find_element_by_xpath('//*[@id="ember452"]')
userNameBox.send_keys(freshTeam['USERNAME'])

passwordBox = chromeDriver.find_element_by_xpath('//*[@id="ember453"]')
passwordBox.send_keys(freshTeam['PASSWORD'])

signInButton = chromeDriver.find_element_by_xpath('//*[@id="loginSlide"]/div[2]/form/ul/li[4]/button')
signInButton.click()

candidatesData = getCandidatesData()

for candidateData in candidatesData:
    chromeDriver.get(freshTeam["CANDIDATES_LIST_URL"])

    condition = expected_conditions.presence_of_element_located((By.ID, "ember327"))  # this should be configurable
    WebDriverWait(chromeDriver, freshTeam['LOGIN_REDIRECT_TIMEOUT']).until(condition)

    addCandidateButton = chromeDriver.find_element_by_xpath('//*[@id="ember327"]')
    addCandidateButton.click()

    firstNameXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div/form/div[1]/input"

    condition = expected_conditions.presence_of_element_located((By.XPATH, firstNameXpath))  # this should be configurable
    WebDriverWait(chromeDriver, freshTeam['LOGIN_REDIRECT_TIMEOUT']).until(condition)

    lastNameXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div/form/div[3]/input"
    mobileXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div/form/div[5]/input"
    emailXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div/form/div[4]/input"

    d = {'First Name': firstNameXpath, 'Last Name ': lastNameXpath,
         'Mobile Number': mobileXpath, 'Email Address': emailXpath}

    for key, xpath in d.iteritems():
        field = chromeDriver.find_element_by_xpath(xpath)
        field.send_keys(candidateData[key])

    addButtonXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[1]/div[3]/button[2]"
    chromeDriver.find_element_by_xpath(addButtonXpath).click()

chromeDriver.quit()
