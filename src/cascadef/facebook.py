import requests
import csv

def get_posts(page_id, access_token):
    url = f"https://graph.facebook.com/{page_id}/posts"
    params = {
        "access_token": access_token,
        "fields": "id,message,created_time",
        "limit": 10 # Number of posts to pull from the page
    }

    response = requests.get(url, params=params)
    data = response.json()

    
    posts = data.get('data', [])
    print("Number of posts retrieved:", len(posts))

    response = requests.get(url, params=params)
    data = response.json()
    return data.get('data', []) # Extract the 'data' field from the response

file = open("Facebookdata.csv", "w", newline='', encoding='utf-8')
page_id = "1365574063559367" #Replace with Page ID of page to pull data from
access_token = "EAADZBeoXbPQoBO5vqpEyYK1RBsCHZBEi53THmPUjSf8hOczoi4yMENbZBDbqWn4p14O1s2KuIeH8xpzcnaep6oQQGUSfWtZBTwodcyEXeJ86nzOdhzUkOZAXYit6BXPWUVvQjhe1f0uQwJGaPyE7PPKZC63YtZAztmvCE6jVISWzIO4XiAMM35ZAoXPXZBgxJVANVIBXsOVDJm1zBxsZAdCQZDZD" #Replace with personal access token
posts = get_posts(page_id, access_token)

writer = csv.writer(file)
writer.writerow(["Post ID", "Message", "Created Time"]) # Write header

for post in posts:
    post_id = post.get('id', '')
    message = post.get('message', '')
    created_time = post.get('created_time', '')
    writer.writerow([post_id, message, created_time])

file.close()
