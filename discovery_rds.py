#Auther：xwjr.com
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
import json

ID = 'ID'
Secret = 'Secret'
RegionId = 'cn-shenzhen'

clt = client.AcsClient(ID,Secret,RegionId)

DBInstanceIdList = []
DBInstanceIdDict = {}
ZabbixDataDict = {}
def GetRdsList():
    RdsRequest = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    RdsRequest.set_accept_format('json')
    #RdsInfo = clt.do_action(RdsRequest)
    RdsInfo = clt.do_action_with_exception(RdsRequest)
    for RdsInfoJson in (json.loads(RdsInfo))['Items']['DBInstance']:
        DBInstanceIdDict = {}
        DBInstanceIdDict["{#DBINSTANCEID}"] = RdsInfoJson['DBInstanceId']
        DBInstanceIdDict["{#DBINSTANCEDESCRIPTION}"] = RdsInfoJson['DBInstanceDescription']
        DBInstanceIdList.append(DBInstanceIdDict)


GetRdsList()
ZabbixDataDict['data'] = DBInstanceIdList
print json.dumps(ZabbixDataDict)