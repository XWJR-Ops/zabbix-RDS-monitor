#coding=utf-8
#Auther：xwjr.com
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeResourceUsageRequest,DescribeDBInstancePerformanceRequest
import json,sys,datetime

ID = 'ID'
Secret = 'Secret'
RegionId = 'cn-shenzhen'

clt = client.AcsClient(ID,Secret,RegionId)

Type = sys.argv[1]
DBInstanceId = sys.argv[2]
Key = sys.argv[3]

# 阿里云返回的数据为UTC时间，因此要转换为东八区时间。其他时区同理。
UTC_End = datetime.datetime.today() - datetime.timedelta(hours=8)
UTC_Start = UTC_End - datetime.timedelta(minutes=25)

StartTime = datetime.datetime.strftime(UTC_Start, '%Y-%m-%dT%H:%MZ')
EndTime = datetime.datetime.strftime(UTC_End, '%Y-%m-%dT%H:%MZ')

def GetResourceUsage(DBInstanceId,Key):
    ResourceUsage = DescribeResourceUsageRequest.DescribeResourceUsageRequest()
    ResourceUsage.set_accept_format('json')
    ResourceUsage.set_DBInstanceId(DBInstanceId)
    ResourceUsageInfo = clt.do_action_with_exception(ResourceUsage)
    #print ResourceUsageInfo
    Info = (json.loads(ResourceUsageInfo))[Key]
    print Info

def GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime):
    Performance = DescribeDBInstancePerformanceRequest.DescribeDBInstancePerformanceRequest()
    Performance.set_accept_format('json')
    Performance.set_DBInstanceId(DBInstanceId)
    Performance.set_Key(MasterKey)
    Performance.set_StartTime(StartTime)
    Performance.set_EndTime(EndTime)
    PerformanceInfo = clt.do_action_with_exception(Performance)
    #print PerformanceInfo
    Info = (json.loads(PerformanceInfo))
    Value = Info['PerformanceKeys']['PerformanceKey'][0]['Values']['PerformanceValue'][-1]['Value']
    print str(Value).split('&')[IndexNum]


if (Type == "Disk"):
    GetResourceUsage(DBInstanceId, Key)

elif (Type == "Performance"):

    #平均每秒钟的输入流量
    if (Key == "MySQL_NetworkTraffic_In"):
        IndexNum = 0
        MasterKey = "MySQL_NetworkTraffic"
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime)

    #平均每秒钟的输出流量
    elif (Key == "MySQL_NetworkTraffic_Out"):
        IndexNum = 1
        MasterKey = "MySQL_NetworkTraffic"
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime)

    #每秒SQL语句执行次数
    elif (Key == "MySQL_QPS"):
        IndexNum = 0
        MasterKey = "MySQL_QPSTPS"
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime)

    #平均每秒事务数
    elif (Key == "MySQL_TPS"):
        IndexNum = 1
        MasterKey = "MySQL_QPSTPS"
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime)

    #当前活跃连接数
    elif (Key == "MySQL_Sessions_Active"):
        MasterKey = "MySQL_Sessions"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #当前总连接数
    elif (Key == "MySQL_Sessions_Totle"):
        MasterKey = "MySQL_Sessions"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #InnoDB缓冲池的读命中率
    elif (Key == "ibuf_read_hit"):
        MasterKey = "MySQL_InnoDBBufferRatio"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #InnoDB缓冲池的利用率
    elif (Key == "ibuf_use_ratio"):
        MasterKey = "MySQL_InnoDBBufferRatio"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #InnoDB缓冲池脏块的百分率
    elif (Key == "ibuf_dirty_ratio"):
        MasterKey = "MySQL_InnoDBBufferRatio"
        IndexNum = 2
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #InnoDB平均每秒钟读取的数据量
    elif (Key == "inno_data_read"):
        MasterKey = "MySQL_InnoDBDataReadWriten"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #InnoDB平均每秒钟写入的数据量
    elif (Key == "inno_data_written"):
        MasterKey = "MySQL_InnoDBDataReadWriten"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒向InnoDB缓冲池的读次数
    elif (Key == "ibuf_request_r"):
        MasterKey = "MySQL_InnoDBLogRequests"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒向InnoDB缓冲池的写次数
    elif (Key == "ibuf_request_w"):
        MasterKey = "MySQL_InnoDBLogRequests"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒日志写请求数
    elif (Key == "Innodb_log_write_requests"):
        MasterKey = "MySQL_InnoDBLogWrites"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒向日志文件的物理写次数
    elif (Key == "Innodb_log_writes"):
        MasterKey = "MySQL_InnoDBLogWrites"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒向日志文件完成的fsync()写数量
    elif (Key == "Innodb_os_log_fsyncs"):
        MasterKey = "MySQL_InnoDBLogWrites"
        IndexNum = 2
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MySQL执行语句时在硬盘上自动创建的临时表的数量
    elif (Key == "tb_tmp_disk"):
        MasterKey = "MySQL_TempDiskTableCreates"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MyISAM平均每秒Key Buffer利用率
    elif (Key == "Key_usage_ratio"):
        MasterKey = "MySQL_MyISAMKeyBufferRatio"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MyISAM平均每秒Key Buffer读命中率
    elif (Key == "Key_read_hit_ratio"):
        MasterKey = "MySQL_MyISAMKeyBufferRatio"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MyISAM平均每秒Key Buffer写命中率
    elif (Key == "Key_write_hit_ratio"):
        MasterKey = "MySQL_MyISAMKeyBufferRatio"
        IndexNum = 2
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MyISAM平均每秒钟从缓冲池中的读取次数
    elif (Key == "myisam_keyr_r"):
        MasterKey = "MySQL_MyISAMKeyReadWrites"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MyISAM平均每秒钟从缓冲池中的写入次数
    elif (Key == "myisam_keyr_w"):
        MasterKey = "MySQL_MyISAMKeyReadWrites"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MyISAM平均每秒钟从硬盘上读取的次数
    elif (Key == "myisam_keyr"):
        MasterKey = "MySQL_MyISAMKeyReadWrites"
        IndexNum = 2
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MyISAM平均每秒钟从硬盘上写入的次数
    elif (Key == "myisam_keyw"):
        MasterKey = "MySQL_MyISAMKeyReadWrites"
        IndexNum = 3
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒Delete语句执行次数
    elif (Key == "com_delete"):
        MasterKey = "MySQL_COMDML"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒Insert语句执行次数
    elif (Key == "com_insert"):
        MasterKey = "MySQL_COMDML"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒Insert_Select语句执行次数
    elif (Key == "com_insert_select"):
        MasterKey = "MySQL_COMDML"
        IndexNum = 2
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒Replace语句执行次数
    elif (Key == "com_replace"):
        MasterKey = "MySQL_COMDML"
        IndexNum = 3
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒Replace_Select语句执行次数
    elif (Key == "com_replace_select"):
        MasterKey = "MySQL_COMDML"
        IndexNum = 4
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒Select语句执行次数
    elif (Key == "com_select"):
        MasterKey = "MySQL_COMDML"
        IndexNum = 5
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒Update语句执行次数
    elif (Key == "com_update"):
        MasterKey = "MySQL_COMDML"
        IndexNum = 6
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒从InnoDB表读取的行数
    elif (Key == "inno_row_readed"):
        MasterKey = "MySQL_RowDML"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒从InnoDB表更新的行数
    elif (Key == "inno_row_update"):
        MasterKey = "MySQL_RowDML"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒从InnoDB表删除的行数
    elif (Key == "inno_row_delete"):
        MasterKey = "MySQL_RowDML"
        IndexNum = 2
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒从InnoDB表插入的行数
    elif (Key == "inno_row_insert"):
        MasterKey = "MySQL_RowDML"
        IndexNum = 3
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #平均每秒向日志文件的物理写次数
    elif (Key == "Inno_log_writes"):
        MasterKey = "MySQL_RowDML"
        IndexNum = 4
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MySQL实例CPU使用率(占操作系统总数)
    elif (Key == "cpuusage"):
        MasterKey = "MySQL_MemCpuUsage"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MySQL实例内存使用率(占操作系统总数)
    elif (Key == "memusage"):
        MasterKey = "MySQL_MemCpuUsage"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #MySQL实例的IOPS（每秒IO请求次数）
    elif (Key == "io"):
        MasterKey = "MySQL_IOPS"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #ins_size实例总空间使用量
    elif (Key == "ins_size"):
        MasterKey = "MySQL_DetailedSpaceUsage"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #data_size数据空间
    elif (Key == "data_size"):
        MasterKey = "MySQL_DetailedSpaceUsage"
        IndexNum = 1
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #log_size日志空间
    elif (Key == "log_size"):
        MasterKey = "MySQL_DetailedSpaceUsage"
        IndexNum = 2
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #tmp_size临时空间
    elif (Key == "tmp_size"):
        MasterKey = "MySQL_DetailedSpaceUsage"
        IndexNum = 3
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #other_size系统空间
    elif (Key == "other_size"):
        MasterKey = "MySQL_DetailedSpaceUsage"
        IndexNum = 4
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)
