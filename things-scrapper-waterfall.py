from selenium import webdriver
import csv
import time
import datetime

urls = [
    ['Air Terjun Gitgit', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g297699-d626130-Reviews-Gitgit_Waterfall-Singaraja_Buleleng_District_Buleleng_Regency_Bali.html'],
    #['Air terjun nung nung', 'Badung', 'https://www.tripadvisor.com/Attraction_Review-g9856222-d7619192-Reviews-Nungnung_Waterfall-Nungnung_Bali.html'],
    #['Air Terjun Dusun Kuning', 'Bangli', 'https://www.tripadvisor.com/Attraction_Review-g1025506-d7050119-Reviews-Kuning_Waterfall-Bangli_Bali.html'],
    #['Air Terjun Melanting', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g608490-d9681544-Reviews-Melanting_Waterfalls-Munduk_Banjar_Buleleng_Regency_Bali.html'],
    #['Air Terjun Singsing', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g1600235-d6516105-Reviews-Singsing_Waterfall-Temukus_Lovina_Beach_Buleleng_District_Buleleng_Regency_Bali.html'],
    #['Air Terjun Banyumala', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g12288293-d9757743-Reviews-Banyumala_Twin_Waterfalls-Wanagiri_Sukasada_Buleleng_Regency_Bali.html'],
    #['Air Terjun Jembong', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g15226464-d9718627-Reviews-Jembong_Waterfall-Gitgit_Sukasada_Buleleng_Regency_Bali.html'],
    #['Air Terjun Kroya', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g297699-d11959092-Reviews-Kroya_Waterfall-Singaraja_Buleleng_District_Buleleng_Regency_Bali.html'],
    #['Air Terjun Aling-aling', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g14121454-d8394554-Reviews-Aling_Aling_Waterfall-Sambangan_Sukasada_Buleleng_Regency_Bali.html'],
    #['Air Terjun Sekumpul', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g297699-d3218339-Reviews-Sekumpul_Waterfalls-Singaraja_Buleleng_District_Buleleng_Regency_Bali.html'],
    #['Air Terjun Bengbengan', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g15648391-d17733303-Reviews-Bengbengan_Waterfall-Lemukih_Sawan_Buleleng_Regency_Bali.html'],
    #['Air Terjun Yeh Mampeh Lemukih', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g1791618-d4496191-Reviews-Yeh_Mempeh_Waterfall-Tejakula_Buleleng_Regency_Bali.html'],
    #['Air Terjun Yeh Mampeh Les', 'Buleleng', 'https://www.tripadvisor.com/Attraction_Review-g1791618-d4496191-Reviews-Yeh_Mempeh_Waterfall-Tejakula_Buleleng_Regency_Bali.html'],
    #['Air Terjun Tegenungan', 'Gianyar', 'https://www.tripadvisor.com/Attraction_Review-g297701-d2643063-Reviews-Tegenungan_Waterfall-Ubud_Gianyar_Regency_Bali.html']
]

path_to_file = "C:/Users/AnggaSuta/Documents/AnggaSuta/project/BuSumartiniProject/webscrapping/ScrapCode/nativeScrap/Result/DATA-WATERFALL-SAMPLE.csv"

csvFile = open(path_to_file, 'a', newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['DESTINATION_NAME', 'TRIPADVISOR_NAME', 'REGION', 'WEB_URL', 'DOWNLOAD_DATE', 'WRITTER', 'WRITTER_ADDRESS', 'REVIEW_DATE', 'EXPERIENCE_DATE', 'RATING', 'TITLE', 'REVIEWER_COMMENT']) 

options = webdriver.ChromeOptions()
options.add_argument('-headless')
options.add_argument('-no-sandbox')
options.add_argument('-disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
sleepTime = 3
print(str(datetime.datetime.now()) + " Start...")

for url in urls:
    print(str(datetime.datetime.now()) + " "+ url[2].replace('https://www.tripadvisor.com', ''))
    wd = webdriver.Chrome(executable_path=r'C:\Users\AnggaSuta\Documents\AnggaSuta\project\BuSumartiniProject\webscrapping\ScrapCode\nativeScrap\chromedriver.exe',options=options)
    wd.get(url[2])

    time.sleep(sleepTime)
    try:
        wd.find_element_by_xpath(".//div[contains(@class='duhwe _T bOlcm dMbup')]").click()
    except Exception as e:
        print(str(datetime.datetime.now()) + " No Readmore ")
    time.sleep(sleepTime)

    companyName = wd.find_element_by_xpath(".//h1[@class='WlYyy cPsXC GeSzT']").text
    print(str(datetime.datetime.now()) + "   ** Company Name:" + companyName)

    nextPage = True
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

        container = wd.find_elements_by_xpath("//div[@class='bPhtn']/div")
        print(str(datetime.datetime.now()) + "   ***** Review count : " + str(len(container)-1))

        for j in range(len(container)-1):
            try:
                title = container[j].find_element_by_xpath(".//span[@class='NejBf']").text
                ratingx = container[j].find_elements_by_xpath(".//*[local-name()='svg'][@class='RWYkj d H0']/*[local-name()='path'][@d='M 12 0C5.388 0 0 5.388 0 12s5.388 12 12 12 12-5.38 12-12c0-6.612-5.38-12-12-12z']")
                rating = str(len(ratingx))
                experienceDate = wd.find_element_by_xpath("//*[@id='tab-data-qa-reviews-0']/div/div[@class='bPhtn']/div["+ str(j+1) +"]/span/span/div[@class='fEDvV']").text

                writter = ''
                try:
                    writter = wd.find_element_by_xpath("//*[@id='tab-data-qa-reviews-0']/div/div[@class='bPhtn']/div["+ str(j+1) +"]/span/span/div[@class='dDwZb f M k']/div[@class='bJyQA f u o']/div[@class='cjhIj']/span[@class='WlYyy cPsXC dTqpp']/a").text           
                except:
                    pass

                writterAddress = ''
                try:
                    writterAddress = wd.find_element_by_xpath("//*[@id='tab-data-qa-reviews-0']/div/div[@class='bPhtn']/div["+ str(j+1) +"]/span/span/div[@class='dDwZb f M k']/div[@class='bJyQA f u o']/div[@class='cjhIj']/div[@class='ddOtn']/div[@class='WlYyy diXIH bQCoY']/span").text
                except:
                    pass

                review = container[j].find_element_by_xpath(".//div[@class='duhwe _T bOlcm']/div/div/span").text.replace("\n", "  ")
                reviewDate = container[j].find_element_by_xpath(".//div[@class='WlYyy diXIH cspKb bQCoY']").text.replace('Written ','').replace(',','')
                csvWriter.writerow([url[0], companyName, url[1], url[2], "'"+str(datetime.datetime.now()), writter, writterAddress, reviewDate, experienceDate, rating, title, review])

                print(str(datetime.datetime.now()) + "   ********** Saving result success ")
            except e:
                print(str(datetime.datetime.now()) + "   ********** ** Saving result FAILED")
                print(str(e))
                pass

        try:
            paginatedUrl = wd.find_element_by_xpath("//*[@id='tab-data-qa-reviews-0']/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a").get_attribute('href')
        except:
            print(str(datetime.datetime.now()) + "   ***** CANNOT FIND NEXT PAGE | FINISH")
            nextPage = False
            
        print('_________________________________________________________')

print(str(datetime.datetime.now()) + "   ***** FINISH *****")
wd.close()