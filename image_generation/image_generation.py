import numpy as np
import json
import requests
import time
import io
import os
from PIL import Image, ImageDraw, ImageFont
import ref
import base64
import tempfile

# oss_request = requests.get("https://newbucket-345ljh.oss-cn-shenzhen.aliyuncs.com/a.img")
# print(oss_request.status_code)
# print(oss_request.content)

# exit(0)

def loadfont(base64_str, size=18):
    """使用临时文件方法加载ref中的base64字体,绕过所有编码问题"""
    
    try:
        # 清理和解码
        clean_b64 = base64_str.replace('\n', '').replace(' ', '')
        font_data = base64.b64decode(clean_b64)
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ttf') as temp_file:
            temp_file.write(font_data)
            temp_path = temp_file.name
        
        try:
            # 从临时文件加载字体
            font = ImageFont.truetype(temp_path, size=size)
            return font
        finally:
            # 清理临时文件
            try:
                os.unlink(temp_path)
            except:
                pass
                
    except Exception as e:
        return None
    
deepseek_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
deepseek_key = "2a8f37fe-394b-4a50-a9a2-d24b706083a2"

image_url = "https://api.siliconflow.cn/v1/images/generations"
image_key = "sk-imjbobjscalcnhleejcrkjkmwrpjrqkzqjvskgbebdqxlbth"

oss_url = "https://newbucket-345ljh.oss-cn-shenzhen.aliyuncs.com"

try:
    # 随机生成内容
    age = str(np.random.randint(12, 70))
    role = np.random.choice(["农业/种植类", "工匠/工业/技术类", "养殖/畜牧类", "公共事务/法律类", "军事/安保类", 
                            "销售/贸易类", "文化/教育类", "宗教/术士/哲学类", "医疗/护理/卫生类", "表演/娱乐类", 
                            "交通/运输/物流类", "采集/狩猎/渔业类", "能源/矿产类", "服务业类", "新闻/媒体/出版类",
                            "科技/研发类", "手工业/纺织类", "建筑/园林类", "食品/餐饮类", "天文/地理类", 
                            "摊贩/店铺类", "金融/经济/保险类", "艺术/创作类", "考古/历史类", "生老病死/婚姻家庭类",
                            "体育/运动类"
                            ])
    if(np.random.random() < 0.8):
        era_selection = ["西周", "秦代", "汉代", "唐代", "明代", "民国", "1960年", "1980年", "2000年", "2020年", "2277年"]
        style_selection = [
            "铭文风格，简约古拙，带有甲骨文和金文的质感，多使用“唯”、“其”等古语，庄重肃穆。",
            "诗经风格，质朴口语化，带有比兴手法，多提及自然景物，生活气息浓厚。",
            "律令风格，严谨、精确、冷峻，如法律条文或官方诏书，充满权威感和秩序感。",
            "耕战风格，务实、粗犷，反映庶民与士兵的视角，用语直接有力。",
            "辞赋风格，铺陈华丽，气势恢宏，善用排比与典故，词汇丰富绚烂，充满浪漫与想象。",
            "乐府风格，叙事性强，语言清新自然，情感真挚动人，带有民间故事的色彩。",
            "诗豪风格，自信奔放，意境开阔，色彩浓烈，如李白、李贺的诗歌，充满奇特的想象和磅礴气势。",
            "禅意风格，空灵含蓄，言简意赅，追求意境深远，如王维、寒山的诗句，带有佛道哲学的韵味。",
            "话本风格，口语化、故事性强，如同章回小说，生动有趣，贴近市井。",
            "笔记风格，明代通俗文学，语言趋于平实、细腻、生活化，常带有品鉴、把玩的意味，如同文人笔记中的记录。",
            "白话文风格，文白夹杂，兼具古典韵味与现代启蒙的简洁感，带有革新、探索与忧患意识的色彩。",
            "申报风格，如同老报纸的新闻体或广告语，客观中带有一丝旧上海的摩登与商业气息。",
            "口号风格，简洁有力，充满集体主义、革命理想主义和劳动热情，常用排比和比喻，富有感召力。",
            "日记风格，朴实、真诚，带有个人崇拜和无私奉献的情感色彩，如《雷锋日记》般亲切感人。",
            "新风风格，充满希望、憧憬与反思，语言开始变得个性化、抒情化，带有的理想主义。",
            "市井风格，鲜活、接地气，反映市井生活的复苏，带有烟火气和商业萌芽感。",
            "网络初兴风格，互联网兴起，语言趋向多元化、网络化、商业化，常带有广告语、流行文化的影子与千禧年的乐观与开放。",
            "全球化风格，时尚、多元，词汇中融入英文缩写和新兴概念，节奏明快。",
            "自媒体风格，碎片化、吸睛，善用梗、表情包化和夸张语气，追求即时传播和情绪共鸣。",
            "极简风格，冷静、精确，如同产品说明书或科技评测，注重效率、数据和用户体验。",
            "AI逻辑风格，极度理性、精准，不带感情色彩，语句结构可能非常规，带有算法分析和数据报告的冰冷感。",
            "意识流风格， 跳跃、非线性，反映高度互联或混乱的意识状态。"
        ]
        era_index = np.random.randint(0, len(era_selection))
        era = era_selection[era_index]
        style = style_selection[era_index * 2 + np.random.randint(0, 2)]
    else:
        era_selection = ["史前", "魔法时代", "水底世界", "末世"]
        style_selection = [
            "神话风格，语言充满对自然力量的敬畏，将万物拟人化、神化，描述如创世史诗般宏大而神秘。",
            "岩画风格，极其简练、具象，如同刻在岩壁上的符号，只描述动作、猎物和基本需求，原始粗犷。",
            "咒语风格，韵律感强，多使用隐喻和象征，晦涩难懂但充满神秘的美感。",
            "学徒笔记风格，好奇、尝试性，夹杂着成功与失败的记录，像是魔法学徒的实践手札，生动而琐碎。",
            "潮汐风格，语言流动、空灵，节奏如波浪般起伏，多使用与水流、光影、声音相关的柔和词汇。",
            "航海日志风格，客观、记录性，但细节中透露出对未知深渊的警惕与好奇，如潜水员的观察笔记。",
            "启示录风格，破碎、压抑、充满不确定性和创伤后的混乱逻辑。",
            "日志风格，务实、警惕，语言直接且充满生存智慧，专注于记录生存细节，不带多余感情。"
        ]
        era_index = np.random.randint(0, len(era_selection))
        era = era_selection[era_index]
        style = style_selection[era_index * 2 + np.random.randint(0, 2)]



    culture = np.random.choice(["江南", "岭南", "巴蜀", "中原", "西北", "东北", "西域",
                                "燕京", "滇南", "徽州", "荆楚", "齐鲁", "关中", "青藏", 
                                "草原", "海滨", "海岛", "客家", "闽南", "吴越", "壮乡"])
    price = str(int(10 ** (np.random.random() * 4)))
    if(np.random.random() < 0.7):
        typ = "生成一项与你的职业特征强相关的工具，原料，产品或物品"
    else:
        typ = "生成一项与你的职业弱相关或无关，但你可能会携带或使用的日常生活用品或个人配饰"

    print(role, age, era, price, culture, style.split("风格，")[0])
    style = style.split("风格，")[1]

    # deepseek
    deepseek_request = requests.post(deepseek_url, json={
        "model": "deepseek-v3-250324",
        "messages": [
                {
                    "role": "user",
                    "content": "你是一位游戏中的平民阶层角色，年龄" + age + "，背景为" + culture + "文化，" + era + '''时代。
                                请根据以下约束生成内容：
                                role：你的具体职业（具体而简短），该职业类型属于''' + role + '''
                                item：''' + typ + '''（8字以内，不要带括号），
                                该场景下参考物品品质：草帽5/酒30/铁锄50/米10/绢200/牛1500，该物品品质为''' + price + '''

                                description：一段简短的物品描述
                                - 语言风格：''' + style + '''
                                - 长度：15-25字符
                                prompt：用于文生图的提示词
                                - 必须包含：3D建模参考图，白色背景，等距视角，写实风格，物品材质+形态+颜色+细节特征，无拼接无透视变形
                                - 禁止出现：拼接碎片、透视变形
                                - 需描述物品形态/材质/颜色/典型特征

                                严格按照以下示例输出json：
                                {
                                "role":string
                                "item": string
                                "description": string
                                "prompt"：string
                                }
                                '''
                }
            ]
        }, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + deepseek_key
        })

    deepseek_request_json = deepseek_request.json()
    # image_prompt = deepseek_request_json["choices"][0]["message"]["content"]
    response_content = deepseek_request_json["choices"][0]["message"]["content"]
    # 去掉可能的```json ```
    response_content = json.loads(response_content.replace("json", "").replace("```", ""))
    print(response_content)
    image_prompt = response_content["prompt"]

    # # oss下载字体
    # font_path  = "https://newbucket-345ljh.oss-cn-shenzhen.aliyuncs.com/zpix.ttf"
    # response = requests.get(font_path, verify=False)
    # font = ImageFont.truetype(io.BytesIO(response.content), 18)
    font = loadfont(ref.font, 18)
    if font is None:
        raise Exception("字体加载失败")

    # 生图
    image_request = requests.post(image_url, json={
        "model": "Kwai-Kolors/Kolors",
        "prompt": image_prompt,
        "image_size": "1024x1024",
        "batch_size": 1,
        "image": ref.ref_image
    }, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + image_key
    })

    image_request_json = image_request.json()
    image_url = image_request_json["images"][0]["url"]

    # 下载图片
    response = requests.get(image_url, verify=False)
    image_bytes = response.content

    # 使用PIL打开图像
    img = Image.open(io.BytesIO(image_bytes))

    # 转换灰度并缩放
    img = img.convert('L')
    img = img.resize((300, 300))

    # 归一化像素值到[0, 1]范围
    # img = ImageOps.equalize(img)
    pixels = np.array(img, dtype=np.float32) / 255.0

    # 获取图像尺寸
    height, width = pixels.shape

    # 随机抖动处理
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if pixels[i, j] > np.random.random():
                pixels[i, j] = 1.0
            else:
                pixels[i, j] = 0.0

    # 将结果转换回[0, 255]范围并转换为PIL图像
    output_image = Image.fromarray((pixels * 255).astype(np.uint8))

    # 在图片下方添加宽度300, 高度100的白色区域
    white_region = Image.new('L', (300, 100), 255)
    final_image = Image.new('L', (300, 400))
    final_image.paste(output_image, (0, 0))
    final_image.paste(white_region, (0, 300))

    # 图片下方写字
    for i in range(response_content["item"].__len__()):
        draw = ImageDraw.Draw(final_image)
        draw.text((20 * i + 11, 301), response_content["item"][i], font=font)

    for i in range(response_content["role"].__len__()):
        draw = ImageDraw.Draw(final_image)
        draw.text((271 - i * 20, 301), response_content["role"][response_content["role"].__len__() - i - 1], font=font)

    for i in range(np.min([response_content["description"].__len__(), 42])):
        draw = ImageDraw.Draw(final_image)
        draw.text((20 * (i % 14) + 11, 321 + i // 14 * 20), response_content["description"][i], font=font)

    # 图像逆时针旋转90度
    final_image = final_image.transpose(Image.ROTATE_90)

    # # 保存图像
    final_image.save("output.png")
    exit(0)

    final_image = np.array(final_image)

    # 转换为bytes, 每个byte储存8个像素
    image_bytes_black = bytearray()
    image_bytes_yellow = bytearray()

    for i in range(final_image.shape[0]):
            for j in range((final_image.shape[1]) // 8):
                byte_black = 0
                byte_yellow = 0
                for k in range(8):
                    if final_image[i, j * 8 + k] > 128:
                        final_image[i, j] = 255
                        byte_black |= 1 << (7 - k)
                        byte_yellow &= ~(1 << (7 - k))
                        # print("1", end="")
                    # elif image[i, j * 8 + k] > 90:
                    #     image[i, j] = 128
                    #     byte_black &= ~(1 << (7 - k))
                    #     byte_yellow |= 1 << (7 - k)
                    else:
                        final_image[i, j] = 0
                        byte_black |= 1 << (7 - k)
                        byte_yellow &= ~(1 << (7 - k))
                        # print("0", end="")
                image_bytes_black.append(byte_black)
                image_bytes_yellow.append(byte_yellow)
                # print(byte)

    image_bytes_black.extend(image_bytes_yellow)

    # 存储到oss
    oss_request = requests.put(oss_url + "/a.img", data = image_bytes_black, headers={
            "Content-Type": "application/octet-stream",
    })
    if oss_request.status_code == 200:
        print("上传成功")
    else:
        print("上传失败")
except:
    # 错误原因与行数
    import sys
    print(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
