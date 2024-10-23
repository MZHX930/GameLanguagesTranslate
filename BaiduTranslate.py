import aiohttp
import hashlib
import random
import string
from typing import Any, Dict
from rsa import sign
from urllib.parse import quote
import json


# Generate salt and sign
def make_md5(s, encoding="utf-8"):
    return hashlib.md5(s.encode(encoding)).hexdigest()


async def translate_text_async(
    query: str,
    to_lang: str,
) -> str:
    # query = quote(query)
    # print("请求翻译：" + query)

    # Set your own appid/appkey.
    appid = "20241017002178166"
    appkey = "ftzW2C9rkCVyDeeHDR8B"

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = "zh"
    # to_lang = "en"

    endpoint = "http://api.fanyi.baidu.com"
    path = "/api/trans/vip/translate"
    url = endpoint + path

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "appid": appid,
        "q": query,
        "from": from_lang,
        "to": to_lang,
        "salt": salt,
        "sign": sign,
    }

    async with aiohttp.ClientSession() as session:
        # 创建一个异步HTTP会话
        async with session.post(url, data=payload, headers=headers) as response:
            # 使用POST方法向指定的URL发送请求
            if response.status == 200:
                # 检查响应状态码是否为200（表示请求成功）
                result = await response.json()
                # 异步地将响应内容解析为JSON格式
                print(json.dumps(result, indent=4, ensure_ascii=False))
                if "trans_result" in result:
                    translated_text = "".join(
                        [item["dst"] for item in result["trans_result"]]
                    )
                else:
                    error_code = result.get("error_code", "未知错误")
                    translated_text = f"error_code: {error_code}"
                return translated_text
            else:
                return f"请求失败,状态码: {response.status}"
                # 如果状态码不是200，返回一个包含错误信息的字典


# 在主程序中调用异步函数
# asyncio.run(translate_text_async("Hello", "your_app_id", "your_secret_key"))
