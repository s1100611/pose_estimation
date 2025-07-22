import instaloader


L = instaloader.Instaloader() 
L.login("s1100611_", "yzu1100611") 

data_path = "https://www.instagram.com/"


profile = instaloader.Profile.from_username(L.context, "only.grapher") # "only.grapher"欄位可以更改成想要爬取照片的帳號
followee_list = profile.get_followees() #取得追蹤的帳號清單

for post in profile.get_posts():
        L.download_post(post, target=profile.username)