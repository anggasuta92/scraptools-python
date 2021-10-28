from tkinter import *
import tkinter
from tkinter import font
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox 
import datetime
import textwrap
from selenium import webdriver
import csv
import time
import os

path_to_file = ""
sleepTime = 5
options = webdriver.ChromeOptions()
options.add_argument('-headless')
options.add_argument('-no-sandbox')
options.add_argument('-disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
appPath = os.getcwd()
wd = ""
allSuccess = True

def file_save():
    global path_to_file
    global wd
    global allSuccess

    txtLogs.delete("1.0", END)
    strUrl = txtSearch.get("1.0", END)
    wd = webdriver.Chrome(executable_path=r''+appPath+'\chromedriver.exe',options=options)

    reviewType = ""
    if(strUrl.find("Attraction_Review")>=0):
        reviewType = "attraction"
    elif(strUrl.find("Restaurant_Review")>=0):
        reviewType = "restaurant"
        #reviewType = ""
    elif(strUrl.find("Hotel_Review")>=0):
        reviewType = "hotel"

    if(reviewType!=""):
        f = asksaveasfile(initialfile = (reviewType + '.csv'), defaultextension=".csv",filetypes=[("Comma Delimitted Doc","*.csv")])
        path_to_file = f.name

        addLogs("PROCCESS STARTED")

        if(reviewType.find("attraction")>=0):
            scrap_things(strUrl)
        elif(reviewType.find("restaurant")>=0):
            scrap_restaurant(strUrl)
        elif(reviewType.find("hotel")>=0):
            scrap_hotels(strUrl)

        addLogs("************ Process completed ************")
        if allSuccess:
            messagebox.showinfo("Information", "Proccess completed")
        else:
            messagebox.showwarning("Warning", "Process completed with error(s)")

        wd.close()

    else:
        msg = "URL '"+ strUrl.strip() +"' unrecognized"
        messagebox.showwarning("Warning", msg)
        addLogs(msg)

def scrap_things(url):
    global path_to_file
    global sleepTime
    global wd
    global window
    global allSuccess

    csvFile = open(path_to_file, 'a', newline='', encoding="utf-8")
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['TRIPADVISOR_NAME', 'WEB_URL', 'DOWNLOAD_DATE', 'WRITTER', 'WRITTER_ADDRESS', 'REVIEW_DATE', 'EXPERIENCE_DATE', 'RATING', 'TITLE', 'REVIEWER_COMMENT']) 
    window.update()
    wd.get(url)
    window.update()
    time.sleep(sleepTime)

    try:
        wd.find_element_by_xpath(".//div[contains(@class='duhwe _T bOlcm dMbup')]").click()
    except Exception as e:
        pass

    time.sleep(sleepTime)
    companyName = ""
    try:
        companyName = wd.find_element_by_xpath(".//h1[@class='WlYyy cPsXC GeSzT']").text
        addLogs("Company Name : " + companyName)
    except:
        try:
            companyName = wd.find_element_by_xpath("//html/body/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/h1").text
            addLogs("Company Name : " + companyName)
        except:
            addLogs("Failed to get data, please check your URL...")
            allSuccess = False
            return

    nextPage = True
    paginatedUrl = url
    while nextPage:
        addLogs("Getting detail: " + paginatedUrl.replace('https://www.tripadvisor.com', ''))
        
        window.update()
        wd.get(paginatedUrl)
        window.update()
        
        time.sleep(sleepTime)
        window.update()

        try:
            readMores = wd.find_elements_by_xpath("//div[@class='duhwe _T bOlcm dMbup']")
            for c in range(len(readMores)):
                readMores[c].click()
        except:
            pass
        
        window.update()
        time.sleep(sleepTime)
        window.update()

        container = []
        try:
            container = wd.find_elements_by_xpath("//div[@class='bPhtn']/div")
        except:
            container = wd.find_elements_by_xpath("//*[@id='component_10']/div[5]/div[3]/div/div[@class='eVykL Gi z cPeBe MD cwpFC']")

        if(len(container)<11):
            addLogs("Total review : " + str(len(container)))
        else:
            addLogs("Total review : " + str(len(container)-1))

        for j in range(len(container)):
            if(j<10):
                isPagination = False
                try:
                    pg = container[j].find_element_by_xpath(".//div[@class='fQGNe c']")
                    if not pg:
                        isPagination = False
                    else:
                        isPagination = True
                except:
                    pass

                if(isPagination==False):
                    try:
                        #title = container[j].find_element_by_xpath(".//span[@class='NejBf']").text
                        title = container[j].find_element_by_xpath(".//div[@class='WlYyy cPsXC bLFSo cspKb dTqpp']/span[@class='NejBf']").text
                        
                        ratingx = container[j].find_elements_by_xpath(".//*[local-name()='svg'][@class='RWYkj d H0']/*[local-name()='path'][@d='M 12 0C5.388 0 0 5.388 0 12s5.388 12 12 12 12-5.38 12-12c0-6.612-5.38-12-12-12z']")
                        rating = str(len(ratingx))
                        experienceDate = ''
                        try:
                            wd.find_element_by_xpath("//*[@id='tab-data-qa-reviews-0']/div/div[@class='bPhtn']/div["+ str(j+1) +"]/span/span/div[@class='fEDvV']").text
                        except:
                            print()

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
                        csvWriter.writerow([companyName, url, "'"+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), writter, writterAddress, reviewDate, experienceDate, rating, title, review])

                        addLogs(title + "Data Saved")
                    except e:
                        addLogs("Saving result FAILED " + e.args[0])
                        allSuccess = False
                        pass

        try:
            paginatedUrl = wd.find_element_by_xpath("//*[@id='tab-data-qa-reviews-0']/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a").get_attribute('href')
        except:
            addLogs("CANNOT FIND NEXT PAGE")
            nextPage = False

def scrap_restaurant(url):
    global path_to_file
    global sleepTime
    global wd
    global window
    global allSuccess

    csvFile = open(path_to_file, 'a', newline='', encoding="utf-8")
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['TRIPADVISOR_NAME', 'PRICE_RANGE', 'WEB_URL', 'DOWNLOAD_DATE', 'WRITTER', 'WRITTER_ADDRESS', 'REVIEW_DATE', 'EXPERIENCE_DATE', 'RATING', 'VALUE_RATING', 'ATMOSPHERE_RATING', 'SERVICE_RATING', 'FOOD_RATING', 'TRIP_TYPE', 'TITLE', 'REVIEWER_COMMENT']) 
    window.update()
    wd.get(url)
    window.update()
    time.sleep(sleepTime)

    companyName = ""
    try:
        companyName = wd.find_element_by_xpath("//html/body/div[2]/div[1]/div/div[4]/div/div/div[1]/h1").text
        print("companyName: " + companyName)
    except:
        try:
            companyName = wd.find_element_by_xpath("//html/body/div[2]/div[1]/div/div[3]/div/div/div[1]/h1").text
            print("companyName: " + companyName)
        except:
            addLogs("Failed to get data, please check your URL...")
            allSuccess = False
            return

    priceRange = ''
    try:
        priceRange = wd.find_element_by_xpath("//html/body/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]").text
    except:
        print()

    nextPage = True
    firstPage = True
    paginatedUrl = url

    while nextPage:
        addLogs("Getting detail: " + paginatedUrl.replace('https://www.tripadvisor.com', ''))
        window.update()
        wd.get(paginatedUrl)
        window.update()
        time.sleep(sleepTime)
        window.update()
        try:
            clicked = False
            readMores = []
            try:
                readMores = wd.find_elements_by_xpath("//*[contains(@id, 'review_')]/div/div[2]/div[2]/div/p/span[@class='taLnk ulBlueLinks']")
            except:
                readMores = wd.find_elements_by_xpath("//*[contains(@id, 'review_')]/div/div[2]/div[2]/div/p/span[@class='taLnk ulBlueLinks']")

            for c in range(len(readMores)):
                if(clicked==False):
                    readMores[c].click()
                    clicked = True
                    print("READMORE KLICKED")
        except:
            print()
        
        time.sleep(sleepTime)

        container = wd.find_elements_by_xpath("//*[@id='taplc_location_reviews_list_resp_rr_resp_0']/div/div[not(@class) or @class='mobile-more']")
        totalContainer = len(container)
        if(totalContainer>10) : 
            totalContainer = totalContainer - 1
        else:
            if(firstPage==False) : totalContainer = totalContainer - 1

        addLogs("   ***** Review count : " + str(totalContainer))

        for j in range(totalContainer):
            try:
                title = ''
                try:
                    title = container[j].find_element_by_xpath(".//*[contains(@id,'review_')]/div/div[2]/div[1]").text
                except:
                    title = container[j].find_element_by_xpath(".//div[3]/div/div/div/div[2]/div[@class='quote']/a/span").text
                rating = ''
                try:
                    rating = container[j].find_element_by_xpath(".//*[contains(@id,'review_')]/div/div[2]/span[1]").get_attribute("class").split("_")[3]
                except:
                    print("rating not found")

                experienceDate = ''
                try:
                    experienceDate = container[j].find_element_by_xpath(".//div/div[2]/div[3]").text
                    if(experienceDate==""):
                        experienceDate = container[j].find_element_by_xpath(".//div/div[2]/div[4]").text
                except:
                    experienceDate = container[j].find_element_by_xpath(".//div/div[2]/div[4]").text
                    print("exp date not found")

                writter = ''
                try:
                    writter = container[j].find_element_by_xpath(".//*[contains(@id, 'UID_')]/div[2]/div").text
                except:
                    print("writer not found")

                writterAddress = ''
                try:
                    #writterAddress = container[j].find_element_by_xpath(".//*[contains(@id, 'UID_')]/div[2]/div[2]/strong").text
                    writterAddress = container[j].find_element_by_xpath(".//*[contains(@id,'UID_')]/div[2]/div[@class='userLoc']").text
                    #writterAddress = wd.find_element_by_xpath("//html/body/div[2]/div[2]/div[2]/div[6]/div/div[1]/div[4]/div/div[5]/div/div["+ (j+2) +"]/div[3]/div/div/div/div[1]/div/div/div[1]/div[2]/div[2]").text
                except:
                    print("address not found")

                review = ''
                try:
                    review = container[j].find_element_by_xpath(".//*[contains(@id,'review_')]/div/div[2]/div[2]/div/p").text.replace("\n", "  ")
                except:
                    print("review not found")

                tripType = ''
                reviewDate = container[j].find_element_by_xpath(".//*[contains(@id,'review_')]/div/div[2]/span[2]").text

                valueRating = ""
                try:
                    valueRating = rating = container[j].find_element_by_xpath(".//*[contains(@id,'review_')]/div/div[2]/div[4]/div/ul/li/ul[1]/li[1]/div[1]").get_attribute("class").split("_")[3]
                except:
                    pass

                atmosphereRating = ""
                try:
                    atmosphereRating = rating = container[j].find_element_by_xpath(".//*[contains(@id,'review_')]/div/div[2]/div[4]/div/ul/li/ul[1]/li[2]/div[1]").get_attribute("class").split("_")[3]
                except:
                    pass

                serviceRating = ""
                try:
                    serviceRating = rating = container[j].find_element_by_xpath(".//*[contains(@id,'review_')]/div/div[2]/div[4]/div/ul/li/ul[2]/li[1]/div[1]").get_attribute("class").split("_")[3]
                except:
                    pass

                foodRating = ""
                try:
                    foodRating = rating = container[j].find_element_by_xpath(".//*[contains(@id,'review_')]/div/div[2]/div[4]/div/ul/li/ul[2]/li[2]/div[1]").get_attribute("class").split("_")[3]
                except:
                    pass

                csvWriter.writerow([companyName, priceRange, url, "'"+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), writter, writterAddress, reviewDate, experienceDate, rating, valueRating, atmosphereRating, serviceRating, foodRating, tripType, title, review])
                addLogs("Saving result success")
            except Exception as e:
                addLogs("Saving result FAILED " + e.args[0])
                allSuccess = False

        try:
            print("FIRSTPAGE: " + str(firstPage))
            if(firstPage):
                try:
                    paginatedUrl = wd.find_element_by_xpath("//html/body/div[2]/div[2]/div[2]/div[6]/div/div[1]/div[4]/div/div[5]/div/div[13]/div/div/a[2]").get_attribute('href')
                except:
                    paginatedUrl = wd.find_element_by_xpath("//*[@id='taplc_location_reviews_list_resp_rr_resp_0']/div/div[12]/div/div/a[2]").get_attribute('href')

                firstPage = False
            else:
                try:
                    paginatedUrl = wd.find_element_by_xpath("//*[@id='taplc_location_reviews_list_resp_rr_resp_0']/div/div[12]/div/div/a[2]").get_attribute('href')
                except:
                    print("Halaman next gak ketemu")
                    nextPage = False
        except:
            addLogs("CANNOT FIND NEXT PAGE")
            nextPage = False

def scrap_hotels(url):
    global path_to_file
    global sleepTime
    global wd
    global window
    global allSuccess

    csvFile = open(path_to_file, 'a', newline='', encoding="utf-8")
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['TRIPADVISOR_NAME', 'PRICE', 'WEB_URL', 'DOWNLOAD_DATE', 'WRITTER', 'WRITTER_ADDRESS', 'REVIEW_DATE', 'EXPERIENCE_DATE', 'RATING', 'TRIP_TYPE', 'TITLE', 'REVIEWER_COMMENT']) 
    window.update()
    wd.get(url)
    window.update()

    companyName = ""
    try:
        companyName = wd.find_element_by_xpath("//*[@id='HEADING']").text
    except:
        addLogs("Failed to get data, please check your URL...")
        allSuccess = False
        return

    price = "0"
    try:
        price = wd.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[7]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[2]").text
    except:
        try:
            price = wd.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[7]/div/div/div/div[2]/a/div/div[2]/div[@class='vyNCd b Wi']").text
        except:
            try:
                price = wd.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[7]/div/div/div[1]/div[3]/div/div[2]/div/div[@class='fzleB b']").text
            except:
                try:
                    price = wd.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[7]/div/div/div[1]/div[2]/a/div[1]/div[2]/div[2]").text
                except:
                    try:
                        price = wd.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[7]/div/div/div[1]/div[2]/a/div[1]/div[2]/div[@class='vyNCd b Wi']").text
                    except:
                        try:
                            price = wd.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[7]/div/div/div[1]/div[2]/a/div/div[2]/div[@class='vyNCd b Wi']").text
                        except:    
                            addLogs("Harga tidak ditemukan....")
                

    nextPage = True
    firstPage = True
    paginatedUrl = url

    while nextPage:
        addLogs("Getting detail: " + paginatedUrl.replace('https://www.tripadvisor.com', ''))
        window.update()
        wd.get(paginatedUrl)
        window.update()
        time.sleep(sleepTime)
        window.update()
        try:
            readMores = wd.find_elements_by_xpath("//div[@class='duhwe _T bOlcm dMbup']")
            for c in range(len(readMores)):
                readMores[c].click()
        except:
            pass
        
        time.sleep(sleepTime)

        container = wd.find_elements_by_xpath("//*[@id='component_16']/div/div[3]/div[@class='cWwQK MC R2 Gi z Z BB dXjiy']")
        if(len(container)<=0):
            container = wd.find_elements_by_xpath("//*[@id='component_15']/div/div[3]/div[@class='cWwQK MC R2 Gi z Z BB dXjiy']")
            
        addLogs("   ***** Review count : " + str(len(container)))

        for j in range(len(container)):
            try:
                title = ''
                try:
                    title = container[j].find_element_by_xpath(".//div[2]/div[2]/a/span/span").text
                except:
                    try:
                        title = container[j].find_element_by_xpath(".//div[3]/div[2]/a/span/span").text
                    except:
                        title = container[j].find_element_by_xpath(".//div[2]/div[3]/a/span/span").text
                    # pass

                rating = ''
                try:
                    rating = container[j].find_element_by_xpath(".//div[2]/div[1]/div/span").get_attribute("class").split("_")[3]
                except:
                    try:
                        rating = container[j].find_element_by_xpath(".//div[3]/div[1]/div/span").get_attribute("class").split("_")[3]
                    except:
                        rating = container[j].find_element_by_xpath(".//div[2]/div[2]/div/span").get_attribute("class").split("_")[3]
                    # pass

                experienceDate = ''
                try:
                    experienceDate = container[j].find_element_by_xpath(".//div[3]/div[3]/span[1]").text
                    if(experienceDate==""):
                        experienceDate = container[j].find_element_by_xpath(".//div[2]/div[3]/span[1]").text
                except:
                    try:
                        experienceDate = container[j].find_element_by_xpath(".//div[2]/div[3]/span[1]").text
                    except:
                        print()
                    # pass

                writter = ''
                try:
                    writter = container[j].find_element_by_xpath(".//div[1]/div/div[2]/span/a").text           
                except:
                    print()

                writterAddress = ''
                try:
                    writterAddress = container[j].find_element_by_xpath(".//div[1]/div/div[3]/span[1]/span").text
                except:
                    print()

                review = ''
                try:
                    review = container[j].find_element_by_xpath(".//div[2]/div[3]/div[1]/div[1]/q/span").text.replace("\n", "  ")
                except:
                    try:
                        review = container[j].find_element_by_xpath(".//div[3]/div[3]/div[1]/div[1]/q/span").text.replace("\n", "  ")
                    except:
                        review = container[j].find_element_by_xpath(".//div[2]/div[4]/div[1]/div[1]/q/span").text.replace("\n", "  ")

                tripType = ''
                try:
                    tripType = container[j].find_element_by_xpath(".//div[3]/div[3]/span[2]").text
                    if(tripType==""):
                        try:
                            tripType = container[j].find_element_by_xpath(".//div[2]/div[3]/span[2]").text
                        except:
                            print()
                except:
                    try:
                        tripType = container[j].find_element_by_xpath(".//div[2]/div[3]/span[2]").text
                    except:
                        print()

                #reviewDate = container[j].find_element_by_xpath(".//div[1]/div/div[2]/span").text.replace(' wrote a review ','').replace(',','')
                reviewDate = container[j].find_element_by_xpath(".//div[1]/div/div[2]/span").text.split(' wrote a review ')[1].replace(',','')

                csvWriter.writerow([companyName, price, url, "'"+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), writter, writterAddress, reviewDate, experienceDate, rating, tripType, title, review])
                addLogs("Saving result success")
            except Exception as e:
                addLogs("Saving result FAILED " + e.args[0])
                allSuccess = False
                print()

        try:
            if(firstPage):
                paginatedUrl = wd.find_element_by_xpath("//*[@id='component_16']/div/div[3]/div[8]/div/a").get_attribute('href')
                firstPage = False
            else:
                paginatedUrl = wd.find_element_by_xpath("//*[@id='component_16']/div/div[3]/div[8]/div/a[2]").get_attribute('href')
        except:
            try:
                if(firstPage):
                    paginatedUrl = wd.find_element_by_xpath("//html/body/div[2]/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/div/div[3]/div[8]/div/a").get_attribute('href')
                    firstPage = False
                else:
                    paginatedUrl = wd.find_element_by_xpath("//html/body/div[2]/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/div/div[3]/div[8]/div/a[2]").get_attribute('href')
            except:
                addLogs("CANNOT FIND NEXT PAGE")
                nextPage = False

def addLogs(logs):
    global window
    dt = datetime.datetime.now()
    dt = (dt.strftime("%Y-%m-%d %H:%M:%S") + " : ")
    emsg = dt +logs
    emsg = textwrap.fill(emsg, initial_indent='', subsequent_indent=' ' * 22, width=100)

    newLogs = txtLogs.get("1.0", END)
    if(len(newLogs)>0):
        newLogs += ""
    newLogs += emsg
    
    txtLogs.delete("1.0", END)
    txtLogs.insert("1.0", newLogs)
    window.update()
    txtLogs.see(tkinter.END)
    window.update()

window = Tk()
window.title('TripAdvisor Scrapp Apps | 20211028.2146')
window.geometry("900x600")
window.resizable(0,0)

lbl=Label(window, text="Masukkan URL Trip Advisor dibawah ini", fg='black', font=("Consolas", 12))
lbl.place(x=5, y=5)

txtSearch=Text(window,font=("Consolas", 13), height=2, width=90)
txtSearch.place(x=7, y=27)

btnSearch=Button(window, text="Simpan", font=("Consolas", 10), bg="black", fg="white", width=8, height=2, command=file_save)
btnSearch.place(x=825, y=27)

txtLogs=Text(window, fg="white", bg="black", height=32, width=110)
txtLogs.place(x=7,y=77)

window.geometry("+{}+{}".format(0, 0))
window.mainloop()