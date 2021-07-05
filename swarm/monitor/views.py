

# Create your views here.

from django.template import loader
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
from requests import exceptions
from swarm.monitor.models import NodeInfo
from swarm.monitor.models import NodeStatus


def index(request):
    t = loader.get_template("index.html")
    nodes = NodeStatus.objects.all()
    c = {}
    nodeList = []
    offNodeSum = 0
    chequeSum = 0
    uncashedSum = 0
    for node in nodes:
        nodeList.append({
            'id': node.node_id.id,
            'ip': node.node_id.ip,
            'version': node.version,
            'port': node.node_id.port,
            'name': node.node_id.name,
            'status': node.status,
            'connect': node.connect,
            'chequeSum': node.chequeSum,
            'cashout': node.cashout,
            'walletScan': node.walletScan,
            'chequeScan': node.chequeScan
        })
        if node.status != "在线":
            offNodeSum = offNodeSum + 1
        if node.chequeSum:
            chequeSum = chequeSum + node.chequeSum
        if node.cashout:
            uncashedSum = uncashedSum + node.cashout

    c['nodeList'] = nodeList
    c['nodeSum'] = len(nodeList)
    c['offNodeSum'] = offNodeSum
    c['chequeSum'] = chequeSum
    c['uncashedSum'] = uncashedSum

    return HttpResponse(t.render(c))

def add_nodes(request):
    s_nodes = request.GET.get('nodes')
    # print(s_nodes)
    # print(type(s_nodes))
    v = s_nodes.split(';')
    # print(v)
    for s in v:
        # print(s)
        if len(s) > 0:
            c = s.split(',')
            ip = c[0].strip()
            port = c[1].strip()
            name = c[2].strip()
            try:
                NodeInfo.objects.get(ip=ip, port=port)
            except ObjectDoesNotExist:
                obj = NodeInfo(ip=ip, port=port, name=name)
                obj.save()
    ret = {'code': 0, 'msg': '', 'result': {}}
    res = json.dumps(ret)

    return HttpResponse(res)


def refresh(request):
    nodes = NodeInfo.objects.all()
    nodeList = []
    o = 0
    c = 0
    u = 0
    for node in nodes:
        id = node.id
        ip = node.ip
        port = node.port
        name = node.name
        try:
            node_status = NodeStatus.objects.get(node_id=id)
            version = node_status.version
            status = node_status.status
            connect = node_status.connect
            chequeSum = node_status.chequeSum
            cashout = node_status.cashout
            walletScan = node_status.walletScan
            chequeScan = node_status.chequeScan
            obj = {
                "id": id,
                "ip": ip,
                "version": version,
                "port": port,
                "name": name,
                "status": status,
                "connect": connect,
                "chequeSum": chequeSum,
                "cashout": cashout,
                "walletScan": walletScan,
                "chequeScan": chequeScan
            }
            nodeList.append(obj)
            if status != "在线":
                o = o + 1
            if chequeSum:
                c = c + chequeSum
            if cashout:
                u = u + cashout
        except ObjectDoesNotExist:
            obj = {
                "id": id,
                "ip": ip,
                "version": "Null",
                "port": port,
                "name": name,
                "status": "",
                "connect": "",
                "chequeSum": "",
                "cashout": "",
                "walletScan": "",
                "chequeScan": ""
            }
            nodeList.append(obj)
            o = o + 1

    # print(nodeList)
    ret = {}
    ret['nodeList'] = nodeList
    ret['nodeSum'] = len(nodeList)
    ret['offNodeSum'] = o
    ret['chequeSum'] = c
    ret['uncashedSum'] = u
    ret['code'] = 0
    ret['msg'] = ''
    ret['result'] = nodeList
    # ret = {'code': 0, 'msg': '', 'result': nodeList}
    res = json.dumps(ret)
    return HttpResponse(res)

def get_node_status(request):
    ret = NodeInfo.objects.all()
    for item in ret:
        # print(type(item))
        try:
           res = requests.get('http://{0}:{1}/health'.format(item.ip, item.port), timeout=1)
        except:
            node_status = "离线"
            version = "Null"
            conn_num = 0
            chequeSum = 0
            cashout = 0
            walletScan = "#"
            chequeScan = "#"
            try:
                NodeStatus.objects.get(node_id=item.id)
                NodeStatus.objects.filter(node_id=item.id).update(version=version, status=node_status, connect=conn_num,
                                                                  chequeSum=chequeSum, cashout=cashout, walletScan=walletScan,
                                                                  chequeScan=chequeScan)
            except ObjectDoesNotExist:
                obj = NodeStatus(node_id=item, version=version, status=node_status, connect=conn_num,
                                                                  chequeSum=chequeSum, cashout=cashout, walletScan=walletScan,
                                                                  chequeScan=chequeScan)
                obj.save()
        else:
            version = json.loads(res.text)['version'].split("-")[0]
            node_status = "在线"
            conn_tmp = requests.get('http://{0}:{1}/peers'.format(item.ip, item.port))
            conn_num = len(json.loads(conn_tmp.text)['peers'])
            cheque_tmp = requests.get('http://{0}:{1}/chequebook/cheque'.format(item.ip, item.port))
            trac_list = []
            for trac in json.loads(cheque_tmp.text)['lastcheques']:
                if trac['lastreceived']:
                    trac_list.append(trac['peer'])
            chequeSum = len(trac_list)
            cashout_list = []
            uncashed = ""
            for peer in trac_list:
                res = requests.get('http://{0}:{1}/chequebook/cashout/{2}'.format(item.ip, item.port, peer))
                if json.loads(res.text)['uncashedAmount']:
                    cashout_list.append(peer)
                    uncashed = uncashed + peer + ";"
            cashout = len(cashout_list)
            walletScan_tmp = requests.get('http://{0}:{1}/addresses'.format(item.ip, item.port))
            walletScan = json.loads(walletScan_tmp.text)['ethereum']
            chequeScan_tmp = requests.get('http://{0}:{1}/chequebook/address'.format(item.ip, item.port))
            chequeScan = json.loads(chequeScan_tmp.text)['chequebookAddress']
            try:
                NodeStatus.objects.get(node_id=item.id)
                NodeStatus.objects.filter(node_id=item.id).update(version=version, status=node_status, connect=conn_num,
                                                                  chequeSum=chequeSum, cashout=cashout, walletScan=walletScan,
                                                                  chequeScan=chequeScan, uncashed=uncashed)
            except ObjectDoesNotExist:
                obj = NodeStatus(version=version, node_id=item, status=node_status, connect=conn_num,
                                                                  chequeSum=chequeSum, cashout=cashout, walletScan=walletScan,
                                                                  chequeScan=chequeScan, uncashed=uncashed)
                obj.save()
    return HttpResponse({})


def delete_node(request):
    id = request.GET.get("id")
    node = NodeInfo.objects.get(id=id)
    node.delete()
    ret = {'code': 0, 'msg': '', 'result': {}}
    res = json.dumps(ret)
    return HttpResponse(res)
