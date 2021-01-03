from nonebot import on_command, CommandSession
from nonebot import permission as perm

#百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8

import http.client
import hashlib
import urllib
import random
import json

appid = '20201220000651651'  # 填写你的appid
secretKey = '_0NSDPzemDJB6R5m7w4O'  # 填写你的密钥

httpClient = None
fromLang = 'auto'   #原文语种

salt = random.randint(32768, 65536)






# sogou_tr使用帮助：
# print(sogou_tr('hello world'))  # -> '你好世界'
# print(sogou_tr('hello world', to_lang='de'))  # ->'Hallo Welt'
# print(sogou_tr('hello world', to_lang='fr'))  # ->'Salut tout le monde'
# print(sogou_tr('hello world', to_lang='ja'))  # ->'ハローワールド'


@on_command('translate', aliases=('翻译', '翻譯', '翻訳'), permission=perm.GROUP_ADMIN, only_to_me=False)
async def translate(session: CommandSession):
    q = session.get('text')
    if distinguishLanguage(q)['data']['src'] == 'zh':
        toLang = 'en'
    else:
        toLang = 'zh'
    if q:
        translation = baiduTransAPI(q,toLang)['trans_result'][0]['dst']
        await session.send(f'机翻译文：\n{translation}')
    else:
        await session.send('翻译姬待命中...')


@translate.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip() # 删去首尾空白
    if stripped_arg:
        session.state['text'] = stripped_arg
    else:
        session.state['text'] = None
    return


# async def get_translation(text: str) -> str:
#    if not hasattr(get_translation, 'cdtime'):
#        get_translation.cdtime = datetime.now() - timedelta(seconds=3)
#    now = datetime.now()
#    if(now < get_translation.cdtime):
#        return '翻译姬冷却中...'
#    else:
#        get_translation.cdtime = datetime.now() + timedelta(seconds=1)
#        ret = sogou_tr(text)
#        # print(sogou_tr.json)
#        return ret if '0' != sogou_tr.json.get('errorCode') else '翻译姬出错了 ごめんなさい！'




def distinguishLanguage(q):
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()


    languageurl='/api/trans/vip/language'
    languageurl = languageurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&salt=' + str(salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', languageurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        print(result)
        return result

    except Exception as e:
        print(e)
        return e
    finally:
        if httpClient:
            httpClient.close()



def baiduTransAPI(q,toLang):
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = '/api/trans/vip/translate'
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        print(result)
        return result

    except Exception as e:
        print(e)
        return e
    finally:
        if httpClient:
            httpClient.close()
