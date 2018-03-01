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