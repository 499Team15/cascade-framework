import requests
import csv

def get_page_posts(page_id, access_token):
    url = f"https://graph.facebook.com/{page_id}/posts"
    params = {
        "access_token": access_token,
        "fields": "id,message,created_time",
        "limit": 10 # Let's retrieve multiple posts
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'error' in data:
        print("Error:", data['error'])
    else:
        posts = data.get('data', [])
        print("Number of posts retrieved:", len(posts))

    response = requests.get(url, params=params)
    data = response.json()
    return data.get('data', []) # Extract the 'data' field from the response

file = open("Facebookdata.csv", "w", newline='', encoding='utf-8')
page_id = "1365574063559367"
access_token = "EAADZBeoXbPQoBO5vqpEyYK1RBsCHZBEi53THmPUjSf8hOczoi4yMENbZBDbqWn4p14O1s2KuIeH8xpzcnaep6oQQGUSfWtZBTwodcyEXeJ86nzOdhzUkOZAXYit6BXPWUVvQjhe1f0uQwJGaPyE7PPKZC63YtZAztmvCE6jVISWzIO4XiAMM35ZAoXPXZBgxJVANVIBXsOVDJm1zBxsZAdCQZDZD"
posts = get_page_posts(page_id, access_token)

writer = csv.writer(file)
writer.writerow(["Post ID", "Message", "Created Time"]) # Write header

for post in posts:
    post_id = post.get('id', '')
    message = post.get('message', '')
    created_time = post.get('created_time', '')
    writer.writerow([post_id, message, created_time])

file.close()