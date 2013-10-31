#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import wx
import sys
import threading
from wrapper import *

Pros = { 1:  'ICMP',
		 2:  'IGMP',	
		 6:  'TCP',
		 17: 'UDP',
		 }

Arpops = { 1: 'ARP请求',
		   2: 'ARP应答',
		   3: 'RARP请求',
		   4: 'RARP应答',
		   }

class AddData(threading.Thread):

	def __init__(self, frame, zs):
		threading.Thread.__init__(self)
		self.frame = frame
		self.flag = threading.Event()
		self.status = threading.Event()
		self.flag.clear()
		#------------------------------------
		self.zsdata = zs
		self.datahead = self.zsdata.zhead
		
	def run(self):
		node = self.datahead
		while True:
			if self.flag.isSet():
				break			
			wx.CallAfter(self.frame.updateList, self.getdata(node))
			node = node.contents.next
			if bool(node) == False:
				time.sleep(1)
			else:
			 	time.sleep(0.01)

			#self.status.wait()
	def stop(self):
		self.flag.set()
	
	def getdata(self, node):
		data = node.contents.data
		macto =   '%02X%02X%02X-%02X%02X%02X' % (data[0], data[1], data[2], data[3], data[4], data[5])
		macfrom = '%02X%02X%02X-%02X%02X%02X' % (data[6], data[7], data[8], data[9], data[10], data[11])

		if data[12] == 0x08:
			if data[13] == 0x06:
				pro = 'ARP'
				ipfrom =  '%d.%d.%d.%d' % (data[28], data[29], data[30], data[31])
				ipto =    '%d.%d.%d.%d' % (data[38], data[39], data[40], data[41])
			elif data[13] == 0x00:
				ipfrom =  '%d.%d.%d.%d' % (data[26], data[27], data[28], data[29])
				ipto =    '%d.%d.%d.%d' % (data[30], data[31], data[32], data[33])
				pro = Pros.get(data[23])
		return [macfrom, macto, ipfrom, ipto, pro, node]
		
#--------------------------------------------------------------------------------
	
#--------------------------------------------------------------------------------
	
class MainFrame(wx.Frame):
	def __init__(self, parent, id):
		self.num = 0
		self.datalist = []
		wx.Frame.__init__(self, parent, id, u'网络协议分析器', size=(1000,600))
		self.Bind(wx.EVT_SIZE, self.onResize)
		#self.mainpanel = wx.Panel(self)
		self.createToolBar()
		self.createSplitter()
		self.createList()
		self.createTree()
		favicon = wx.Icon('../img/zs.png', wx.BITMAP_TYPE_ANY)
		self.SetIcon(favicon)
		#----------------------------------------------
		#wrapper
		self.zs = Interface()
		self.zs.init()
		
    #------------------------------------------------------------------------------		
	def createToolBar(self): #创建工具栏
		toolbar = self.CreateToolBar()
		for tool in self.getToolBarData(): 	
			self.addTool(toolbar, *tool) if tool != None else toolbar.AddSeparator()

		toolbar.Realize()	
		
	def getToolBarData(self): #工具定义
		return (('开始', '../img/tool-start.png', '开始捕获数据', self.onStart),
				('停止', '../img/tool-stop.png', '停止捕获数据', self.onStop),
				None,
				('清空', '../img/tool-clear.png', '清空列表', self.onClear),)
				#('设置', '..img/tool-preferences.png', '系统设置', self.onPreferences))
						
	def addTool(self, toolbar, label, imgfile, help, handler): #添加工具
		bmp = wx.Image(imgfile, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		tool = toolbar.AddSimpleTool(-1, bmp, label, help)
		self.Bind(wx.EVT_MENU, handler, tool)
		
	#工具栏 事件处理
	def onStart(self, event):
		print 'Start'
		self.zs.start()
		self.thread = AddData(self, self.zs)
		self.thread.start()
		self.updateflag = True
	def onClear(self, event):
		print 'Clear'
		self.onStop(event)
		self.updateflag = False
		self.zs.clean()
		self.list.DeleteAllItems()
		self.zs.init()
		self.num = 0
		self.tree.DeleteChildren(self.treeroot)
		del(self.datalist)
		self.datalist = []
	
	def onStop(self, event):
		self.updateflag = False
		self.zs.stop()
		self.thread.stop()
		
	def onRefresh(self, event):
		print 'Refresh'	

	#-----------------------------------------------------------------------------------			
	def createSplitter(self):
		self.mainsp = wx.SplitterWindow(self)
		self.lpanel = wx.Panel(self.mainsp, style=wx.SUNKEN_BORDER)
		self.rpanel = wx.Panel(self.mainsp, style=wx.SUNKEN_BORDER)	
		self.mainsp.SplitVertically(self.lpanel, self.rpanel, self.GetSize().x * 0.6)
		self.lpanel.SetSize(wx.Size(self.mainsp.GetSashPosition(), self.GetSize().y))
		self.rpanel.SetSize(wx.Size(self.GetSize().x - self.mainsp.GetSashPosition(), self.GetSize().y))
		self.mainsp.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.onSpResize)
		self.mainsp.Bind(wx.EVT_PAINT, self.onSpResize)
	
	def onSpResize(self, event):
		wsize = self.mainsp.GetSashPosition()
		psize = wx.Size(wsize, self.mainsp.GetSize().y)
		self.lpanel.SetSize(psize)		
		self.list.SetSize(wx.Size(wsize-5, self.mainsp.GetSize().y-5))
		
		self.rpanel.SetSize(wx.Size(self.GetSize().x - self.mainsp.GetSashPosition(), self.GetSize().y))
		self.tree.SetSize(wx.Size(self.rpanel.GetSize().x - 2, self.rpanel.GetSize().y-5))
		
		event.Skip()
	
	
	def onResize(self, event):
		self.mainsp.SetSashPosition(self.GetSize().x * 0.6)
		event.Skip()
	#----------------------------------------------------------------------------------	
	#列表
	def createList(self):
		self.list = wx.ListCtrl(self.lpanel, -1, style=wx.LC_REPORT)
		self.list.InsertColumn(0, '#',		width=40)
		self.list.InsertColumn(1, '源MAC',  	width=120)
		self.list.InsertColumn(2, '目的MAC',	width=120)
		self.list.InsertColumn(3, '源IP', 	width=130)
		self.list.InsertColumn(4, '目的IP', 	width=130)
		self.list.InsertColumn(5, '协议', 	width=50)
		
		self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
		
	def updateList(self, item):
		if self.updateflag == False:
			return
		index = self.list.InsertStringItem(sys.maxint, str(self.num))
		for i in range(0, 5):
			self.list.SetStringItem(index, i+1, item[i])
	
		self.datalist.append(item[5])
		self.num +=1
		
	def onItemSelected(self, event):
		item = event.GetItem()
		node = self.datalist[int(item.GetText())]
		self.tree.DeleteChildren(self.treeroot)
		data = self.getTreeData(node)
		self.addTreeNode(data)
		self.tree.ExpandAll()
	#------------------------------------------------------------------------------------
	#tree
	def createTree(self):
		self.tree = wx.TreeCtrl(self.rpanel, style=wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE)
		self.treeroot = self.tree.AddRoot("数据包")

	
	def getTreeData(self, node):
		data = node.contents.data
		self.datastart = 0;
		self.datasize = node.contents.size
		print self.datasize
		datalist = []
		
		ehead = '以太网'
		macto =   '目的MAC		%02X%02X%02X-%02X%02X%02X' % (data[0], data[1], data[2], data[3], data[4], data[5])
		macfrom = '源MAC 		%02X%02X%02X-%02X%02X%02X' % (data[6], data[7], data[8], data[9], data[10], data[11])
		
		ethpro =  '上层协议		0x%02X%02X' % (data[12], data[13])
		if data[0]==0xff and data[1]==0xff and data[2]==0xff and data[3]==0xff and data[4]==0xff and data[5]==0xff:
			ehead += ' (广播)' 
		datalist.append([ehead, macto, macfrom, ethpro])
		self.datastart = 14
		if data[12] == 0x08 and data[13] == 0x00:
			ipstart = 14
			ipvert = (data[14] & 0xF0) >> 4
			if ipvert != 4:
				return;
			ipver =   '版本号			%d' % (ipvert)
			iphlt = data[14] & 0x0F
			iphl =    '首部长度		%d' % (iphlt)
			iptos =   '服务类型		0x%02X' % (data[15])
			iptl =    '总长度			%d (byte)' % (data[16]*16+data[17])
			ipind =   '标识			0x%02X%02X' % (data[18], data[19])
			ipflag =  '标志			0x%02X' % (data[20] & 0xE0 >>5)
			ipoff =   '偏移			0x%02X%02X' % (data[20] & 0x1F, data[21])
			ipttl =   '生存时间		%d' % (data[22])
			ippro =   '上层协议		%d (%s)' % (data[23], Pros.get(data[23]))
			ipfrom =  '源IP地址		%d.%d.%d.%d' % (data[26], data[27], data[28], data[29])
			ipto =    '目的IP地址	%d.%d.%d.%d' % (data[30], data[31], data[32], data[33])
			ipopt = None
			if iphlt > 5:
				ipopts = '0x'
				for i in range(0, iphlt-5):
					ipots += '%02X' % (data[34+i])
				ipopt =   '其他			%s' % ipopts	
			datalist.append(['IP:', ipver, iphl, iptos, iptl, ipind, ipflag, ipoff, ipttl, ippro, ipfrom, ipto, ipopt])
			uper = ipstart+iphlt*4
			self.datastart = uper
			#UDP
			if data[23] == 17:
				udpfrom =  '源端口 		%d' % (data[uper]*16+data[uper+1])
				udpto   =  '目的端口     	%d' % (data[uper+2]*16+data[uper+3])
				udplen  =  '数据长度     	%d (byte)' % (data[uper+4]*16+data[uper+5])
				datalist.append(['UDP', udpfrom, udpto, udplen])
				self.datastart = uper+6
			#TCP	
			elif data[23] == 6:
				tcpfrom =  '源端口 		%d' % (data[uper]*16+data[uper+1])
				tcpto   =  '目的端口		%d' % (data[uper+2]*16+data[uper+3])
				tcpseq  =  '序号(SEQ) 	0x%02X%02X%02X%02X' % (data[uper+4], data[uper+5], data[uper+6], data[uper+7])
				tcpackn =  '确认号(ACK)	0x%02X%02X%02X%02X' % (data[uper+8], data[uper+9], data[uper+10], data[uper+11])
				tcphl	=  '头部长度		%d (byte)' % ((data[uper+12] & 0xF0)>>4)
				tcpurg  =  'URG			%d' % ((data[uper+13] & 0x20)>>5)
				tcpack  =  'ACK			%d' % ((data[uper+13] & 0x10)>>4)
				tcppst	=  'PST			%d' % ((data[uper+13] & 0x08)>>3)
				tcppsh  =  'PSH			%d' % ((data[uper+13] & 0x04)>>2)
				tcpsyn  =  'SYN			%d' % ((data[uper+13] & 0x02)>>1)
				tcpfin  =  'FIN			%d' % ((data[uper+13] & 0x01))
				tcpwin  =  '窗口大小		%d' % (data[uper+14]*16 + data[uper+15])
				datalist.append(['TCP', tcpfrom, tcpto, tcpseq, tcpackn, tcphl, tcpurg, tcpack, tcppst, tcppsh, tcpsyn, tcpfin])
				self.datastart = uper+16
			elif data[23] == 1:
				icmptype = '类型 			0x%02X' % (data[uper])
				icmpcode = '代码			0x%02X'	% (data[uper+1])
				icmpsum  = '校验和			0x%02X%02X' % (data[uper+2], data[uper+3])
				datalist.append(['ICMP', icmptype, icmpcode, icmpsum])
				self.datastart = uper+4 
		elif data[12] == 0x08 and data[13] == 0x06:
			arpstart = 14
			arphd	 =  '硬件类型			0x%02X%02X' % (data[14], data[15])
			arppro	 =  '协议类型			0x%02X%02x'	% (data[16], data[17])
			arphdl   =  '硬件地址长度		%d (byte)'	% (data[18])
			arpprol	 =  '协议地址长度		%d (byte)'  % (data[19])
			arpop	 =  '操作类型			0x%02X%02X(%s)' % (data[20], data[21], Arpops.get(data[21]))
			arpsmac  =  '发送方MAC		%02X%02X%02X-%02X%02X%02X' %(data[22], data[23], data[24], data[25], data[26], data[27])
			arpsip	 =  '发送方IP			%d.%d.%d.%d' % (data[28], data[29], data[30], data[31])
			arpdmac  =  '接收方MAC		%02X%02X%02X-%02X%02X%02X' %(data[32], data[33], data[34], data[35], data[36], data[37])
			arpdip   =  '接收方IP			%d.%d.%d.%d' % (data[38], data[39], data[40], data[41])
			datalist.append(['ARP', arphd, arppro, arphdl, arpprol, arpop, arpsmac, arpsip, arpdmac, arpdip])
			self.datastart = 42
		return datalist
		
	def addTreeNode(self, data):
		for item in data:
			if item == None:
				continue;
			node = self.tree.AppendItem(self.treeroot, item[0])
			for subitem in item[1:]:
				if subitem == None:
					continue;
				self.tree.AppendItem(node, subitem)


	#------------------------------------------------------------------------------------
	
	
	
	
	
		
if __name__ == '__main__':
	import time
	app = wx.PySimpleApp()
	frame = MainFrame(parent = None, id = -1)
	frame.Show()
	app.MainLoop()		
		

