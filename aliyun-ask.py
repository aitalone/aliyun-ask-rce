#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/11/10
# @Author  : psponge
import json
import re
import argparse
import os
import sys
import base64
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.CreateCommandRequest import CreateCommandRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.InvokeCommandRequest import InvokeCommandRequest
def cmd(region, InstanceId, cmd1):
    client = AcsClient('ak', 'sk', '%s' % region)
    request = CreateCommandRequest()
    request.set_accept_format('json')
    request.set_Name("shell")
    request.set_Type("RunShellScript")
    cmd1 = cmd1.encode("utf-8")
    cmd1 = base64.b64encode(cmd1)
    request.set_CommandContent(cmd1)
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))
    CommandId = json.loads(response)
    CommandId = CommandId["CommandId"]
    request = DescribeInstancesRequest()
    request.set_accept_format('json')
    response = client.do_action_with_exception(request)
    from aliyunsdkecs.request.v20140526.InvokeCommandRequest import InvokeCommandRequest
    request = InvokeCommandRequest()
    print(CommandId)
    print(InstanceId)
    request.set_CommandId(CommandId)
    request.set_InstanceIds([InstanceId])
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))
region1 = [""]
InstanceId1 = [""]
def info():
    a = ['ab-south-1', 'ap-northeast-1', 'ab-southeast-5', 'op-southeast-3',
         'ab-southeast-2', 'op-southeast-1', 'cn-hongkong',
         'ca-chengdu', 'cn-heyuan', 'cn-shenzhen-finance-1',
         'cn-shenzhen', 'cn-north-2-gov-1', 'cn-wulanchabu',
         'cn-huhehaote', 'cn-zhangjiakou', 'cn-beijing', 'cn-qingdao',
         'cn-shanghai', 'cn-shanghai-finance-1', 'cn-hangzhou',
         'an-shanghai-finance-1', 'eu-central-1', 'ab-northeast-1',
         'in-shanghai', 'me-east-1', 'us-east-1', 'us-west-1', 'eu-west-1']
    b = 0
    number = 0
    f = open("./region.txt", 'a')
    ff = open("./InstanceId.txt", 'a')
    f.seek(0)
    f.truncate()
    ff.seek(0)
    ff.truncate()
    while (b < 28):
        region = (a[b])
        b = b + 1
        try:
            client = AcsClient('ak', 'sk', '%s' % region)
            request = DescribeInstancesRequest()
            request.set_accept_format('json')
            response = client.do_action_with_exception(request)
            info = str(response, encoding='utf-8')
            info = json.loads(info)
            zzz = info['Instances']['Instance']
            for z1 in zzz:
                print("实例id", z1['InstanceId'])
                print("主机名称", z1['HostName'])
                print("系统:", z1['OSName'])
                print("cpu:", z1['Cpu'])
                print("地区:%s" % region)
                InstanceId = z1['InstanceId']
                if z1['InstanceId'] != None:
                    region1.extend(['%s' % region])
                    f = open("./region.txt", 'a')
                    ff = open("./InstanceId.txt", 'a')
                    ff.write(InstanceId)
                    ff.write("\n")
                    ff.close()
                    f.write(region)
                    f.write("\n")
                    f.close()
                    InstanceId1.extend(['%s' % InstanceId])
                number += 1
        except BaseException:
            dd = 1
    print("共", number, "台")
def logo():
    CLRF = "\r\n"
    LOGO = R"""
██████╗ ███████╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ███████╗     █████╗ ██╗  ██╗███████╗██╗  ██╗
██╔══██╗██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝ ██╔════╝    ██╔══██╗██║ ██╔╝██╔════╝██║ ██╔╝
██████╔╝███████╗██████╔╝██║   ██║██╔██╗ ██║██║  ███╗█████╗█████╗███████║█████╔╝ ███████╗█████╔╝ 
██╔═══╝ ╚════██║██╔═══╝ ██║   ██║██║╚██╗██║██║   ██║██╔══╝╚════╝██╔══██║██╔═██╗ ╚════██║██╔═██╗ 
██║     ███████║██║     ╚██████╔╝██║ ╚████║╚██████╔╝███████╗    ██║  ██║██║  ██╗███████║██║  ██╗
╚═╝     ╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

                                                                                        """
    print(LOGO)
def main():
    logo()
    parser = argparse.ArgumentParser()
    parser.add_argument('--commond', type=str, help='Execute command parameters')
    parser.add_argument('--info', type=str, help='Output host details')
    args = parser.parse_args()
    cmd1 = str(args.commond)
    if args.info == "info":
        info()
    elif args.commond != None:

        with open('./region.txt', 'r') as f:
            for region11 in f:
                region11 = region11.strip('\n')
                region1.extend(['%s' % region11])
        with open('./InstanceId.txt', 'r') as ff:
            for InstanceId11 in ff:
                InstanceId11 = InstanceId11.strip('\n')
                InstanceId1.extend(['%s' % InstanceId11])
        print(region1, InstanceId1)
        i = 0
        while (i < 50):
            i += 1
            try:
                region = region1[i]
                InstanceId = InstanceId1[i]
                cmd(region, InstanceId, cmd1)
                print(i)
            except BaseException:
                dd = 1
    else:
        print("usage: .py [-h] -c COMMOND -info INFO")

if __name__ == '__main__':
    main()