import time, sys
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from requests import request as rq
from selenium.webdriver import Chrome, ChromeOptions
from random import randint
import datetime
import schedule
import pandas as pd
import tweepy


class AutoTweet:
    # herokuのchromedriverのPATHを指定
    driver_path = '/app/.chromedriver/bin/chromedriver'
    options = ChromeOptions()
    options.add_argument('-headless')
    def __init__(self,yourId,yourPassWord,filename):
        self.driver = webdriver.Chrome(opitons=options,executable_path=driver_path)
        self.yourId = yourId
        self.yourPassWord = yourPassWord
        self.df = pd.read_csv(filename)

    def Login(self):
        url = "https://twitter.com/login"
        self.driver.get(url)

        print(self.driver.current_url)
        """
        self.driver.find_element_by_xpath('//*[@id="doc"]/div/div[1]/div[1]/div[2]/div[2]/div/a[2]').click()
        """
        time.sleep(5)
        id = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[1]/label/div/div[2]/div/input')
        id.send_keys(self.yourId)
        time.sleep(5)
        password = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[2]/label/div/div[2]/div/input')
        password.send_keys(self.yourPassWord)
        time.sleep(5)
        print(self.driver.current_url)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[3]/div/div').click()

    def tweet(self,twi):
        """
            引数で渡された文章をツイートする関数。
            tweetは140文字以内。
        """
        if len(twi) > 140:
            print("This tweet is too long")
        else:
            try:
                elem = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/header/div/div/div/div/div[3]/a/div')
                elem.click()
                print(tmp)
                time.sleep(5)
                elem = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div/div/div/div[2]/div')
                elem.click()
                print(tmp)
                time.sleep(5)
                print("before send key")
                time.sleep(5)
                elem.send_keys(twi)
                time.sleep(5)
                print("input_done")
                time.sleep(5)
                elem = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div/span/span')
                elem.click()
                print("OK")
                elem.send_keys(Keys.CONTROL, Keys.ENTER)

            except KeyboardInterrupt:
                print("\nprogram was ended.\n")
                sys.exit()
            
            except:
                url = "https://twitter.com/home"
                self.driver.get(url)

    def autoIINE(self):
        """
            自動でイイネする関数。
            だいたい一回で10イイネする。
            1日のイイネ制限は1200なので注意。
        """
        self.driver.refresh()
        time.sleep(3)
        for j in range(3,5):
            for i in range(1,11):
                time.sleep(0.5)
                try:
                    elements = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div/div/div[2]/div/div/section/div/div/div/div['+str(i)+']/div/article/div/div[2]/div[2]/div['+str(j)+']/div[3]/div')       
                    elements.click()
                except:
                    pass
    
    def tweetChoice(self):
        """
            filenameには1列のカラムを持つcsvファイルを指定
            ヘッダ名は"tweets",各行には140字以内のツイートを書く
        """
        wlen = len(self.df)
        randomIndex = randint(0,wlen-1)

        return self.df["tweets"].iloc[randomIndex]


    def run(self):
        #ここで実行したい処理を書く
        #例
        """
            公式：https://schedule.readthedocs.io/en/stable/
            #10分おきに実行
            schedule.every(10).minutes.do(job)
            #1時間おきに実行
            schedule.every().hour.do(job)
            #毎日10時30分に実行
            schedule.every().day.at("10:30").do(job)
            #月曜に実行
            schedule.every().monday.do(job)
            #毎週水曜日13時15分に実行
            schedule.every().wednesday.at("13:15").do(job)
            #毎時17分に実行
            schedule.every().minute.at(":17").do(job)

            上記のようにして、自分のツイートしたい時間を設定する。
        """
        """
        #毎時４０分に実行
        schedule.every().minutes.at(":41").do(self.tweet,"{}時{}分をお知らせします！！".format(datetime.datetime.now().hour,datetime.datetime.now().minute))
        schedule.every().minutes.at(":42").do(self.tweet,"{}時{}分をお知らせします！！".format(datetime.datetime.now().hour,datetime.datetime.now().minute))
        schedule.every().minutes.at(":43").do(self.tweet,"{}時{}分をお知らせします！！".format(datetime.datetime.now().hour,datetime.datetime.now().minute))
        schedule.every().minutes.at(":44").do(self.tweet,"{}時{}分をお知らせします！！".format(datetime.datetime.now().hour,datetime.datetime.now().minute))
        """
        #毎時00分に実行
        """
        schedule.every().hour.at(":00").do(self.tweet,"{}時をお知らせします！！".format(datetime.datetime.now().hour))

        #毎時30分に実行
        schedule.every().minutes.at(":50").do(self.tweet,"{}時{}分をお知らせします！！".format(datetime.datetime.now().hour,datetime.datetime.now().minute))

        tweetTmp = self.tweetChoice()
        #tweetChoiceで選んだ文字を5分おきにツイートする。
        #同じツイートが選ばれるとエラーとなるため、ランダムに選んだ2つの文章を組み合わせた方がよい
        schedule.every(15).minutes.do(self.tweet,tweetTmp)
        #イイネの実行はAutoIIne関数を使う
        schedule.every(2).minutes.do(self.autoIINE)
        """

            
    def quit_chrome(self):      
        self.driver.close()
        self.driver.quit()

if __name__ == '__main__':
    """
    tweet1 = AutoTweet("Oithu1Oiu543beu","banagid263","tweet.csv")
    """
    tweet1 = AutoTweet("ogurayuidaisuki43@gmail.com","kokurayuidaisuki43","tweet.csv")
    #tweet1 = AutoTweet("sakurasou_petto","kimetusuki","tweet.csv")
    tweet1.Login()
    time.sleep(10)
    """
    tweet2.Login()
    time.sleep(10)
    """

    while(True):
        try:
            tmp = tweet1.tweetChoice()
            print(tmp)
            time.sleep(5)
            tweet1.tweet(tmp)
            #tweet1.tweet(date2)
            #tweet1.tweet(date2)
            time.sleep(60*30)
            tweet1.driver.refresh()
            """tweet1.autoIINE()"""
            """
            tmp = tweet2.tweetChoice()
            tweet2.tweet(tmp)
            time.sleep(60)
            tweet2.driver.refresh()
            """
            """tweet2.autoIINE()"""

        except KeyboardInterrupt:
                print("\nprogram was ended.\n")
                tweet1.quit_chrome()
                sys.exit()
