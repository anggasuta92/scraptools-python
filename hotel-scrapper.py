from selenium import webdriver
import csv
import time
import datetime

urls = [
    ['PT. Griyatama Abian', 'Denpasar', 'https://www.tripadvisor.com/Hotel_Review-g297700-d2509699-Reviews-Abian_Srama_Hotel_and_Spa-Sanur_Denpasar_Bali.html'],
]

path_to_file = "C:/Users/AnggaSuta/Documents/AnggaSuta/project/BuSumartiniProject/webscrapping/ScrapCode/nativeScrap/Result/DATA-HOTEL-SAMPLE.csv"

csvFile = open(path_to_file, 'a', newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['DESTINATION_NAME', 'TRIPADVISOR_NAME', 'REGION', 'WEB_URL', 'DOWNLOAD_DATE', 'WRITTER', 'WRITTER_ADDRESS', 'REVIEW_DATE', 'EXPERIENCE_DATE', 'RATING', 'TITLE', 'REVIEWER_COMMENT']) 

options = webdriver.ChromeOptions()
options.add_argument('-headless')
options.add_argument('-no-sandbox')
options.add_argument('-disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
sleepTime = 5
print(str(datetime.datetime.now()) + " Start...")

for url in urls:
    print(str(datetime.datetime.now()) + " "+ url[2].replace('https://www.tripadvisor.com', ''))
    wd = webdriver.Chrome(executable_path=r'C:\Users\AnggaSuta\Documents\AnggaSuta\project\BuSumartiniProject\webscrapping\ScrapCode\nativeScrap\chromedriver.exe',options=options)
    wd.get(url[2])

    time.sleep(sleepTime)
    # try:
    #     wd.find_element_by_xpath(".//div[contains(@class='duhwe _T bOlcm dMbup')]").click()
    # except Exception as e:
    #     print(str(datetime.datetime.now()) + " No Readmore ")
    # time.sleep(sleepTime)

    companyName = wd.find_element_by_xpath("//*[@id='HEADING']").text
    print(str(datetime.datetime.now()) + "   ** Company Name:" + companyName)

    nextPage = True
    firstPage = True
    paginatedUrl = url[2]
    while nextPage:
        print(str(datetime.datetime.now()) + "   ***** Getting detail: " + paginatedUrl.replace('https://www.tripadvisor.com', ''))
        wd.get(paginatedUrl)
        time.sleep(sleepTime)
        try:
            readMores = wd.find_elements_by_xpath("//div[@class='duhwe _T bOlcm dMbup']")
            for c in range(len(readMores)):
                readMores[c].click()
        except:
            print(str(datetime.datetime.now()) + "   ***** No Readmore")
        
        time.sleep(sleepTime)

        container = wd.find_elements_by_xpath("//*[@id='component_16']/div/div[3]/div[@class='cWwQK MC R2 Gi z Z BB dXjiy']")
        print(str(datetime.datetime.now()) + "   ***** Review count : " + str(len(container)))

        for j in range(len(container)):
            try:
                title = ''
                try:
                    title = container[j].find_element_by_xpath(".//div[2]/div[2]/a/span/span").text
                except:
                    title = container[j].find_element_by_xpath(".//div[3]/div[2]/a/span/span").text
                    pass

                rating = ''
                try:
                    rating = container[j].find_element_by_xpath(".//div[2]/div[1]/div/span").get_attribute("class").split("_")[3]
                except:
                    rating = container[j].find_element_by_xpath(".//div[3]/div[1]/div/span").get_attribute("class").split("_")[3]
                    pass

                experienceDate = ''
                try:
                    experienceDate = container[j].find_element_by_xpath(".//div[2]/div[3]/span[1]").text
                except:
                    experienceDate = container[j].find_element_by_xpath(".//div[3]/div[3]/span[1]").text
                    pass

                writter = ''
                try:
                    writter = container[j].find_element_by_xpath(".//div[1]/div/div[2]/span/a").text           
                except:
                    pass

                writterAddress = ''
                try:
                    writterAddress = container[j].find_element_by_xpath(".//div[1]/div/div[3]/span[1]/span").text
                except:
                    pass

                review = ''
                try:
                    review = container[j].find_element_by_xpath(".//div[2]/div[3]/div[1]/div[1]/q/span").text.replace("\n", "  ")
                except:
                    review = container[j].find_element_by_xpath(".//div[3]/div[3]/div[1]/div[1]/q/span").text.replace("\n", "  ")
                    pass

                reviewDate = container[j].find_element_by_xpath(".//div[1]/div/div[2]/span").text.replace(' wrote a review ','').replace(',','')

                csvWriter.writerow([url[0], companyName, url[1], url[2], "'"+str(datetime.datetime.now()), writter, writterAddress, reviewDate, experienceDate, rating, title, review])
                print(str(datetime.datetime.now()) + "   ********** Saving result success ")
            except e:
                print(str(datetime.datetime.now()) + "   ********** ** Saving result FAILED")
                print(str(e))
                pass

        try:
            if(firstPage):
                paginatedUrl = wd.find_element_by_xpath("//*[@id='component_16']/div/div[3]/div[8]/div/a").get_attribute('href')
                firstPage = False
            else:
                paginatedUrl = wd.find_element_by_xpath("//*[@id='component_16']/div/div[3]/div[8]/div/a[2]").get_attribute('href')
        except:
            print(str(datetime.datetime.now()) + "   ***** CANNOT FIND NEXT PAGE | FINISH")
            nextPage = False
            
        print('_________________________________________________________')

print(str(datetime.datetime.now()) + "   ***** FINISH *****")
wd.close()