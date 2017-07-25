# -*- coding: utf-8 -*-
import sys
import argparse
import StringIO
import smtplib
import requests
from email.mime.text import MIMEText
from lxml import etree


class Args():
    pass


if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()

    args = parser.parse_args(namespace=Args())
    
    # request service
    with requests.Session() as session:
        # 查詢航班
        response = session.get('https://yoyaku.4and5.com/reserve/html/rvpc_srchHtl.html', params={
            # 都道府県
            'cntry': 'JPN',
            # 都道府県
            'prfctr': '40',
            # 年月
            'chcknYearAndMnth': '201710',
            # 日
            'chcknDayOfMnth': '13',
            # 宿泊数
            'ldgngNum': '1',
            # 利用人数
            'ldgngPpl': '2',
            # 部屋数
            'roomNum': '1',
            # ホテル名
            'htlName': '博多口駅前2',
            'dispFull': 'on',
            'tabGrpCode': 'BASIC',
        })
        # 解析HTML
        parser = etree.HTMLParser(encoding=response.encoding, remove_blank_text=True)
        root = etree.HTML(response.text, parser=parser)
        # 查詢結果
        input = root.xpath("//input[contains(@name, 'rsrvMmbr[6000179][21][6000179][null][113660]')]")
        if input:
            if 'disabled' not in input[0].attrib:
                message = '查詢結果已可購票! 請盡速至官網訂購機票!'
                print 'Message:', message
            else:
                sys.exit()
                # message = '查詢無結果!'
        else:
            message = '查詢結果異常!\n\n' + etree.tostring(root, encoding='utf-8', pretty_print=True, method='html')
            print 'Message:', message

        # 寄送信件
        try:
            # 信件內容
            text = MIMEText(message)
            text['Subject'] = '東橫INN查詢空房程式'
            text['From'] = 'service@toyoko-inn.com'
            text['To'] = 'etoanik@gmail.com'
            # 登入伺服器
            server = smtplib.SMTP(host='msa.hinet.net')
            server.sendmail('service@toyoko-inn.com', 'etoanik@gmail.com', text.as_string())
        finally:
            # 離開
            server.quit()
        
        
