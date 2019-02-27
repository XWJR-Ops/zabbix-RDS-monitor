# zabbix-RDS-monitor
Aliyun RDS-mysql status monitor with zabbix   
   
zabbix通过阿里云api 自动发现、监控阿里云RDS-Mysql数据库      
本版本数据的图表展示，是以**监控项进行分组**，后期会再发布**以rds实例分组**的版本。
## 使用方法
### 注意事项
1. 脚本会收集RDS别名，
2. 不要默认别名
3. 不要使用中文别名（zabbix不识别）
4. 切记aliyun-python-sdk-core==2.3.5，新版本的sdk有bug
### 环境要求
python = 2.7
### 模块安装
```shell
/usr/bin/env pip2.7 install aliyun-python-sdk-core==2.3.5 aliyun-python-sdk-rds==2.1.4 datetime
```
### 使用方法
1. 从阿里云控制台获取 **AccessKey** ,并修改脚本中的 **ID** 与 **Secret**
2. 修改区域 **RegionId**
3. 将两个脚本放置于以下目录
```conf
/etc/zabbix/script
```
```shell
chmod +x /etc/zabbix/script/*
```
4. 修改zabbix-agentd.conf，添加以下内容
```conf
#rds
UserParameter=rds.discovery,/usr/bin/env python2.7 /etc/zabbix/script/discovery_rds.py
UserParameter=check.rds[*],/usr/bin/env python2.7 /etc/zabbix/script/check_rds.py $1 $2 $3
```
5. 重启zabbix-agent
6. zabbix控制台导入模板，并关联主机
