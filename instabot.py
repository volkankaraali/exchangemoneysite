from selenium import webdriver #use for choromedriver
from selenium.webdriver.common.keys import Keys #for use keyboard keys
import time
from userinfo import username,password


class Instagram:

    def __init__(self,username,password):
        self.browser=webdriver.Chrome()
        self.username=username
        self.password=password

        Instagram.signIn(self) #open browser and login

    def signIn(self):
        self.browser.get("https://www.instagram.com/")
        time.sleep(1)

        usernameInput=self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input") #take username input
        passwordInput=self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input") #take password input

        usernameInput.send_keys(self.username) # insert username from userinfo
        passwordInput.send_keys(self.password) # insert password from userinfo
        passwordInput.send_keys(Keys.ENTER) #login after input username and password
        time.sleep(3)
    
    def getFollowers(self):
        self.browser.get(f"https://www.instagram.com/{self.username}") #go to username's profile.
        time.sleep(1.5)
        self.browser.find_element_by_xpath("//li[2]/a").click() #click to followers.
        time.sleep(2)

        print('Counting followers...')
        Instagram.scrollDown(self) #scrolldown until last followers
 
        self.followersList=set()
        followers=self.browser.find_elements_by_css_selector(".FPmhX.notranslate._0imsa ") #tüm takipçileri çeker parantez içi a tag class adı.
        followerCount=0
        
        for user in followers:
            followerCount +=1
            followerUserName=user.text
            self.followersList.add(followerUserName)
        
        print(f'total followers: {followerCount}')

    def getFollowing(self):
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(1.5)
        self.browser.find_element_by_xpath("//li[3]/a").click() #click to following.
        time.sleep(1)


        print('Counting followings...')
        Instagram.scrollDown(self)

        self.followingList=set()  
        following=self.browser.find_elements_by_css_selector(".FPmhX.notranslate._0imsa ")
        followingCount=0
        
        for user in following:
            followingCount +=1
            followingUserName=user.text
            self.followingList.add(followingUserName)

        print(f'total following: {followingCount}')

    def isFollower(self):
        print("loading do not follow you...")
        time.sleep(1)
        Instagram.getFollowers(self)
        print('**************')
        Instagram.getFollowing(self)
        time.sleep(1)
        noFollowMe=set()
        for isFollowMe in self.followingList:
            if isFollowMe in self.followersList:
               pass
            else:
                noFollowMe.add(isFollowMe)
        time.sleep(1)
        print(noFollowMe)
        time.sleep(1)
        print(f'in your following, {len(noFollowMe)} users doesnt follow you.')

        
    def scrollDown(self):
        #scrolldown with javascript code. isgrP is scroll cursor when open follower popup
        #and doing scroll until last heigt end of page
        jsComment="""
        page=document.querySelector(".isgrP");  
        page.scrollTo(0,page.scrollHeight);
        var endPage=page.scrollHeight;
        return endPage;
        """

        endPage=self.browser.execute_script(jsComment)
        while True:
            last=endPage
            time.sleep(1)
            endPage=self.browser.execute_script(jsComment)
            if last==endPage:
                break


insta=Instagram(username,password)
#insta.getFollowers()
#insta.getFollowing()
insta.isFollower()