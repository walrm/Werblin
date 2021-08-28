import bs4, requests, time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
load_dotenv()

times = []
#Werblin Sniper
#url = 'https://services.rec.rutgers.edu/Program/GetProgramDetails?courseId=694b3079-a4f9-4988-94d5-6374f9d3fe40&semesterId=61d7fedd-4078-466e-afda-7003ce3123ac'

#College Avenue Gym
url = 'https://services.rec.rutgers.edu/Program/GetProgramDetails?courseId=16f6ea9c-fb20-42d0-afdd-b08fca2bec1f&semesterId=3302ba85-8b33-4145-b755-2d709e0ec9ef'
selection = ""

def get_updates():
     x = requests.get(url)

     soup = bs4.BeautifulSoup(x.text, features="html.parser")
     captions = soup.select('.program-schedule-card-caption')

     times.clear()
     for i in range(len(captions)):
          caption = captions[i]
          x = caption.text.strip().split('\n')
          time_dict = {"Date":x[0].strip(),  "Time":x[4].strip(), "Available":x[6].strip(), "Index":i}
          times.append(time_dict)

def sign_up():
     browser = webdriver.Chrome(executable_path="./chromedriver.exe")
     browser.get(url)

     browser.find_elements_by_link_text("Register")[selection['Index']].click()
     time.sleep(1)

     #Click the NetID Login option
     elem = browser.find_element_by_xpath("/html/body/div[3]/div[4]/div/div/div/div[2]/div[2]/div[2]/div/button")
     elem.click()
     time.sleep(1)

     #Write in netid and password info
     netid = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/form/section/div[1]/input')
     netid.send_keys(os.getenv('NETID'))
     password = browser.find_element_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/form/section/section[1]/div/input')
     password.send_keys(os.getenv('PASSWORD'))
     browser.find_element_by_xpath("/html/body/main/div/div[2]/div[1]/div[2]/form/section/input[4]").click()
     time.sleep(1)

     #Click on the correct register\
     x = browser.find_elements_by_class_name('program-schedule-card')[selection['Index']]
     x.find_element_by_xpath('.//button[text()="Register"]').click()
     time.sleep(2)

     #click all radio buttons and then click checkout
     elem = browser.find_element_by_id("rbtnYes")
     elem.click();
     browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/form[2]/div[2]/button[2]').click()
     time.sleep(3)

     #Checkout process
     browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div/p[2]/button[1]').click()
     browser.find_element_by_id("checkoutButton").click()
     time.sleep(2)
     browser.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div[5]/div/div/div[2]/div/div[2]/button").click()
     time.sleep(60)

if __name__ == '__main__':
     get_updates()
     for i in range(len(times)):
          print(str(i)+".", times[i])

     num = input('Select a date/time:\n')

     selection = times[int(num)]

     while selection['Available'] == 'No Spots Available':
          time.sleep(60)
          get_updates()

          for t in times:
               if selection['Date'] == t['Date'] and selection['Time'] == t['Time']:
                    selection = t
                    print(selection)

     sign_up()
          

     
