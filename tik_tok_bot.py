import requests, os

# https://www.tiktok.com/@codex_kg/video/7327987700139691271
# https://www.tiktok.com/@codex_kg/video/7327987700139691271?is_from_webapp=1&sender_device=pc&web_id=7289042945105217029


input_url = input("URL: ").split("/")
# print(input_url)
current_id = input_url[5].split("?")[0]
# print(current_id)
if current_id.isdigit():
    print("ID верный")
    video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()
    # print(video_api)
    video_url = video_api['aweme_list'][0]['video']['play_addr']['url_list'][0]
    print(video_url)
    try:
        print("Создаю папку video")
        os.mkdir("video")
    except:
        pass
    try:
        with open(f'video/{current_id}.mp4', 'wb') as video_file:
            video_file.write(requests.get(video_url).content)
        print(f'video {current_id} успешно загружен')
        # os.system(" cd video && explorer .")
        os.system(f'start video/{current_id}.mp4')
    except Exception as error:
        print(f"Error:{error}")
else:
    print("Неверный ID")
