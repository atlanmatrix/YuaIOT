## Introduction
---
A lightweight IOT framework

## Requirements
---
MicroPython
Python3

## Definition
---
### Role
0 - watcher  
1 - processor  
2 - collector  

## Tasks
---
### Common
- 设备间互联、发现
- 服务、数据备份容灾机制

### Wacher Tasks
> 提供计算设备、边缘设备或其它软硬件实例的基本数据管理；提供设备的注册发现；提供固件更新等
- ESP32 固件管理
- 插件库
- 设备信息管理
- 设备注册发现管理

### Processor Tasks
> 提供收集器上传数据的管理、计算；任务下发
- 时序数据库
- 对边缘设备下发任务

### Collector Tasks
> 传感器数据收集；响应处理器下发的任务驱动其它元器件
- 固件升级
- 插件动态加载
- 状态展示
- 通过 Web 对引脚进行管理控制
- Mesh 组网
