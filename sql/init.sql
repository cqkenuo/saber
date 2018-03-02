--node属性表
CREATE TABLE nodes(
id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
nodeName VARCHAR(20) NOT NULL , --节点名字
nodeJoinTime VARCHAR(20) NOT NULL , --节点加入时间
nodeLastTime VARCHAR (20) NOT NULL ,--节点签到时间
online INT(2) NOT NULL , --节点是否在线
st TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) DEFAULT CHARSET='utf8';

--server属性表
CREATE TABLE Servers(
id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
serverName VARCHAR (20) NOT NULL ,
serverTime VARCHAR (20) NOT NULL ,
st TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) DEFAULT CHARSET='utf8';

--node与server关系表
CREATE TABLE node_server(
nodeID INT (11),
serverID INT (11)
) DEFAULT CHARSET='utf8';

--要先建联合主键，再添加外键。顺序不能反了
ALTER TABLE node_server ADD CONSTRAINT ns_pk PRIMARY KEY(nodeID,serverID);
ALTER TABLE node_server ADD CONSTRAINT node_fk FOREIGN KEY(nodeID) REFERENCES nodes(id);
ALTER TABLE node_server ADD CONSTRAINT server_fk FOREIGN KEY(serverID) REFERENCES servers(id);

--删除外键约束
ALTER TABLE node_server DROP FOREIGN KEY node_fk;
ALTER TABLE node_server DROP FOREIGN KEY server_fk;


----------------------------------
--时间比较赶，先用以下表结构
--nodes
CREATE TABLE node_info(
id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
nHostname VARCHAR (20) NOT NULL ,
nIP VARCHAR (20) NOT NULL ,
isMaster INT (2) NOT NULL DEFAULT 0,
st TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) DEFAULT CHARSET='utf8';

--param
CREATE TABLE param(
id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
pKey VARCHAR (20) NOT NULL ,
pValue VARCHAR (20) NOT NULL ,
pRemark VARCHAR (20) NOT NULL DEFAULT '_',
st TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)DEFAULT CHARSET='utf8';

INSERT into  param(pKey,pValue,pReamrk) values('','','');
INSERT INTO  node_info(nHostname,nIP,isMaster) VALUES ('VM_217_177_centos','10.104.217.177',1);
INSERT INTO  node_info(nHostname,nIP,isMaster) VALUES ('VM_217_177_centos','10.104.217.177',0);