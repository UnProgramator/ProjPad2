'''
    @version 0.1
    author: Pescaru Alexandru-Mihai
'''
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkm
import importlib as imp


class Message:
    warning = tkm.showwarning
    error = tkm.showerror
    info = tkm.showinfo
    quest = tkm.askquestion

msg = Message


class page:
    on_page_activate=None
    on_page_deactivate=None
    '''
        the first parameter must be a reference to the root page or to another frame
        the other parameters are use only in case that the page in not linked to the root
    '''
    def __init__(self,master,name=None,row=0,column=0,height=1000,width=1000,sticky="nsew",**options):
        self.fr=tk.Frame(master,height=height,width=width,**options)
        #self.fr.grid(row=row,column=column,sticky=sticky)
        self.grid_val={'row':row,'column':column,'sticky':sticky}
        self.hiden=True
        self.widgets = {}
        self.name=name

    '''this function is used to add the widget in the dictionary, based on it's type
            *it's tested if it's key already exists
                _if it's in the dict already then the key is modified
             then the key is inserted in the dict
             the named is returned in case of modification
        '''
    def nameCorection(self,obj,name=None):
        # wid = widget ID - for example for a button is tk.Button
        wid=type(obj).__name__
        
        # i verify if the key exists in the widgets dict
        if wid not in self.widgets:
            self.widgets[wid]={}
                
        #I insert the new object acordenly
        if name in self.widgets[wid]:
            i=0;
            while name+str(i) in self.widgets[wid]:
                i+=1
            name+=str(i)
        self.widgets[wid][name]=obj
        return name

    def setUndefinedWidget(self, w_type,w_id, row, column, sticky='nsew', **options):
        self.widgets[w_type][w_id].grid(row=row,column=column,sticky=sticky,**options)
    
    def addWidget(self, widget_type_name, w_id, **options):
        class_ = getattr(tk, widget_type_name)
        try:
            wd = class_(self.fr, **options)
            return self.nameCorection(name=w_id,obj=wd)
        except Exception as E:
            raise E 

    def setOnPageActivateEvent(self, command):
        self.on_page_activate=command

    def setOnPageDeactivateEvent(self, command):
        self.on_page_deactivate=command

    def deleteOnPageActivateEvent(self):
        self.on_page_activate=None

    def deleteOnPageDeactivateEvent(self):
        self.on_page_deactivate=None

    def addTtkWidget(self, widget_type_name, w_id, **options):
        class_ = getattr(ttk, widget_type_name)
        wd = class_(self.fr, **options)
        return self.nameCorection(name=w_id,obj=wd)
        
    def addButton(self,b_id,name,row,column,sticky='nsew',**options):
        bt = tk.Button(self.fr,text=name,**options)
        bt.grid(row=row,column=column,sticky=sticky)
        return self.nameCorection(name=b_id,obj=bt)

    def addText(self,text,row,column,sticky='nsew',**options):
        lb = tk.Label(self.fr,text=text,**options)
        lb.grid(row=row,column=column,sticky=sticky)
        return self.nameCorection(name=text,obj=lb)

    def addListbox(self,name,row,column,columnspan=None,height=2,width=80,**options):
        if columnspan is None:
            columnspan=width/20
        lb = tk.Listbox(self.fr,height=height,width=width,**options)
        lb.grid(row=row,column=column,rowspan=height)
        return self.nameCorection(name=t_id,obj=lb)

    def addEntryfield(self,entry_id,row,column,defaultText='',**option):
        ef=tk.Entry(self.fr,**option)
        ef.grid(row=row,column=column)
        ef.insert(0,defaultText)
        return self.nameCorection(name=entry_id,obj=ef)

    '''
        columnName : dict key = name, value = width
    '''
    def addTable(self,tableName:str,columnNames:dict,row,column,rowNo=1,rowSpan=None,colSpan=None,**option):
        tb = Table(self.fr,columnNames,height=rowNo+1,row=row,column=column,rowSpan=rowSpan, **option)
        return self.nameCorection(name=tableName,obj=tb)
        
    def addFrame(self,name,row=0,column=0,sticky="nsew",**options):
        p=page(self.fr,name,row=row,column=column,sticky=sticky,**options)
        return self.nameCorection(name=name,obj=p,wid=page)
    
    '''return a reference to the curent frame, or, else if the name is not None
        it returns a reference to an sub-frame'''
    def getFrame(self,name=None):
        if name is None:
            return self.fr
        else :
            return self.get_widget(tk.Frame,name)

    def addEvent(self,widget_type,widget_id,event,command):
        try:
            wd=self.widgets[widget_type][widget_id]
            wd.bind(event,command)
        except KeyError as ke:
            print('cheie inexistenta \n')
            raise ke
        except AttributeError as ae:
            print('clasa ' + widget_type + ' don\'t have the atribute nedded in ' + command)
            raise ae
        except Exception as e:
            print(e)
            raise e

    def getWidget(self,widget_type_name,widget_id):
        try:
            wd=self.widgets[widget_type_name][widget_id]
            return  wd
        except KeyError as ke:
            print('cheie inexistenta \n')
            raise ke
        except Exception as e:
            print(e)
            raise e

    def value_of_Entry(self,entry_id):
        return self.widgets[tk.Entry][entry_id].get()
    
    def activate_page(self):
        if self.on_page_activate is not None:
            self.on_page_activate()
        if self.hiden:
            self.fr.grid(**self.grid_val)
            self.fr.tkraise()
            self.hiden=False

    def deactivate_page(self):
        if self.on_page_deactivate is not None:
            self.on_page_deactivate()
        if not self.hiden:
            self.fr.grid_remove()
            self.hiden=True
    
    def __del__(self):
        for i in self.widgets:
            i.destroy()
        self.fr.destroy()

'''
    Table class used for the consistency of the page class - for the wid
    (see page.nameCorection()_
'''

class Table:

    def __init__(self,master:page,columnNames,height,row,column,rowSpan=None,colSpan=None,arrowScroll=True,**options):
        self.master=master
        self.tree=ttk.Treeview(master,columns=tuple(columnNames),**options)
        self.tree['show']='headings'
        self.tree.grid(row=row,column=column,rowspan=rowSpan,columnspan=colSpan)
        self.hidenColumns = []
        for colname,colwidth in columnNames.items():
            self.tree.heading(colname,text=colname)
            self.tree.column(colname,width=colwidth)
        if arrowScroll is True:
            self.tree.bind('<Up>',self.tree.yview)
            self.tree.bind('<Down>',self.tree.yview)
            self.tree.focus()

    def hideColumn(self, colname):
        if type(colname) is str:
            self.hidenColumns += [colname]
        else:
            self.hidenColumns += colname
        disp = []
        for col in self.tree['columns']:
            if col in self.hidenColumns:
                continue
            disp += [col]
        self.tree["displaycolumns"] = disp

    def showAllColumn():
        self.tree["displaycolumns"] = self.tree['columns']
        self.hidenColumns=[]
    
    def attatchScrollbar(self,scrollbar):
        self.tree.configure(yscrollcommand=scrollbar.set)

    def bind(self, event:str, action):
        self.tree.bind(event,action)

    def getValue(self, contextEvent, fieldName="all"):
        item = self.tree.identify('item',contextEvent.x,contextEvent.y)
        print(item)
        return self.tree.item(item, "text")
    
    def append(self,fillers):
        tg=1;
        for fls in fillers:
            self.tree.insert('','end',fls[0],tag=tg)
            if tg==1:
                tg=0
            else:
                tg=1
            if len(fls) == len(self.tree['column']):
                i=0
            else:
                i=1
            for col in self.tree['column']:
                self.tree.set(fls[0],col,fls[i])
                i=i+1
        
    '''which atribute can take the values all for delete all, first for del first, or the atribute name'''
    def deleteContent(self,which='all'):
        if which == 'all':
            self.tree.delete(*self.tree.get_children())
        elif which == 'first':
            try:
                self.tree.delete(self.tree.get_children()[0])
            except:
                pass
        elif which == 'selected':
            selected_item = self.tree.selection()[0]
            self.tree.delete(selected_item)
        else:
            try:
                self.tree.delete(which)
            except Exception as e:
                msg.warning('item inexistent','The content you want to delete doesn\'t exists')
    def getSelectedItem(self):
        itemID = self.tree.focus()
        return self.tree.item(itemID)['values']
                  
'''
    colection of frames - page - that makes an programm

class pageColection:
    pass
'''


class window:
    
    def __init__(self,pageName='untitled'):
        self.win=tk.Tk(className=pageName)
        self.frames={}

    def getRoot(self):
        return self.win

    def makePage(self, name=None,**options):
        tmp = page(self.win, name=name, **options)
        self.addFrame(name, tmp)
        return tmp

    def addFrame(self,name:str,frame:page):
        self.frames[name]=frame
    
    def __del__(self):
        self.win.destroy()
