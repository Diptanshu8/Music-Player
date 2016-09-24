import wx,os,pymedia,time,string
from string import maketrans 

class frame (wx.Frame):
    def __init__(self,parent,title):

        wx.Frame.__init__(self,parent,title = title,size = (400,300))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        subsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        subsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        subsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.st1 = wx.StaticText(panel,-1,"Add your Music",style = wx.ALIGN_CENTER) 

        self.tb1 = wx.TextCtrl(panel,-1) 

        self.splb1 = wx.Button(panel,-1,"Browse",pos = (0,-1))
        self.splb1.Bind(wx.EVT_BUTTON,self.browse)
        #VOlume control box
        self.sld= wx.Slider(panel,-1,50,0,100,(300,40),(-1,150), wx.SL_AUTOTICKS | wx.SL_VERTICAL | wx.SL_LABELS)
        #self.st2 = wx.StaticText(panel,-1,"Volume\nControl",(320,5),style = wx.ALIGN_CENTER)
        wx.StaticBox(panel, -1, "Volume", (300, 5), size=(75, 200),style = wx.ALIGN_CENTER)
        self.cb1 = wx.CheckBox(panel,1,"Mute",(320,25))
        #self.cb1.Bind(wx.EVT_CHECKBOX,self.Mute)
        
        self.b1 = wx.Button(panel,-1,"Play")
        self.b1.Bind(wx.EVT_BUTTON,self.Play)

        self.b2 = wx.Button(panel,-1,"Stop")
        self.b2.Bind(wx.EVT_BUTTON,self.Stop)
        
        self.b3 = wx.Button(panel,-1,"Pause")
        self.b3.Bind(wx.EVT_BUTTON,self.Pause)

        self.b4 = wx.Button(panel,-1,"Close this app")
        self.b4.Bind(wx.EVT_BUTTON,self.Exit)
        
        self.b5 = wx.Button(panel,-1,"Add this track to queue")
        self.b5.Bind(wx.EVT_BUTTON,self.addtrack)

        self.b6 = wx.Button(panel,-1,"Play queue")
        self.b6.Bind(wx.EVT_BUTTON,self.playqueue)

        self.b7 = wx.Button(panel,-1,"Skip track")
        self.b7.Bind(wx.EVT_BUTTON,self.skiptrack)

        self.b8 = wx.Button(panel,-1,"Previous track")
        self.b8.Bind(wx.EVT_BUTTON,self.previoustrack)

        subsizer1.Add(self.st1,0,0,0)
        subsizer1.Add(self.splb1,0,flag  = wx.ALIGN_RIGHT)
        sizer.Add(subsizer1,0,0,0)

        subsizer2.Add(self.b1,0,0,0)
        subsizer2.Add(self.b2,0,0,0)
        subsizer2.Add(self.b3,0,0,0)

        subsizer3.Add(self.b8,0,0,0)
        subsizer3.Add(self.b6,0,0,0)
        subsizer3.Add(self.b7,0,0,0)

        
        
        sizer.Add(self.tb1,0,0,0)
        sizer.Add(subsizer2,0,0,0)
        sizer.Add(subsizer3,0,0,0)
        sizer.Add(self.b4,0,0,0)
        sizer.Add(self.b5,0,0,0)       
        
        
        panel.SetSizer(sizer)

        self.address=''
        self.temp = 0
        self.queuecounter = 0
        self.queue = []
        #self.songtime = 0
        self.Centre()
        self.Show()

    def browse(self,e):
            wildcard = "Music Files (*.mp3)|*.mp3| ""All files (*.*)|*.*"
            dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)   
            if dialog.ShowModal() == wx.ID_OK:
                self.address = str(dialog.GetPath())
                sname = self.address
                self.tb1.SetValue(sname.split("\\")[-1])
            dialog.Destroy()
            
    def playqueue(self,e):
        with open('E:\exp.txt') as g:
            text = str(g.read())
        self.queue = str.split(text,'\n')
        self.player = pymedia.Player()
        self.queuecounter = 0
        #self.player.start() 
        self.timer = wx.Timer(self,-1)
        self.Bind(wx.EVT_TIMER,self.queuecontinue)
        a =(self.player.getLength)
        self.timer.Start(1000)

    def queuecontinue(self,e):
        if self.player.isPlaying():
            pass;
        elif self.queuecounter<len(self.queue):
            add = self.queue[self.queuecounter]
            self.queuecounter+=1
            self.address = str(add)
            self.Play(e)
    
    def skiptrack(self,e):
        self.Stop(e)
        self.create_player
        self.queuecontinue(e)

    def previoustrack(self,e):
        self.Stop(e)
        self.queuecounter-=2
        self.create_player
        self.queuecontinue(e)

    def addtrack(self,e):
        f = open('E:\exp.txt','a')
        if self.address != '':
            f.write(self.address)
            f.write('\n')

    def create_player(self):
        self.player = pymedia.Player()
        self.player.start()

    def Mute(self,e):
        self.player.setVolume(0)

    def Play(self,e):
        
        if self.temp == 0 and self.address != '':
            self.create_player()
            self.temp = 1
        if self.address == '':
            self.browse(e)
        
        self.player.startPlayback(self.address)
        

    def Stop(self,e):
        self.player.stopPlayback()
        self.player.stop()
        self.temp = 0
        
    def Pause(self,event):
        self.player.pausePlayback()

    def Exit(self,e):
        self.player.stop()
        self.Close()
    
app = wx.App()
a = frame(None,'Music')
app.MainLoop()

    
