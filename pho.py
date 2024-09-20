import requests
import base64
import json
import time

user_id_glob = 500648815

def get_user_data(user_id, access_token):
    url = f"https://api.vk.com/method/users.get?access_token={access_token}&fields=photo_100&user_ids={user_id}&v=5.131"
    response = requests.get(url)
    data = response.json()
    return data

def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    return None

def save_image_to_blob(image_content):
    return base64.b64encode(image_content).decode('utf-8')

def save_blob_to_file(blob, file_path):
    with open(file_path, 'a') as file:
        file.write(blob + '\n')

def saving(access_token, file_path, user_data, file_path_name):
    global user_id_glob
    user_data = get_user_data(user_id_glob, access_token)
    print(user_data)
     
    # time.sleep(1)
    # if 'error' in user_data:
    #     time.sleep(1)
    try:

        if ('deactivated' not in user_data['response'][0]) and (user_data['response'][0]['photo_100'] != 'https://sun9-49.userapi.com/impf/DW4IDqvukChyc-WPXmzIot46En40R00idiUAXw/l5w5aIHioYc.jpg?quality=96&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360&sign=10ad7d7953daabb7b0e707fdfb7ebefd&u=I6EtahnrCRLlyd0MhT2raQt6ydhuyxX4s72EHGuUSoM&cs=100x100'):
                
            

            with open(file_path_name, 'a', encoding = 'utf-8') as file:
                file.write(user_data['response'][0]['first_name'] + ' ' + user_data['response'][0]['last_name'] + ' ' + str(user_data['response'][0]['id']) + '\n')
            try:
                photo_url = user_data['response'][0]['photo_100']
                image_content = download_image(photo_url)
                print(user_id_glob)

                if image_content:
                    image_blob = save_image_to_blob(image_content)
                    save_blob_to_file(image_blob, file_path)
            except:
                with open(file_path_name, 'r', encoding = 'utf-8') as f:
                    lines = f.readlines()
                    lines = lines[:-1]
                with open(file_path_name, 'w', encoding = 'utf-8') as f:
                    f.writelines(lines)
                user_id_glob += 1
                saving(access_token, file_path, user_data, file_path_name)
        else:
            user_id_glob += 1
            saving(access_token, file_path, user_data, file_path_name)
    except:
        time.sleep(1)
        saving(access_token, file_path, user_data, file_path_name)

def main():
    access_token = 'vk1.a.4N4OQeJAIXGSpZuPb3DqYIThWt-gLBC_mfDMDCaYO7UHBcDQFF8_EKQ9qYQdO_a2oB_OZUvZjwKr8a4MjWpS8xIk1UNDkwgCBi6wZPQJNQKRxuMXbosLbWV26fX4-k96wnWD8vOVNlCsYOwkJN5EqKpx4gRxZLGRQ2sPXKEdjE641w50OUR3gd9-miOPiklZcUiR8tmfuqI9geKJkFlT3Q'
    global user_id_glob 
    file_path = 'avatars_blob.txt'
    file_path_name = 'name.txt'

    for i in range(1000):
        user_data = get_user_data(user_id_glob, access_token)
        
        saving(access_token, file_path, user_data, file_path_name)
        
        user_id_glob += 1


main()
print('DONE')