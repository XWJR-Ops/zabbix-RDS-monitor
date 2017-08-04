# zabbix-RDS-monitor
Aliyun RDS-mysql status monitor with zabbix
zabbix通过阿里云api 自动发现、监控阿里云RDS-Mysql数据库
## 使用方法
### 环境要求
python = 2.7
### 模块安装
```shell
pip2.7 install aliyun-python-sdk-core aliyun-python-sdk-rds datetime
```
### 使用方法
1. 从阿里云控制台获取 **AccessKey** ,并修改脚本中的 **ID** 与 **Secret**
2. 修改区域 **RegionId**
3. 将两个脚本放置于以下目录
```conf
/etc/zabbix3/script
```
```shell
chmod +x /etc/zabbix3/script/*
```
4. 修改zabbix-agentd.conf，添加以下内容
```conf
#rds
UserParameter=rds.discovery,/usr/local/python2.7/bin/python2.7 /etc/zabbix3/script/discovery_rds.py
UserParameter=check.rds[*],/usr/local/python2.7/bin/python2.7 /etc/zabbix3/script/check_rds.py $1 $2 $3
```
5. 重启zabbix-agent
6. zabbix控制台导入模板，并关联主机