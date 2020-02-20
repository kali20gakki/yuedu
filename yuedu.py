#!/usr/bin/env python3
# coding:utf-8

import requests, json, random, base64, os, logging, sys, time
from aes_crypto import AESCrypto
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from pathlib import Path
from merge_pdf import file_name_walk
from config import DownloadPath, BookPath, TaskFilePath, BookQueue

logging.basicConfig(stream=sys.stderr, format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)



DETAIL_URL = 'https://bridge.51zhy.cn/transfer/Content/Detail?'
LIST_URL = 'https://bridge.51zhy.cn/transfer/tableofcontent/list?'
AUTHORIZE_URL = 'https://bridge.51zhy.cn/transfer/content/authorize'



HEADER = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}


HEADER2 = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}
# detial param
PARAM = {
    'AccessToken': 'Qr3n1SX5TXikQaQw34HhCDoS3P5SCysT1KcX1dPJ',
    'DeviceToken': 'ebook031BCBD364453A896DA7CBE1AE95599C',
    'ApiName': '/Content/Detail',
    'BridgePlatformName': 'phei_yd_web',
    'random': str(random.uniform(0.0,1.0)),
    'AppId': '3',
    'id': ''
}


P = {
    'AccessToken': 'Qr3n1SX5TXikQaQw34HhCDoS3P5SCysT1KcX1dPJ',
    'DeviceToken': 'ebook031BCBD364453A896DA7CBE1AE95599C',
    'ApiName': '/tableofcontent/list',
    'BridgePlatformName': 'phei_yd_web',
    'random': str(random.uniform(0.0,1.0)),
    'AppId': '3',
    'objectId': ''
}

rsa = {
    "privateKey":"-----BEGIN RSA PRIVATE KEY-----\r\nMIIEogIBAAKCAQEAqhC+NmhvKKqB/Utz3HITsPrrMRmsi088T3cjE5yR+6beWhpz\r\nknylxOrI20uWhRvREoCfTt6AHYNXF7J4jJHYzyqSUFJYOlvabT2zsLCrn4zlfkRX\r\nyHJHHXD0soMGcUZmjj2z8/SsmX5IWZp6mmkYFItiYHIdMfYLz1OP0cX47x7wFf1m\r\nszTnRoyrDYm6PpQaP2VxCF4OC9D41pifkHwKfv6RQK5zV+xWFf17DG0U5yIxdiLT\r\nmDpBLjxid9XILOfnFQ0A6NQDicUV1nGw93oN3+kUUQcle2OJANhOa9oKqtDl1slM\r\nGa6qXBA9pwL99thovrHZTo3iWuujAcsY47+l/QIBAwKCAQBxYH7O8EobHFao3Pfo\r\nTA0gp0d2ER2yNNLfpMINEwv9GemRZve2/cPYnIXnh7muEothqxTfPwATrOS6dvsI\r\nYTs0xww1jDrRkpGeKSJ1yx0VCJj+2DqFoYS+S03MV1mg2Zm0KSKiox27qYWREacR\r\nm2VjB5bq9r4hTrKKN7U2g/tKE4iv2Jy+CQiz338S/6IJ0EKtGm/gzOOLW5pefvw1\r\nVvJsdT1z1Od5DyqymaYwEqqBk78GAaUoK50SEFSsIpKDZkeYVq4tP6EEBBdwOebT\r\nF4wzYzW+F6psWGgPehTv6e0ep7I4yWnNA94qPgZio5jD2uOX5WahGAEbUe/gnjzm\r\n8ZwrAoGBAOSi9QbU4xg351NmUtTzMG8Gyg/n6GQzZZ4IkDIduF6S05hxMTVLstSX\r\nkePFqVap/bVbwixiSOZ9/ovQo2SAjQBdBkLz0tlbreRy+45gFkPhpjGrcrS47XwI\r\nOE5y1GO3YKtDcl32g9/aqv5UhI3LWcHgVTBRTsA/kRgDTYxJmLAxAoGBAL5rQ3TB\r\nREIA1hkKt3I8q0c087lPQlSHYfNASfMiwUBJexyhveLWosFyhR3+p756xt2RXi95\r\nr+8VJVek/ofnQXtThLixIbioEQ47H0hawHexLhIIcPEf8XDhaOCRJsNFdK8+KM9v\r\npP1CCDW+iQsFtlF6hI8LmyByX6MtkDE/vIuNAoGBAJhso1njQhAlROJENziiIEoE\r\nhrVFRZgiQ76wYCFpJZRh4mWgy3jdIeMPtpfZG48b/njn1shBhe7+qbKLF5hVs1WT\r\nWYH34eY9HphMp7RADtfrxCEc9yMl86gFet73OEJ6QHIs9ulPApU8cf7jAwkyO9aV\r\njiA2NIAqYLqs3l2GZcrLAoGAfvIs+IDYLACOu1x6TChyL3iie4osOFpBTNWGohcr\r\ngDD8vcEpQeRsgPcDaVRv1FHZ6QuUH6Z1Sg4Y5Ripr++A/OJYeyDBJcVgtCdqMDyA\r\nT8t0DAWgoL/2S0DwlbYZ14OjH37F35/DU4Fazn8GB1kkNlGttLJnavbqbMkKy3/T\r\nB7MCgYEA3WeEEq7mIrm/Q4TOBM4cVLWUBbx9ssYsR+yzSGWIzDWr+fLsq4c8WePK\r\neaQGBc9Z5Y5sM1FsCMSTF0kZkJdEbTictq5JDNU6ND7EVTSkoVwIRyVNJI5U9w6n\r\nrQZIMqkgXXjJEmRC+SS0LtyKh/1HWBNspq7lb7USLefAgLXTnmU=\r\n-----END RSA PRIVATE KEY-----\r\n",
    "publicKey":'-----BEGIN+PUBLIC+KEY-----%0D%0AMIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAqhC%2BNmhvKKqB%2FUtz3HIT%0D%0AsPrMjI0MTYwMTQ0MTQ1MjEwMTQ3MTQ1MTc4MTY0MTc3MjQ0MjA5MjA4MTc4MTc2MTc3MjE0MjA3MTg0MjQ0MjE2MjI2MjAxMjQ3MTQ1MjUxMjI1MTQ1MjQ3MTk4MTI4MTYxrMRmsi088T3cjE5yR%2B6beWhpzknylxOrI20uWhRvREoCfTt6AHYNXF7J4jJHY%0D%0AzyqSUFJYOlvabT2zsLCrn4zlfkRXyHJHHXD0soMGcUZmjj2z8%2FSsmX5IWZp6mmkY%0D%0AFItiYHIdMfYLz1OP0cX47x7wFf1mszTnRoyrDYm6PpQaP2VxCF4OC9D41pifkHwK%0D%0Afv6RQK5zV%2BxWFf17DG0U5yIxdiLTmDpBLjxid9XILOfnFQ0A6NQDicUV1nGw93oN%0D%0A3%2BkUUQcle2OJANhOa9oKqtDl1slMGa6qXBA9pwL99thovrHZTo3iWuujAcsY47%2Bl%0D%0A%2FQIBAw%3D%3D%0D%0A-----END+PUBLIC+KEY-----%0D%0A'
}



def parse_detail_url(bookid):
    PARAM['id'] = bookid
    detail = requests.get(url= DETAIL_URL, 
                        headers=HEADER, 
                        params=PARAM)
    return detail


def get_token_tile(detail):
    data = json.loads(detail.text)
    Title = data.get('Data').get('Title')
    AuthorizeToken = data.get('Data').get('ExtendData').get('AuthorizeToken')

    return AuthorizeToken, Title


def get_bookmark(bookid):
    P['objectId'] = bookid
    r = requests.get(LIST_URL,headers=HEADER, params=P)
    filepath = os.path.join(DownloadPath, bookid, 'bookmark.json')
    with open(filepath, 'w', encoding='utf-8') as fd:
         fd.write(json.dumps(r.json(), indent=4, ensure_ascii=False))
    logging.info('%s bookmark.json save done!'%bookid)

def parse_authorize_url(bookid, AuthorizeToken):
    
    DATA = 'IsOnline=true&AccessToken=Qr3n1SX5TXikQaQw34HhCDoS3P5SCysT1KcX1dPJ&DeviceToken={DeviceToken}'\
    '&ApiName=content/authorize&BridgePlatformName=phei_yd_web&random={random}'\
    '&AppId=3&id={bookid}'\
    '&type=rsa&devicekey={devicekey}'\
    '&authorizeToken={authorizeToken}'.format(DeviceToken = PARAM['DeviceToken'], 
    random = str(random.uniform(0.0,1.0)),
    bookid = bookid,
    devicekey = rsa['publicKey'],
    authorizeToken = AuthorizeToken)

    authorize = requests.post(url= AUTHORIZE_URL, 
                        data=DATA,headers=HEADER2)

    
    return authorize


def get_key_urls(authorize):
    authorize_data = json.loads(authorize.text)
    data_key = authorize_data.get('Data').get('Key')
    # 整书 url
    book_url = authorize_data.get('Data').get('Url')
    # 每一页pdf url
    SplitFileUrls = authorize_data.get('Data').get('SplitFileUrls')

    return data_key, book_url, SplitFileUrls

    

def load_taskfile(bookid):
    filepath = os.path.join(TaskFilePath, bookid + '.txt')
    with open(filepath, 'r', encoding='utf-8') as fd:
        tasks = fd.read()
    
    return eval(tasks)


def save_taskfile(bookid, tasks):
    if not os.path.exists(TaskFilePath):
        os.makedirs(TaskFilePath)
    tasks = str(tasks)
    filepath = os.path.join(TaskFilePath, bookid + '.txt')
    with open(filepath, 'w', encoding='utf-8') as fd:
        fd.write(tasks)


def download_pdf_page(page_url, bookid, title, cnt, aes_key):
    # AES 加密过的PDF
    pdf = requests.get(page_url, headers=HEADER)

    aes = AESCrypto(aes_key, 'ECB', 'pkcs7')

    f = aes.decrypt(base64.b64encode(pdf.content), None)
    pagename = bookid + '-' + title + '-' +str(cnt) + '.pdf'
    pagepath = os.path.join(DownloadPath, bookid, pagename)
    with open(pagepath, 'wb') as fd:
        fd.write(f)

book_cnt = 1
def download_book(bookid, booksum = 1):
    global book_cnt
    detail = parse_detail_url(bookid)
    #print(detail.content)
    AuthorizeToken, Title = get_token_tile(detail)
    logging.info('%s parse detial url done!'%bookid)

    authorize = parse_authorize_url(bookid, AuthorizeToken)
    aes_key, book_url, SplitFileUrls = get_key_urls(authorize)
    logging.info('%s parse authorize url done!'%bookid)
            
    get_bookmark(bookid)

    rsakey = RSA.importKey(rsa['privateKey'])
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = cipher.decrypt(base64.b64decode(aes_key), None)
    aes_key = str(text, encoding='utf-8')
    logging.info('%s decrypt AES key done!'%bookid)
    
    print(SplitFileUrls)
    page_sum = len(SplitFileUrls)
    tasks = [i for i in range(1, page_sum+1)]
    tasks_path = Path(TaskFilePath+bookid+'.txt')

    if tasks_path.exists():
        tasks = load_taskfile(bookid)
        logging.info('%s taskfile already exist, jump'%bookid)#bug
    else: 
        # 第一次运行
        save_taskfile(bookid, tasks)

    while tasks:
        # popleft
        num = tasks.pop(0) # num : int
        try:
            page_url = SplitFileUrls[num - 1]
            download_pdf_page(page_url, bookid, Title, num, aes_key)
            # 存档
            save_taskfile(bookid, tasks)
            logging.info('%s<%s> page %d/%d OK [%d/%d]'%(bookid, Title, num, page_sum, book_cnt, booksum))
            slptime = round(random.uniform(10 ,20))
            time.sleep(slptime)
        except:
            tasks.append(num)
            save_taskfile(bookid, tasks)
            logging.error('%s<%s> page %d/%d ERROR [%d/%d]'%(bookid, Title, num, page_sum, book_cnt, booksum))

    # 合并PDF
    floder = os.path.join(BookPath, bookid)
    if not os.path.exists(floder):
        os.makedirs(floder)
    
    # 检查是否已经转换过
    pdf = Path(BookPath, bookid, bookid+'-'+Title+'.pdf')

    if not pdf.exists():
        logging.info('%s merge pdf ...'%bookid)
        pdfpath = os.path.join(DownloadPath, bookid)
        try:
            file_name_walk(pdfpath, bookid)
            logging.info('%s merge pdf done!'%bookid)
            book_cnt += 1
        except:
            logging.error('%s merge pdf error!'%bookid)
    else:
        book_cnt += 1
        logging.warning('%s pdf already exists!'%bookid)



def download_books(bookid_list):
    BOOKLIST = bookid_list
    if not os.path.exists(DownloadPath):
        os.makedirs(DownloadPath)
    
    if not os.path.exists(BookPath):
        os.makedirs(BookPath)
    
    if not isinstance(BOOKLIST, list):
        logging.error('BOOKLIST is not List!')
        return
    
    while BOOKLIST:
        bookid = BOOKLIST.pop(0)
        
        bookpath = os.path.join(DownloadPath, bookid)
        if not os.path.exists(bookpath):
            os.makedirs(bookpath)
            logging.info('%s bookid path generate done!'%bookid)

        try:
            start = time.time()
            download_book(bookid, len(BOOKLIST))
            print('ok')
            end = time.time()
            logging.info('%s book download cost %d s'%((round(end-start)), bookid))
            logging.info('sleep a while...')
            slptime = round(random.uniform(8*60,10*60))
            time.sleep(slptime)
            logging.info('start next book...')
        except:
            logging.error('error in parse！')
    
    logging.info('ALL Down!!!')
    




if __name__ == '__main__':
    download_books(['19526294'])
    # if BookQueue:
    #     logging.info('BookQueue have %d book'%len(BookQueue))
    #     download_books(BookQueue)
