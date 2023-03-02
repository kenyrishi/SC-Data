#go to https://www.scc-csc.ca/case-dossier/cb/index-eng.aspx
#get list of case numbers

#for each case number
#go to https://www.scc-csc.ca/case-dossier/cb/2022/39875-eng.aspx
#or https://www.scc-csc.ca/case-dossier/cb/2022/39480-39481-eng.aspx
#pick out breakdown of decision

#for each split names into majority/dissenting

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions
import csv

names = ['Wagner','Moldaver','Karakatsanis','Côté','Brown','Rowe','Martin','Kasirer','Jamal']
prevNames = ['Gascon','Cromwell','Rothstein','Charron','McLachlin','Abella']
majWords = ["Unanimous","Majority","Concurring"]
minWords = ["Dissenting"]


def setup():
    options = EdgeOptions()
    options.add_argument("--headless")
    driver = webdriver.Edge(options=options)
    return driver

def find_nums(year):
    driver.get('https://www.scc-csc.ca/case-dossier/cb/index-eng.aspx')
    time.sleep(2)
    f = open("test.txt","w")
    for i in range (2,41):
        xpath = '//*[@id="'+year+'"]/table/thead/tr['+str(i)+']/td[3]' 
        element = driver.find_element(By.XPATH, xpath)
        f.write(element.text)
        f.write('\n')
        print(element.text)
    f.close()
  
    #info = element.text
    #f = open("test.txt", "a")
    #f.write(info)
    #f.close()


def get_nums_to_list():
    f = open("test.txt","r")
    r = f.read()
    d = r.split("\n")
    f.close()
    return d

def visit_nums(driver, ids, year):
    with open('csvfile.csv','w',newline='') as f:
        w = csv.writer(f)
                
        for num in ids:
            site = 'https://scc-csc.ca/case-dossier/cb/'+year+'/'+num+'-eng.aspx'
            driver.get(site)
            info = []
            info.append(num)

            title = '//*[@id="wb-main-in"]/h2'
            info.append(driver.find_element(By.XPATH,title).text)

            date = '//*[@id="wb-main-in"]/div[4]/div[1]/ul/li[2]'
            info.append(driver.find_element(By.XPATH,date).text)
            
            summary = '//*[@id="wb-main-in"]/p[1]/strong'
            info.append(driver.find_element(By.XPATH,summary).text)

            try:
                decision='//*[@id="wb-main-in"]/div[4]/div[1]/ul/li[4]/ul'
                text = driver.find_element(By.XPATH,decision).text
            except:
                decision='//*[@id="wb-main-in"]/div[4]/div[1]/ul/li[5]/ul'
                text = driver.find_element(By.XPATH,decision).text
            info.append(text)

            w.writerow(info)

        f.close()

        
def parse_decisions():
    with open('csvfile.csv','r') as f:
         with open('completefile.csv','w',newline='') as f2:
            r = csv.reader(f)
            w = csv.writer(f2)
            w.writerow(["Case Number", "Case Name", "Date", "Judgement","Summary","Result","Count","Majority","Minority"])
            for row in r:
                decision = row[4]
                val = ''
                rules = decision.split('\n')
                print(decision)
                if 'dismissed' in rules[0]:
                    val = 'dismissed'
                elif 'allowed' in rules[0]:
                    val = 'allowed'

                majNames = []
                minNames = []
                for line in rules:
                    if any(word in line for word in majWords):
                        for name in names:
                            if name in line:
                                majNames.append(name)
                    elif any(word in line for word in minWords):
                        for name in names:
                            if name in line:
                                minNames.append(name)
                count = str(len(majNames)) + " to " + str(len(minNames))

                row.append(val)
                row.append(count)
                row.append(','.join(majNames))
                row.append(','.join(minNames))
                w.writerow(row)
                        
            f.close()
            f2.close()


def find_similar():
    with open('completefile.csv','r') as f:
        r = csv.reader(f)
        next(r)

        data = []
        for i in names:
            p = []
            for j in names:
                p.append([0,0])
            p.append([0,0])
            data.append(p)

        for row in r:
            majN = row[7].split(',')
            minN = row[8].split(',')
            for i in range(len(names)):
                if names[i] in majN:
                    data[i][-1][0] += 1
                if names[i] in minN:
                    data[i][-1][1] += 1
                    
                for j in range(len(names)):
                    if names[i] in majN and names[j] in majN or names[i] in minN and names[j] in minN:
                        data[i][j][0] += 1
                        data[i][j][1] += 1
                    elif names[i] in majN and names[j] in minN or names[i] in minN and names[j] in majN:
                        data[i][j][1] += 1
            print(majN,minN)

        f.close()

        with open('similarity.csv','w',newline='') as f2:
            w = csv.writer(f2)
            header = ['']
            header.extend(names)
            header.append("Majority")
            w.writerow(header)
            for i in range(len(data)):
                l = [names[i]]
                for j in range(len(data[i])-1):
                    l.append(data[i][j][0]/data[i][j][1])
                l.append(data[i][-1][0]/(data[i][-1][0]+data[i][-1][1]))
                w.writerow(l)
            f2.close()    
                

        

def main():
    #driver = setup()
    #ids = get_nums_to_list()
    #visit_nums(driver,ids)
    find_similar()
    #driver.quit()

main()
