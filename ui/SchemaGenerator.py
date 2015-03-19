__author__ = 'dingming'

import os
import wx
import wx.grid
from domain.FunctionalDependency import FunctionalDependency
from domain.Relation import Relation
from api.GUIApi import normalize_relation


class MainFrame(wx.Frame) :
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, style = wx.CLOSE_BOX ,size = wx.Size(500, 450))
        self.relation = None
        self.NF = "NIL"

        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)

        schemaDeleteButton = wx.Button(self,-1,"Delete", size=(40,20))
        self.Bind(wx.EVT_BUTTON, self.OnDeleteDomain, schemaDeleteButton)

        schemaNewButton = wx.Button(self,-1, "New")
        self.Bind(wx.EVT_BUTTON, self.OnNew, schemaNewButton)

        schemaEditButton = wx.Button(self,-1, "Edit")
        self.Bind(wx.EVT_BUTTON, self.OnEdit, schemaEditButton)

        self.schemaTable = SchemaTable(self)

        self.schemaTable.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnSingleCellSelection)

        titlePanel = wx.Panel(self)
        titleLabel = wx.StaticText(titlePanel, label = "Schema Generator ")

        nfPanel = wx.Panel(self)
        nfLabel = wx.StaticText(nfPanel, label = "Normal Form: ")
        rbPanel = wx.Panel(self)
        self.rb1 = wx.RadioButton(rbPanel, -1, '2NF',(10,0), style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(rbPanel, -1, '3NF',(70,0))
        self.rb3 = wx.RadioButton(rbPanel, -1, 'BCNF',(130,0))
        self.rb4 = wx.RadioButton(rbPanel, -1, '4NF', (190,0))
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton, id=self.rb1.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton, id=self.rb2.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton, id=self.rb3.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton, id=self.rb4.GetId())


        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(titlePanel, 1, wx.EXPAND)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(nfPanel)
        sizer4.Add(rbPanel)

        self.fdTable = FDTable(self)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(self.fdTable)

        fdDeleteButton = wx.Button(self,-1,"Delete", size=(40,20))
        self.Bind(wx.EVT_BUTTON, self.OnFDDelete, fdDeleteButton)

        fdNewButton = wx.Button(self,-1, "New")
        self.Bind(wx.EVT_BUTTON, self.OnFDNew, fdNewButton)

        fdEditButton = wx.Button(self,-1, "Edit")
        self.Bind(wx.EVT_BUTTON, self.OnFDEdit, fdEditButton)

        self.fdTable.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnFDSingleCellSelection)

        sizer6 = wx.BoxSizer(wx.VERTICAL)
        sizer6_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6_3 = wx.BoxSizer(wx.HORIZONTAL)

        sizer6_1.Add(fdNewButton, 1, wx.EXPAND)
        sizer6_2.Add(fdEditButton, 1, wx.EXPAND)
        sizer6_3.Add(fdDeleteButton, 1, wx.EXPAND)

        sizer6.Add(sizer6_1, 1, wx.EXPAND | wx.ALL, 10)
        sizer6.Add(sizer6_2, 1, wx.EXPAND | wx.ALL, 10)
        sizer6.Add(sizer6_3, 1, wx.EXPAND | wx.ALL, 10)

        fdSizer = wx.BoxSizer(wx.HORIZONTAL)
        fdSizer.Add(sizer5, 1, wx.EXPAND)
        fdSizer.Add(sizer6)

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_3 = wx.BoxSizer(wx.HORIZONTAL)

        sizer1_1.Add(schemaNewButton, 1, wx.EXPAND)
        sizer1_2.Add(schemaEditButton, 1, wx.EXPAND)
        sizer1_3.Add(schemaDeleteButton, 1, wx.EXPAND)

        sizer1.Add(sizer1_1, 1, wx.EXPAND | wx.ALL, 10)
        sizer1.Add(sizer1_2, 1, wx.EXPAND | wx.ALL, 10)
        sizer1.Add(sizer1_3, 1, wx.EXPAND | wx.ALL, 10)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.schemaTable)


        listSizer = wx.BoxSizer(wx.HORIZONTAL)

        listSizer.Add(sizer2, 1,wx.EXPAND)
        listSizer.Add(sizer1)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer3, 1, wx.ALIGN_CENTER)
        mainSizer.Add(listSizer, 1, wx.EXPAND | wx.ALL, 20)
        mainSizer.Add(fdSizer,1, wx.EXPAND | wx.ALL, 20)
        mainSizer.Add(sizer4)

        generateButton = wx.Button(self, -1, "Generate")
        self.Bind(wx.EVT_BUTTON, self.OnGenerate, generateButton)
        sizer9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer9.Add(generateButton)
        mainSizer.Add(sizer9)


        self.SetSizer(mainSizer)
        self.SetAutoLayout(1)
        self.Show(True)

        self.NF = "NONE"
        self.childView = None

    def OnAbout(self, event):
        dlg = wx.MessageDialog( self, "A small text editor", "About Sample Editor", wx.OK)
        dlg.ShowModal() # Show it
        # dlg.Destroy() # finally destroy it when finished.

    def OnExit(self, event):
        self.Close(True)

    def AddDomain(self, domainName, dataType):
        if domainName == "" or dataType == "" :
            dlg = wx.MessageDialog( self, "Domain Name Cannot Be Empty", "ERROR",wx.OK)
            dlg.ShowModal()
        else :
            self.schemaTable.AddDomain(domainName, dataType)

    def AddFD(self, LHS, operator, RHS):
        if len(LHS) == 0 or len(RHS) == 0 :
            dlg = wx.MessageDialog( self, "Invalid functional dependency. Please add again", "ERROR",wx.OK)
            dlg.ShowModal()
        else :
            self.fdTable.AddFD(LHS, operator,RHS)

    def EditTuple(self, rowNo, domainName, dataType):
        self.schemaTable.SetCellValue(rowNo, 1, domainName)
        self.schemaTable.SetCellValue(rowNo, 2, dataType)

    def OnDeleteDomain(self, event):
        if len(self.schemaTable.GetSelectedRows()) == 0 :
            dlg = wx.MessageDialog(self, "No Row Selected", "ERROR", wx.OK)
            dlg.ShowModal()
        else :
            rows = self.schemaTable.GetSelectedRows()
            for i in rows :
                self.schemaTable.DeleteRows(i)

    def OnSingleCellSelection(self, event):
        self.schemaTable.SelectRow(event.GetRow())


    def OnNew(self, event):
        self.childView = AddDomainDialog()

        self.childView.ShowModal()

    def OnEdit(self, event):
        if len(self.schemaTable.GetSelectedRows()) == 0 :
            dlg = wx.MessageDialog(self, "No Row Selected", "ERROR", wx.OK)
            dlg.ShowModal()
        else :
            rows = self.schemaTable.GetSelectedRows()
            self.childView = EditDomainDialog(rows[0])

            self.childView.ShowModal()

    def OnFDSingleCellSelection(self, event):
        self.fdTable.SelectRow(event.GetRow())

    def OnFDNew(self, event):
        self.childView = AddFDDomainDialog(-1)
        self.childView.ShowModal()

    def OnFDEdit(self, event):
        if len(self.fdTable.GetSelectedRows()) == 0 :
            dlg = wx.MessageDialog(self, "No Row Selected", "ERROR", wx.OK)
            dlg.ShowModal()
        else :
            rows = self.fdTable.GetSelectedRows()
            self.childView = AddFDDomainDialog(rows[0])
            self.childView.ShowModal()

    def OnFDDelete(self, event):
        if len(self.schemaTable.GetSelectedRows()) == 0 :
            dlg = wx.MessageDialog(self, "No Row Selected", "ERROR", wx.OK)
            dlg.ShowModal()
        else :
            rows = self.schemaTable.GetSelectedRows()
            for i in rows :
                self.schemaTable.DeleteRows(i)

    def OnGenerate(self, event):

        # check the domain table is not empty
        if self.schemaTable.GetNumberRows() == 0 :
            dlg = wx.MessageDialog(self, "No domain is added to the system. Fail to generate schema", "ERROR", wx.OK)
            dlg.ShowModal()
            return
        elif self.NF == "NIL" :
            dlg = wx.MessageDialog(self, "No normal form is specified. Fail to generate schema", "ERROR", wx.OK)
            dlg.ShowModal()
            return
        else :
            self.schemaList = []
            for i in range(0, self.schemaTable.GetNumberRows()) :
                tmp = {}
                tmp["name"] = self.schemaTable.GetCellValue(i, 1)
                tmp["type"] = self.schemaTable.GetCellValue(i, 2)
                self.schemaList.append(tmp)

        if self.fdTable.GetNumberRows() > 0 :
            self.fdList = []
            for i in range(0, self.fdTable.GetNumberRows()) :
                tmp = {}
                tmp["lhs"] = self.fdTable.GetCellValue(i,0)
                tmp["op"] = self.fdTable.GetCellValue(i,1)
                tmp["rhs"] = self.fdTable.GetCellValue(i,2)
                self.fdList.append(tmp)

        print self.schemaList
        print self.fdList
        self.runLogic()

    def runLogic(self):
        relationSet = set()
        for i in self.schemaList :
            relationSet.add(i["name"])

        fdSet = set()
        for i in self.fdList :
            lhs = set()
            rhs = set()
            for j in i["lhs"].split(", ") :
                if j != "" :
                    lhs.add(j)
            for k in i["rhs"].split(", ") :
                if k != "" :
                    rhs.add(k)
            fdSet.add(FunctionalDependency(lhs,rhs))

        self.relation = Relation(relationSet, fdSet)
        print self.relation

        soln = normalize_relation(self.relation, self.NF)

        print soln


    def OnRadioButton(self, event):
        if event.GetId() == self.rb1.GetId() :
            self.NF = "2nf"
        elif event.GetId() == self.rb2.GetId() :
            self.NF = "3nf"
        elif event.GetId() == self.rb3.GetId() :
            self.NF = "bcnf"
        elif event.GetId() == self.rb4.GetId() :
            self.NF = "4NF"
        else :
            self.NF = "NIL"


        print self.NF


class AddDomainDialog(wx.Dialog) :
    def __init__(self):
        wx.Dialog.__init__(self,frame,-1,"AddDomainDialog")
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        idomainNamePanel = wx.Panel(self)
        idomainNameLabel = wx.StaticText(idomainNamePanel, label = "Domain Name: ", style = wx.ALIGN_CENTER)
        idomainTypePanel = wx.Panel(self)
        idomainTypeLabel = wx.StaticText(idomainTypePanel, label = "Data Type: ", style = wx.ALIGN_CENTER)
        self.inameTextBox = wx.TextCtrl(self)
        self.itypeTextBox = wx.TextCtrl(self)
        addButton = wx.Button(self,-1, "Add")
        self.Bind(wx.EVT_BUTTON, self.OnSave, addButton)
        cancelButton = wx.Button(self,-1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancelButton)
        okButton = wx.Button(self,-1, "OK")
        self.Bind(wx.EVT_BUTTON, self.OnOK, okButton)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_1.Add(idomainNamePanel, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer1_2.Add(self.inameTextBox, 1, wx.EXPAND)
        sizer1_3.Add(idomainTypePanel, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer1_4.Add(self.itypeTextBox, 1, wx.EXPAND)
        sizer1.Add(sizer1_1)
        sizer1.Add(sizer1_2)
        sizer1.Add(sizer1_3)
        sizer1.Add(sizer1_4)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(okButton, 1, wx.EXPAND | wx.ALL, 20)
        sizer2.Add(addButton, 1, wx.EXPAND | wx.ALL, 20)
        sizer2.Add(cancelButton, 1, wx.EXPAND | wx.ALL, 20)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer1, 1, wx.EXPAND | wx.ALL, 20)
        mainSizer.Add(sizer2, 1, wx.EXPAND)

        self.SetSizer(mainSizer)
        self.Fit()

    def OnSave(self, event):
        if self.inameTextBox.GetValue() in frame.schemaTable.GetAllAttr() :
            dlg = wx.MessageDialog(self, "Domain with the same name is already added", "ERROR", wx.OK)
            dlg.ShowModal()
        else :
            frame.AddDomain(self.inameTextBox.GetValue(), self.itypeTextBox.GetValue())

    def OnCancel(self, event):
        self.EndModal(0)
        self.Close()
        frame.childView = None

    def OnClose(self, event):
        self.EndModal(0)
        self.Close()
        frame.childView = None

    def OnOK(self, event):
        if self.inameTextBox.GetValue() in frame.schemaTable.GetAllAttr() :
            dlg = wx.MessageDialog(self, "Domain with the same name is already added", "ERROR", wx.OK)
            dlg.ShowModal()
        else :
            frame.AddDomain(self.inameTextBox.GetValue(), self.itypeTextBox.GetValue())
        self.Close(True)


class EditDomainDialog(wx.Dialog) :
    def __init__(self,rowNo):

        self.rowNo = rowNo
        wx.Dialog.__init__(self,None,-1,"Edit Domain")
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        idomainNamePanel = wx.Panel(self)
        idomainNameLabel = wx.StaticText(idomainNamePanel, label = "Domain Name: ", style = wx.ALIGN_CENTER)
        idomainTypePanel = wx.Panel(self)
        idomainTypeLabel = wx.StaticText(idomainTypePanel, label = "Data Type: ", style = wx.ALIGN_CENTER)
        self.inameTextBox = wx.TextCtrl(self)
        self.itypeTextBox = wx.TextCtrl(self)
        name = frame.schemaTable.GetCellValue(rowNo, 1)
        type = frame.schemaTable.GetCellValue(rowNo, 2)
        self.inameTextBox.SetValue(name)
        self.itypeTextBox.SetValue(type)

        cancelButton = wx.Button(self,-1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancelButton)
        okButton = wx.Button(self,-1, "OK")
        self.Bind(wx.EVT_BUTTON, self.OnOK, okButton)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_1.Add(idomainNamePanel, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer1_2.Add(self.inameTextBox, 1, wx.EXPAND)
        sizer1_3.Add(idomainTypePanel, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer1_4.Add(self.itypeTextBox, 1, wx.EXPAND)
        sizer1.Add(sizer1_1)
        sizer1.Add(sizer1_2)
        sizer1.Add(sizer1_3)
        sizer1.Add(sizer1_4)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        sizer2.Add(okButton, 1, wx.EXPAND | wx.ALL, 20)
        sizer2.Add(cancelButton, 1, wx.EXPAND | wx.ALL, 20)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer1, 1, wx.EXPAND | wx.ALL, 20)
        mainSizer.Add(sizer2, 1, wx.EXPAND)

        self.SetSizer(mainSizer)
        self.Fit()


    def OnCancel(self, event):
        self.EndModal(0)
        frame.childView = None
        self.Destroy()

    def OnOK(self, event):
        if self.inameTextBox.GetValue() in frame.schemaTable.GetAllAttr() and self.inameTextBox.GetValue() != frame.schemaTable.GetCellValue(self.rowNo, 1):
            dlg = wx.MessageDialog(self, "Domain with the same name is already added", "ERROR", wx.OK)
            dlg.ShowModal()
        else :
            frame.EditTuple(self.rowNo, self.inameTextBox.GetValue(), self.itypeTextBox.GetValue())
        self.Close(True)

    def OnClose(self, event):
        self.EndModal(0)
        frame.childView= None
        self.Destroy()



class AddFDDomainDialog(wx.Dialog) :
    def __init__(self, rowNo):
        self.rowNo = rowNo
        wx.Dialog.__init__(self,frame,-1,"AddFDDialog")
        LHSPanel = wx.Panel(self)
        LHSLabel = wx.StaticText(LHSPanel, label = "LHS: ", style = wx.ALIGN_CENTER)
        RHSPanel = wx.Panel(self)
        RHSLabel = wx.StaticText(RHSPanel, label = "RHS: ", style = wx.ALIGN_CENTER)
        self.LHSList = SelectAttrTable(self)
        self.LHSList.SetColLabelValue(0, "LHS")
        self.LHSList.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnLHSSelection)
        self.RHSList = SelectAttrTable(self)
        self.RHSList.SetColLabelValue(0, "RHS")
        self.RHSList.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnRHSSelection)

        LHSAddButton = wx.Button(self, 0, "Add")
        self.Bind(wx.EVT_BUTTON, self.OnAttrAdd, LHSAddButton)
        LHSDeleteButton = wx.Button(self, 2, "Delete")
        self.Bind(wx.EVT_BUTTON, self.OnAttrDelete, LHSDeleteButton)
        LHSClearButton = wx.Button(self, 4 ,"Clear")
        self.Bind(wx.EVT_BUTTON, self.OnAttrClear, LHSClearButton)
        RHSAddButton = wx.Button(self, 1, "Add")
        self.Bind(wx.EVT_BUTTON, self.OnAttrAdd, RHSAddButton)
        RHSDeleteButton = wx.Button(self, 3, "Delete")
        self.Bind(wx.EVT_BUTTON, self.OnAttrDelete, RHSDeleteButton)
        RHSClearButton = wx.Button(self, 5 ,"Clear")
        self.Bind(wx.EVT_BUTTON, self.OnAttrClear, RHSClearButton)


        operator = ["->" , "->>"]
        self.operatorComboBox = wx.ComboBox(self, -1, choices = operator, style = wx.CB_READONLY)
        addButton = None
        if self.rowNo == -1 :
            addButton = wx.Button(self,-1, "Add")
            self.Bind(wx.EVT_BUTTON, self.OnSave, addButton)
        cancelButton = wx.Button(self,-1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancelButton)
        okButton = wx.Button(self,-1, "OK")
        self.Bind(wx.EVT_BUTTON, self.OnOK, okButton)


        LHSSizer = wx.BoxSizer(wx.VERTICAL)
        LHSSizer_1 = wx.BoxSizer()
        LHSSizer_2 = wx.BoxSizer()
        LHSSizer_1.Add(LHSPanel)
        LHSSizer_2.Add(self.LHSList)
        LHSSizer.Add(LHSSizer_1)
        LHSSizer.Add(LHSSizer_2)
        LHSSizer.Add(LHSAddButton, 1, wx.TOP|wx.BOTTOM, 5)
        LHSSizer.Add(LHSDeleteButton,1, wx.TOP|wx.BOTTOM, 5)
        LHSSizer.Add(LHSClearButton,1, wx.TOP|wx.BOTTOM, 5)

        RHSSizer = wx.BoxSizer(wx.VERTICAL)
        RHSSizer_1 = wx.BoxSizer()
        RHSSizer_2 = wx.BoxSizer()
        RHSSizer_1.Add(RHSPanel)
        RHSSizer_2.Add(self.RHSList)
        RHSSizer.Add(RHSSizer_1)
        RHSSizer.Add(RHSSizer_2)
        RHSSizer.Add(RHSAddButton, 1, wx.TOP|wx.BOTTOM, 5)
        RHSSizer.Add(RHSDeleteButton,1, wx.TOP|wx.BOTTOM, 5)
        RHSSizer.Add(RHSClearButton,1, wx.TOP|wx.BOTTOM, 5)

        operatorSizer = wx.BoxSizer()
        operatorSizer.Add(self.operatorComboBox)

        inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputSizer.Add(LHSSizer)
        inputSizer.Add(operatorSizer,1, wx.UP | wx.LEFT, 27)
        inputSizer.Add(RHSSizer)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        if addButton != None :
            sizer2.Add(addButton, 1, wx.EXPAND | wx.ALL, 20)
        sizer2.Add(okButton, 1, wx.EXPAND | wx.ALL, 20)
        sizer2.Add(cancelButton, 1, wx.EXPAND | wx.ALL, 20)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(inputSizer, 1, wx.EXPAND | wx.ALL, 20)
        mainSizer.Add(sizer2, 1, wx.EXPAND)

        if self.rowNo != -1 :
            LList = frame.fdTable.GetCellValue(self.rowNo, 0).split(", ")
            for i in LList :
                self.AddAttrToList(i, 0)
            RList = frame.fdTable.GetCellValue(self.rowNo, 2).split(", ")
            for i in RList :
                self.AddAttrToList(i, 1)
            self.operatorComboBox.SetValue(frame.fdTable.GetCellValue(self.rowNo, 1))

        self.SetSizer(mainSizer)
        self.Fit()

    def OnSave(self, event):
        LHS = self.LHSList.GetExistAttr()
        RHS = self.RHSList.GetExistAttr()
        opr = self.operatorComboBox.GetValue()
        if self.rowNo != -1 :
            LHSString = ""
            RHSString = ""
            for i in LHS :
                LHSString += i
                LHSString += ", "
            LHSString = LHSString[:len(LHSString)-2]
            for i in RHS :
                RHSString += i
                RHSString += ", "
            RHSString = RHSString[:len(RHSString)-2]

            isExist = False

            for i in range(0, frame.fdTable.GetNumberRows()) :
                if frame.fdTable.GetCellValue(i, 0) == LHSString and frame.fdTable.GetCellValue(i,1) == opr and frame.fdTable.GetCellValue(i,2) == RHSString :
                    isExist = True

            if isExist == True :
                dlg = wx.MessageDialog(self, "Same functional dependency have already been added", "ERROR", wx.OK)
                dlg.ShowModal()
            else :
                frame.fdTable.SetCellValue(self.rowNo, 0, LHSString)
                frame.fdTable.SetCellValue(self.rowNo, 1, opr)
                frame.fdTable.SetCellValue(self.rowNo, 2, RHSString)
        else :
            frame.AddFD(LHS,opr,RHS)

    def OnCancel(self, event):
        self.EndModal(0)
        self.Close()

    def OnOK(self, event):
        self.OnSave(event)
        self.Close(True)

    def OnAttrAdd(self, event):
        print "OnAttrAdd called"
        if event.GetId() == 0 :
            list = self.LHSList
        else :
            list = self.RHSList
        if len(list.GetRemainAttr()) == 0 :
            dlg = wx.MessageDialog(self, "All domains have already been added", "ERROR", wx.OK)
            dlg.ShowModal()
        else :
            self.addAttrView = AddAttrDialog(list.GetRemainAttr(), event.GetId())
            self.addAttrView.ShowModal()

    def OnAttrDelete(self, event):
        if event.GetId() == 2:
            if len(self.LHSList.GetSelectedRows()) == 0 :
                dlg = wx.MessageDialog(self, "No Row Selected", "ERROR", wx.OK)
                dlg.ShowModal()
            else :
                rows = self.LHSList.GetSelectedRows()
                for i in rows :
                    self.LHSList.DeleteRows(i)
        else :
            if len(self.RHSList.GetSelectedRows()) == 0 :
                dlg = wx.MessageDialog(self, "No Row Selected", "ERROR", wx.OK)
                dlg.ShowModal()
            else :
                rows = self.RHSList.GetSelectedRows()
                for i in rows :
                    self.RHSList.DeleteRows(i)

    def OnAttrClear(self, event):
        if event.GetId() == 4 :
            length = self.LHSList.GetNumberRows()
            for i in range(0,length) :
                self.LHSList.DeleteRows(0)
        else :
            length = self.RHSList.GetNumberRows()
            for i in range(0,length) :
                self.RHSList.DeleteRows(0)

    def OnLHSSelection(self, event):
        self.LHSList.SelectRow(event.GetRow())

    def OnRHSSelection(self, event):
        self.RHSList.SelectRow(event.GetRow())

    def AddAttrToList(self, name, index):
        if index == 0 :
            self.LHSList.AppendRows(1)
            self.LHSList.SetCellValue(self.LHSList.GetNumberRows()-1, 0, name)
        else :
            self.RHSList.AppendRows(1)
            self.RHSList.SetCellValue(self.RHSList.GetNumberRows()-1, 0, name)

class AddAttrDialog(wx.Dialog) :

    def __init__(self, attrList, index):
        self.attrList = attrList
        self.index = index
        wx.Dialog.__init__(self, frame.childView, -1, "Add Domain Dialog")
        self.AttrComboBox = wx.ComboBox(self, -1, choices = self.attrList, style = wx.CB_READONLY, size = (190,-1))
        OKButton = wx.Button(self, -1, "OK")
        self.Bind(wx.EVT_BUTTON, self.OnOK, OKButton)
        CancelButton = wx.Button(self,-1,"Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancel, CancelButton)
        panel = wx.Panel(self)
        text = wx.StaticText(panel, label = "Please Select Domain : ", style = wx.ALIGN_LEFT)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        sizer1.Add(self.AttrComboBox,1, wx.EXPAND | wx.LEFT, 10)
        sizer2.Add(OKButton, 1, wx.ALL, 10)
        sizer2.Add(CancelButton,1, wx.ALL,10)
        mainSizer.Add(panel, 1, wx.ALL, 10)
        mainSizer.Add(sizer1)
        mainSizer.Add(sizer2)

        self.SetSizer(mainSizer)
        self.Fit()
        print "Dialog add made"

    def OnOK(self,event):
        if self.AttrComboBox.GetValue() != None and self.AttrComboBox.GetValue() != "" :
            frame.childView.AddAttrToList(self.AttrComboBox.GetValue(), self.index)
        # self.EndModal(0)
        # frame.childView.ShowModal()
        self.Close(True)
    def OnCancel(self,event):
        self.Close(True)

class SchemaTable(wx.grid.Grid) :
    def __init__(self, parent):
        wx.grid.Grid.__init__(self,parent,-1, size = (500, 130))
        self.SetColSizes(wx.grid.GridSizesInfo(103, range(0,2)))
        self.SetDefaultCellBackgroundColour(wx.Colour(0,0,0,0))
        self.CreateGrid(0,3)
        self.EnableEditing(False)
        self.EnableDragCell(False)
        self.EnableDragRowSize(False)
        self.EnableDragColSize(True)
        self.HideRowLabels()


        self.SetColLabelValue(0, "Identifier")
        self.SetColLabelValue(1, "Domain Name")
        self.SetColLabelValue(2, "Data Type")

    def AddDomain(self, name, type):
        self.AppendRows(1)
        self.SetCellValue(self.GetNumberRows()-1, 1, name)
        self.SetCellValue(self.GetNumberRows()-1, 2, type)

    def GetAllAttr(self):
        attrList = []
        for i in range(0, self.GetNumberRows()) :
            attrList.append(self.GetCellValue(i,1))
        print "Schema table : Get attr"
        print attrList
        return attrList

class FDTable(wx.grid.Grid) :
    def __init__(self, parent):
        wx.grid.Grid.__init__(self,parent,-1, size = (500, 130))
        self.SetColSizes(wx.grid.GridSizesInfo(103, range(0,3)))
        self.SetDefaultCellBackgroundColour(wx.Colour(0,0,0,0))
        self.CreateGrid(0,3)
        self.EnableEditing(False)
        self.EnableDragCell(False)
        self.EnableDragRowSize(False)
        self.EnableDragColSize(True)
        self.HideRowLabels()


        self.SetColLabelValue(0, "LHS")
        self.SetColLabelValue(1, "Operator")
        self.SetColLabelValue(2, "RHS")

    def AddFD(self, LHS, operator, RHS):

        LHSString = ""
        RHSString = ""
        for i in LHS :
            LHSString += i
            LHSString += ", "
        LHSString = LHSString[:len(LHSString)-2]
        for i in RHS :
            RHSString += i
            RHSString += ", "
        RHSString = RHSString[:len(RHSString)-2]

        isExist = False

        for i in range(0, self.GetNumberRows()) :
            if self.GetCellValue(i, 0) == LHSString and self.GetCellValue(i,1) == operator and self.GetCellValue(i,2) == RHSString :
                isExist = True

        if isExist == False :
            self.AppendRows(1)
            self.SetCellValue(self.GetNumberRows()-1, 0, LHSString)
            self.SetCellValue(self.GetNumberRows()-1, 1, operator)
            self.SetCellValue(self.GetNumberRows()-1, 2, RHSString)
        else :
            dlg = wx.MessageDialog(self, "Same functional dependency have already been added", "ERROR", wx.OK)
            dlg.ShowModal()


class SelectAttrTable(wx.grid.Grid) :
    def __init__(self, parent) :
        wx.grid.Grid.__init__(self, parent, -1, size = (100, 130))
        self.SetDefaultCellBackgroundColour(wx.Colour(0,0,0,0))
        self.CreateGrid(0,1)
        self.EnableEditing(False)
        self.EnableDragCell(False)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.HideRowLabels()

    def addAttr(self, attrName):
        self.AppendRows(1)
        self.SetCellValue(self.GetNumberRows(), 0, attrName)

    def GetAllAttr(self):

        return frame.schemaTable.GetAllAttr()

    def GetExistAttr(self):
        attrList = []
        for i in range(0, self.GetNumberRows()) :
            attrList.append(self.GetCellValue(i, 0))
        return attrList

    def GetRemainAttr(self):
        attrList = self.GetAllAttr()
        for i in self.GetExistAttr() :
            if i in attrList:
                attrList.remove(i)
        return attrList

app = wx.App(False)
frame = MainFrame(None, "SchemaGenerator" )

app.MainLoop()
