import requests, json
url = "https://45252e10a3b14cac99b4bd5d21c44b8d.apig.cn-north-4.huaweicloudapis.com/image_generation"

request = requests.post(url, json = {
    "llm_model": "deepseek-v3-250324",
    "llm_url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "llm_key": "Bearer 2a8f37fe-394b-4a50-a9a2-d24b706083a2",
    "img_key": "Bearer sk-imjbobjscalcnhleejcrkjkmwrpjrqkzqjvskgbebdqxlbth"
})
print(request.text)