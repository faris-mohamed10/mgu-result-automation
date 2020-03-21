import inquirer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

select_list = []
answers1 = inquirer.prompt([
    inquirer.Text('url', message="Enter the full URL"),
    inquirer.Text('reg', message="Enter first roll number of your class",),
    inquirer.Text('lreg', message="Enter last roll number of your class",),
])

regno = int(answers1['reg'])
last_regno = int(answers1['lreg'])
URL = answers1['url'] 

driver = webdriver.Firefox()
driver.set_window_position(0, 0)
driver.set_window_size(512, 384)

driver.get(answers1['url']) #open the url 
for element in Select(driver.find_element_by_id('exam_id')).options:
    select_list.append(element.get_attribute("text"))
del select_list[0]
print(select_list) 

answers2 = inquirer.prompt([
    inquirer.List('exam',
                message="select your exam",
                choices=select_list,
            ),
])
driver.maximize_window()

while regno < last_regno:
    driver.get(URL) #open the url 
    Select(driver.find_element_by_id('exam_id')).select_by_visible_text(answers2['exam'])
    driver.find_element_by_id('prn').send_keys(regno) #enter the roll number
    driver.find_element_by_id('btnresult').click() #click the get result button 
    
    try:
        if(driver.find_element_by_class_name('msg_td_red')): #if result is not found screenshot is not taken
            print("result not found")
    except:
        print('result found for '+ str(regno))  
        driver.execute_script("window.scrollTo(0, 100)") #window is scrolled to adjust the screenshot location
        driver.save_screenshot('results/'+str(regno)+'.png') #screenshot is saved to a location
        regno+=1
        
driver.close()