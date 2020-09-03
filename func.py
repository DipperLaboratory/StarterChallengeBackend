import hashlib
from aliyunsdkcore.request import CommonRequest

# from email.mime.text import MIMEText
# from email.utils import formataddr
# from email.header import Header
# import smtplib

from secret import *

from aliyunsdkcore.request import AcsRequest
saltDict = {
    1: 'dU>HvK15Ss>ogXVnyb>6qg;;`HW.dJD0GVtfs2jwP3&m{JeClfy-Hw.,E1JT^--P',
    2: 'gyo1O@=K`e|+pIoah-/ (fJ@=]+7<gdoKA*NS|DvD<D&cmhH4@F{W+N/-xmL`}6/',
    3: '9M4a5aNnS<f|.a!x0|[`{|2fgd>+R[kqjQaxoSm@)pZ:{,>SZo;zZ}~TK9n381=B',
    4: '-0o+)CTh?I-ohG<l0CzVF<#M)RGDA)z 6/#_+l/-$|[p$de`ATm4Gab*Il67L}^t',
    5: 'Tyk,X&|]:%&w~o{!eSQl>P#KU5Mi]|o46+t( rH.Pfamq627tY<xT*;A&p7Hm~+r'
}


# def sendmail(msg, title, receiver_name, receiver_address):
#     print('send ' + receiver_address)
#     msgMIME = MIMEText(msg, 'plain', 'utf-8')
#     msgMIME['From'] = formataddr((Header('北斗实验室', 'utf-8').encode(), sender_address))
#     msgMIME['To'] = formataddr((Header(receiver_name, 'utf-8').encode(), receiver_address))
#     msgMIME['Subject'] = Header(title, 'utf-8').encode()
#
#     server = smtplib.SMTP(smtp_address, smtp_port)
#     # server.set_debuglevel(True)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()
#     server.login(sender_address, sender_password)
#     server.sendmail(sender_address, [receiver_address], msgMIME.as_string())
#     server.close()

def sendmail(msg, title, receiver_name, receiver_address):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dm.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2015-11-23')
    request.set_action_name('SingleSendMail')

    request.add_query_param('RegionId', "ap-southeast-1")
    request.add_query_param('AccountName', "noreply@mail.startcoder.top")
    request.add_query_param('AddressType', "1")
    request.add_query_param('ReplyToAddress', "true")
    request.add_query_param('ToAddress', receiver_address)
    request.add_query_param('Subject', title)
    request.add_query_param('TextBody', msg)
    request.add_query_param('FromAlias', "北斗实验室")
    request.add_query_param('ClickTrace', "1")

    client.do_action(request)

def getHash(x: str):
    return hashlib.md5(x.encode()).hexdigest()


def getHash2(x: str, y: str):
    return hashlib.md5((x + y).encode()).hexdigest()


if __name__ == '__main__':
    sendmail('这是一封测试邮件\r\n这是第二行', 'TEST', 'Zxilly', 'zhouxinyu1001@gmail.com')
