from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from assignment1.configs import freshTeam
import logging
from parse_csv import getCandidatesData
import urllib2
import datetime
import os


def getTempFileFromUrl(url):
    tempFile = open("Resume_%s.pdf" % datetime.datetime.utcnow(), "wb")
    tempFile.write(urllib2.urlopen(url).read())
    return tempFile


def uploadCandidatesData(candidatesData):

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--headless")

    chromeDriver = webdriver.Chrome(options=chromeOptions)
    chromeDriver.get(freshTeam["CANDIDATES_LIST_URL"])
    condition = expected_conditions.presence_of_element_located((By.ID, "loginSlide"))  # this should be configurable
    WebDriverWait(chromeDriver, freshTeam['LOGIN_REDIRECT_TIMEOUT']).until(condition)

    userNameBox = chromeDriver.find_element_by_xpath('//*[@id="loginSlide"]/div[2]/form/ul/li[1]/input')
    userNameBox.send_keys(freshTeam['USERNAME'])

    passwordBox = chromeDriver.find_element_by_xpath('//*[@id="loginSlide"]/div[2]/form/ul/li[2]/input')
    passwordBox.send_keys(freshTeam['PASSWORD'])

    chromeDriver.find_element_by_xpath('//*[@id="loginSlide"]/div[2]/form/ul/li[3]/input').click()

    signInButton = chromeDriver.find_element_by_xpath('//*[@id="loginSlide"]/div[2]/form/ul/li[4]/button')
    signInButton.click()

    for candidateData in candidatesData:
        addCandidateXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div[1]/button[1]"
        condition = expected_conditions.presence_of_element_located((By.XPATH, addCandidateXpath))  # this should be configurable
        WebDriverWait(chromeDriver, freshTeam['LOGIN_REDIRECT_TIMEOUT']).until(condition)

        addCandidateButton = chromeDriver.find_element_by_xpath(addCandidateXpath)
        addCandidateButton.click()

        firstNameXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div/form/div[1]/input"
        resumeXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/input"

        condition = expected_conditions.presence_of_element_located(
            (By.XPATH, resumeXpath))  # this should be configurable
        WebDriverWait(chromeDriver, freshTeam['LOGIN_REDIRECT_TIMEOUT']).until(condition)

        condition = expected_conditions.presence_of_element_located(
            (By.XPATH, firstNameXpath))  # this should be configurable
        WebDriverWait(chromeDriver, freshTeam['LOGIN_REDIRECT_TIMEOUT']).until(condition)

        lastNameXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div/form/div[3]/input"
        mobileXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div/form/div[5]/input"
        emailXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div/form/div[4]/input"

        d = {'First Name': firstNameXpath, 'Last Name ': lastNameXpath,
             'Mobile Number': mobileXpath, 'Email Address': emailXpath, 'Resume': resumeXpath}

        for key, xpath in d.iteritems():
            data = candidateData[key]
            if key == "Resume":
                tempFile = getTempFileFromUrl(data)
                data = os.path.abspath(tempFile.name)
            field = chromeDriver.find_element_by_xpath(xpath)
            field.send_keys(data)
            if key == "Resume":
                tempFile.close()
                os.remove(data)

        addButtonXpath = "/html/body/div[6]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div/div/div/div[1]/div[3]/button[2]"
        chromeDriver.find_element_by_xpath(addButtonXpath).click()
        logging.info("Uploaded data for %s" % candidateData['Email Address'])

    chromeDriver.quit()


if __name__ == '__main__':
    uploadCandidatesData(getCandidatesData())