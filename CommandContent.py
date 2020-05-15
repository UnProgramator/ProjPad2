import Gui as gui

#in afara o sa lucrez direct doar cu MakeUI
class MakeUI():
    def __init__(self):
        self.win=gui.window()
        self.cc=CommandContent(self.win)
        self.ct=CommandTable(self.win)
        self.cl=ClientList(self.win)
        #legare pagini; stiu ca nu e frumos, dar merge
        self.cl.nextPage=self.ct.pag
        self.ct.previousePage=self.cl.pag
        self.ct.nextPage=self.cc.pag
        self.cc.previousePage=self.ct.pag

    def make(self):
        self.cc.makePage()
        self.cl.makePage()
        self.ct.makePage()
        self.cl.pag.activate_page()
    
    def setFinishedOrderCommand(self, command):
        self.cc.setOrderFinishCommand(command)

    def setTakeOrderCommand(self, command):
        self.cc.setOrderTakeCommand(command)

    def setOrderGetterCommand(self, command):
        self.cc.setOrderGetterCommand(command)
        
    def setOrderSetterCommand(self, command):
        self.ct.setOnOrderSelectCommand(command)   

    def setOrderListGetterCommand(self, command):
        self.ct.setContentGetter(command)

    def setClientSelectGetterCommand(self, command):
        self.cl.setOnClientSelectCommand(command)

    def setClientListGetter(self, command):
        self.cl.setContentGetter(command)

#restul e, cum ar veni, private
class CommandContent:
    finshOrder=None
    takeOrder=None
    pag=None
    table=None
    previousePage=None
    orderGetter=None
    def setOrderFinishCommand(self,ordeFinishCommand):
        self.finshOrder=ordeFinishCommand
    def setOrderTakeCommand(self,ordeTakeCommand):
        self.takeOrder=ordeTakeCommand
    def setOrderGetterCommand(self,command):
        self.orderGetter = command
    
    def __init__(self,wind):
        self.pag = wind.makePage("CommandFoodList",height=800, width=1500)
        
    def makePage(self):
        self.pag.setOnPageActivateEvent(self.onPageBringFront)
        self.pag.setOnPageDeactivateEvent(self.onPagePushBack)
        self.pag.addText(20*' ',0,0)
        self.pag.addText(20*' ',100,100)
        self.pag.addText('Produse de procesate', row=1, column=2)
        self.pag.addText('Produse doar de livrat', row=20, column=2)
        self.pag.addButton("Back","Back to order list", row=1, column=1)
        self.pag.addButton("FinishOrder","Finish Order", row=2, column=10)
        self.pag.addButton("TakeOrder","Take Order", row=3, column=10)
        self.pag.addTable("OrderContent", {"Product ID":100, "Product":400, "Quantity":100}, row=2, column=2, rowSpan=10)
        self.pag.addTable("OtherContent", {"Product ID":100, "Product":400, "Quantity":100}, row=21, column=2, rowSpan=10)
        self.pag.addWidget("Scrollbar", "verticalscroll")
        self.pag.addWidget("Scrollbar", "verticalscroll1")
        self.pag.setUndefinedWidget("Scrollbar","verticalscroll",row=2, column=3, sticky='w', rowspan=10)
        self.pag.setUndefinedWidget("Scrollbar","verticalscroll1",row=21, column=3, sticky='w', rowspan=10)
        self.pag.addEvent("Button", "Back", "<Button-1>", self.returnPage)
        self.pag.addEvent("Button", "FinishOrder", "<Button-1>", self.finishEvent)
        self.pag.addEvent("Button", "TakeOrder", "<Button-1>", self.takeEvent)
        self.table= self.pag.getWidget("Table","OrderContent")
        self.tableO= self.pag.getWidget("Table","OtherContent")
        scrollbar= self.pag.getWidget("Scrollbar","verticalscroll")
        scrollbarO= self.pag.getWidget("Scrollbar","verticalscroll1")
        self.table.attatchScrollbar(scrollbar)
        self.tableO.attatchScrollbar(scrollbarO)
    
    def returnPage(self, event):
        self.pag.deactivate_page()
        self.previousePage.activate_page()

    def setOrderTableContent(self,orderContent):
        self.table.append(orderContent['food'])
        self.tableO.append(orderContent['nonfood'])

    def takeEvent(self, event):
        try:
            self.takeOrder()
            gui.msg.info("Success", "Comanda a fost preluata cu succes")
        except Exception as e:
            gui.msg.warning("Error", "Eroare la preluarea comenzii! \n"+str(e))
    
    def finishEvent(self,event):
        try:
            self.finshOrder()
            gui.msg.info("Success", "Comanda a fost finalizata cu succes")
            self.table.deleteContent()
            self.pag.deactivate_page()
            self.previousePage.activate_page()
        except Exception as e:
            gui.msg.warning("Error", "Eroare la finalizarea comenzii! \n"+str(e))
            
    def onPageBringFront(self):
        self.setOrderTableContent(self.orderGetter())

    def onPagePushBack(self):
        self.table.deleteContent()
    
class CommandTable:
    nextPage=None
    previousePage=None
    pag = None
    onOrderSelect = None
    orderTable = None
    getContent = None
    table=None
    def setOnOrderSelectCommand(self, command):
        self.onOrderSelect = command
    def setContentGetter(self, getter):
        self.getContent = getter

    def __init__(self,wind):
        self.pag = wind.makePage("ClientCommandsList",height=800, width=1500)
        

    def makePage(self):
        self.pag.setOnPageActivateEvent(self.onPageBringFront)
        self.pag.setOnPageDeactivateEvent(self.onPagePushBack)
        self.pag.addText(20*' ',0,0)
        self.pag.addText(20*' ',100,100)
        self.pag.addButton("Back","Back to clinet list", row=1, column=1)
        self.pag.addTable("CommandList", {"ID":0, "Command time":200, "State":100, "Number of items":100}, row=2, column=2, rowSpan=10)
        self.pag.addEvent("Button","Back","<Button-1>", self.goback)
        self.pag.addEvent("Table","CommandList","<Double-1>", self.onOrderClick)
        self.table = self.pag.getWidget("Table","CommandList")
        self.table.hideColumn('ID')
        
    def goback(self,event):
        self.pag.deactivate_page()
        self.previousePage.activate_page()
  
    def onOrderClick(self,event):
        orderId = self.table.getSelectedItem()
        self.onOrderSelect(orderId[0],orderId[2])
        self.pag.deactivate_page()
        self.nextPage.activate_page()

    def onPageBringFront(self):
        self.table.append(self.getContent())

    def onPagePushBack(self):
        self.table.deleteContent()
    
class ClientList:
    nextPage=None
    pag = None
    OnClientSelect = None
    getContent = None
    table=None
    def setOnClientSelectCommand(self, command):
        self.OnClientSelect = command
    def setContentGetter(self, getter):
        self.getContent = getter
    
    def __init__(self,wind):
        self.pag = wind.makePage("ClientCommandsList",height=800, width=1500)
        

    def makePage(self):
        self.pag.setOnPageActivateEvent(self.onPageBringFront)
        self.pag.addText(20*' ',0,0)
        self.pag.addText(20*' ',100,100)
        self.pag.addTable("ClientList", {"ID":0, "Client":1200}, row=2, column=2, rowSpan=10)
        self.pag.addEvent("Table","ClientList","<Double-1>", self.onClientClick)

        self.table = self.pag.getWidget("Table","ClientList")
        self.table.hideColumn('ID')
    
    def onClientClick(self,event):
        clientId= self.table.getSelectedItem()
        self.OnClientSelect(clientId[0])
        self.pag.deactivate_page()
        self.table.deleteContent()
        self.nextPage.activate_page()

    def onPageBringFront(self):
        self.table.append(self.getContent())
        self.table = self.pag.getWidget("Table","ClientList")
        
