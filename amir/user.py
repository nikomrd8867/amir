import gi
from gi.repository import Gtk
from gi.repository import GObject

from sqlalchemy.orm.util import outerjoin
from sqlalchemy.orm.query import aliased
from sqlalchemy.sql.functions import *
from sqlalchemy.sql import and_
from sqlalchemy.orm import sessionmaker, join
from    dateentry       import  *
import  decimalentry

import numberentry
from utility import LN,convertToLatin
from database import *
from share import share
from helpers import get_builder
from amir.share import Share

config = share.config

class User(GObject.GObject):
    subjecttypes = ["Debtor", "Creditor", "Both"]
    
    def __init__ (self, ledgers_only=False, parent_id=[0,], multiselect=False):
        GObject.GObject.__init__(self)

        self.builder = get_builder("user")
        
        self.window = self.builder.get_object("viewUsers")
        self.window.set_modal(True)
        
        self.userTreeview = self.builder.get_object("usersTreeview")
            
        self.userTreestore = Gtk.TreeStore(int, str, str)
        column = Gtk.TreeViewColumn(_("ID"), Gtk.CellRendererText(), text=0)

        column.set_spacing(5)
        column.set_resizable(True)
        self.userTreeview.append_column(column)
        column = Gtk.TreeViewColumn(_("Name"), Gtk.CellRendererText(), text=1)

        column.set_spacing(5)
        column.set_resizable(True)
        self.userTreeview.append_column(column)
        column = Gtk.TreeViewColumn(_("Username"), Gtk.CellRendererText(), text=2)

        column.set_spacing(5)
        column.set_resizable(True)
        self.userTreeview.append_column(column)
        
        #Find top level ledgers (with parent_id equal to 0)
        result = config.db.session.query(Users.id, Users.name, Users.username).all()

        for a in result :            
            iter = self.userTreestore.append(None, (a.id, a.name, a.username))
        
        if ledgers_only == True:
            btn = self.builder.get_object("addsubtoolbutton")
            btn.hide()
        
        self.userTreeview.set_model(self.userTreestore)
        self.userTreestore.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        self.window.show_all()
        self.builder.connect_signals(self)

        if multiselect:
            self.userTreeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
            self.groupTreestore.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
            self.builder.get_object('toolbar4').hide()
            self.builder.get_object('statusbar1').hide()
        else:
            self.builder.get_object('hbox5').hide()
        self.numberOfCheckboxes = 8
        
    def addUser(self, sender):
        dialog = self.builder.get_object("dialog1")
        dialog.set_title(_("Add User"))
        hbox = self.builder.get_object("hbox3")
        hbox.hide()

        username = self.builder.get_object("username")
        username.set_text("")
        password = self.builder.get_object("password")
        password.set_text("")
        name = self.builder.get_object("name")
        name.set_text("")
        
        result = dialog.run()
        if result == 1 :             
            self.saveNewUser(unicode(name.get_text()),unicode(username.get_text()), unicode(password.get_text()), type, None, dialog)
        dialog.hide()
        
    def selectGroup(self,sender=0,edit=None):
        self.session = config.db.session    
        # self.Document = class_document.Document()
        
        query   = self.session.query(Factors.Id).select_from(Factors)
        lastId  = query.order_by(Factors.Id.desc()).first()         
        if not lastId:
            lastId  = 0
        else:
            lastId  = lastId.Id
        self.Id = lastId + 1
                
        self.window = self.builder.get_object("viewGroups")
        
        
#         ###editing
        
#         self.factorDate = DateEntry()
#         self.builder.get_object("datebox").add(self.factorDate)
#         self.factorDate.show()
        
#         self.shippedDate = DateEntry()
#         self.builder.get_object("shippedDateBox").add(self.shippedDate)
#         self.shippedDate.show()
        
        
#         #edit date
#         self.editDate = DateEntry().getDateObject()
        
#         self.additionsEntry = decimalentry.DecimalEntry()
#         self.builder.get_object("additionsbox").add(self.additionsEntry)
#         self.additionsEntry.set_alignment(0.95)
#         #self.additionsEntry.show()
#         # self.additionsEntry.connect("changed", self.valsChanged)
        
#         self.subsEntry = decimalentry.DecimalEntry()
#         self.builder.get_object("subsbox").add(self.subsEntry)
#         self.subsEntry.set_alignment(0.95)
#         #self.subsEntry.show()
#         # self.subsEntry.set_sensitive(False)
#         # self.subsEntry.connect("changed", self.valsChanged)
        
#         self.cashPymntsEntry = decimalentry.DecimalEntry()
#         self.builder.get_object("cashbox").add(self.cashPymntsEntry)
#         self.cashPymntsEntry.set_alignment(0.95)
#         #self.cashPymntsEntry.show()
#         self.cashPymntsEntry.set_text("0")
#         self.cashPymntsEntry.connect("changed", self.paymentsChanged)
        
#         self.qntyEntry = decimalentry.DecimalEntry()
#         self.builder.get_object("qntyBox").add(self.qntyEntry)
#         #self.qntyEntry.show()
#         self.qntyEntry.connect("focus-out-event", self.validateQnty)
        
#         self.unitPriceEntry = decimalentry.DecimalEntry()
#         self.builder.get_object("unitPriceBox").add(self.unitPriceEntry)
#         #self.unitPriceEntry.show()
#         self.unitPriceEntry.connect("focus-out-event", self.validatePrice)
        
#         self.customerEntry      = self.builder.get_object("customerCodeEntry")
#         self.totalEntry         = self.builder.get_object("subtotalEntry")
#         self.totalDiscsEntry    = self.builder.get_object("totalDiscsEntry")
#         self.payableAmntEntry   = self.builder.get_object("payableAmntEntry")
#         self.totalPaymentsEntry = self.builder.get_object("totalPaymentsEntry")
#         self.remainedAmountEntry= self.builder.get_object("remainedAmountEntry")
#         self.nonCashPymntsEntry = self.builder.get_object("nonCashPymntsEntry")
#         self.customerNameEntry  = self.builder.get_object("customerNameEntry")
#         self.taxEntry           = self.builder.get_object("taxEntry")
#         self.feeEntry           = self.builder.get_object("feeEntry")
        
#         self.treeview = self.builder.get_object("TreeView")
#         self.treestore = Gtk.TreeStore(int, str, str, str, str)
#         self.treestore.clear()
#         self.treeview.set_model(self.treestore)
        
                    
#         column = Gtk.TreeViewColumn(_("Id"), Gtk.CellRendererText(), text = 0)
#         column.set_spacing(5)
#         column.set_resizable(True)
#         #column.set_sort_column_id(0)
#         #column.set_sort_indicator(True)
#         self.treeview.append_column(column)
        
        
#         column = Gtk.TreeViewColumn(_("factor"), Gtk.CellRendererText(), text = 1)
#         column.set_spacing(5)
#         column.set_resizable(True)
#         column.set_sort_column_id(0)
#         column.set_sort_indicator(True)
#         self.treeview.append_column(column)
        
#         column = Gtk.TreeViewColumn(_("Date"), Gtk.CellRendererText(), text = 2)
#         column.set_spacing(5)
#         column.set_resizable(True)
# #       column.set_sort_column_id(1)
# #       column.set_sort_indicator(True)
#         self.treeview.append_column(column)     
        
#         column = Gtk.TreeViewColumn(_("Customer"), Gtk.CellRendererText(), text = 3)
#         column.set_spacing(5)
#         column.set_resizable(True)
#         self.treeview.append_column(column) 
        
#         column = Gtk.TreeViewColumn(_("Total"), Gtk.CellRendererText(), text = 4)
#         column.set_spacing(5)
#         column.set_resizable(True)
#         self.treeview.append_column(column)     

#         column = Gtk.TreeViewColumn(_("Permanent"), Gtk.CellRendererText(), text = 5)
#         column.set_spacing(5)
#         column.set_resizable(True)
#         self.treeview.append_column(column) 
        
#         self.treeview.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
#         #self.treestore.set_sort_func(0, self.sortGroupIds)
#         self.treestore.set_sort_column_id(1, Gtk.SortType.ASCENDING)
        self.builder.connect_signals(self)  
#         ###editing      
        

        self.groupTreeview = self.builder.get_object("groupsTreeView")
            
        self.groupTreestore = Gtk.TreeStore(int, str)
        column = Gtk.TreeViewColumn(_("ID"), Gtk.CellRendererText(), text=0)

        column.set_spacing(5)
        column.set_resizable(True)
        self.groupTreeview.append_column(column)
        column = Gtk.TreeViewColumn(_("Name"), Gtk.CellRendererText(), text=1)

        column.set_spacing(5)
        column.set_resizable(True)
        self.groupTreeview.append_column(column)
        
        result = config.db.session.query(Permissions.id, Permissions.name).all()
        for a in result :
            iter = self.groupTreestore.append(None, (int(a.id), str(a.name)))
        self.groupTreeview.set_model(self.groupTreestore)
        self.groupTreestore.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        self.builder.connect_signals(self)

        self.window.show_all()

    def addGroup(self, sender):
        self.window = self.builder.get_object("permission")
        self.builder.connect_signals(self)  
        self.window.show_all()

    def editUser(self, sender):
        dialog = self.builder.get_object("dialog1")
        dialog.set_title(_("Edit User"))
        selection = self.userTreeview.get_selection()
        iter = selection.get_selected()[1]
        id = convertToLatin(self.userTreestore.get(iter, 0)[0])
        name = self.userTreestore.get(iter, 1)[0]
        username = self.userTreestore.get(iter, 2)[0]
        
        if iter != None :
            entry = self.builder.get_object("name")
            entry.set_text(name)
            
            entry = self.builder.get_object("username")
            entry.set_text(username)

            result = dialog.run()
            
            if result == 1:
                userId = convertToLatin(self.userTreestore.get(iter, 0)[0])
                username = self.builder.get_object("username")
                password = self.builder.get_object("password")
                name = self.builder.get_object("name")
                self.saveEditUser(userId, unicode(name.get_text()),unicode(username.get_text()), unicode(password.get_text()), type, None, dialog)
            dialog.hide()
    
    def deleteUser(self, sender):
        selection = self.userTreeview.get_selection()
        iter = selection.get_selected()[1]
        if iter != None :
            Subject1 = aliased(Subject, name="s1")
            Subject2 = aliased(Subject, name="s2")
            
            code = convertToLatin(self.userTreestore.get(iter, 0)[0])
            row = config.db.session.query(Users).filter(Users.id == code).first()
            config.db.session.delete(row)
            config.db.session.commit()
            self.userTreestore.remove(iter)

    def deleteGroup(self, sender):
        selection = self.groupTreeview.get_selection()
        iter = selection.get_selected()[1]
        if iter != None :           
            code = convertToLatin(self.groupTreestore.get(iter, 0)[0])
            row = config.db.session.query(Permissions).filter(Permissions.id == code).first()
            config.db.session.delete(row)
            config.db.session.commit()
            self.groupTreestore.remove(iter)
    
    def saveNewUser(self, name, username, password, type, iter, widget):
        #Now create new subject:
        user = Users(name, username, password)
        config.db.session.add(user)
        
        config.db.session.commit()
        
        child = self.userTreestore.append(iter, (user.id, name, username))
        
        self.temppath = self.userTreestore.get_path(child)
        self.userTreeview.scroll_to_cell(self.temppath, None, False, 0, 0)
        self.userTreeview.set_cursor(self.temppath, None, False)

    def saveEditUser(self, userId, name, username, password, type, iter, widget):
        result = config.db.session.query(Users)
        result = result.filter(Users.id == userId)
        result[0].name = name
        result[0].username = username
        result[0].password = password
        config.db.session.commit()
        
        # self.userTreestore.set( ('Name','Username'), (name, username))
        
        # self.temppath = self.userTreestore.get_path(child)
        # self.treeview.scroll_to_cell(self.temppath, None, False, 0, 0)
        # self.treeview.set_cursor(self.temppath, None, False)
    def getPermission(self):
        permissionResult = 0;
        for x in range(1, self.numberOfCheckboxes + 1):
            if self.builder.get_object("checkbutton" + str(x)).get_active() == True:
                permissionResult += 2**x
        return permissionResult

    def setPermission(self, id):
        result = config.db.session.query(Permissions)
        result = result.filter(Permissions.id == id)
        permissionResult = int(result[0].value)
        for x in range(self.numberOfCheckboxes, 0, -1):
            if  permissionResult >= 2**x:
                self.builder.get_object("checkbutton" + str(x)).set_active(True)
                permissionResult = permissionResult - 2**x
    def submitNewPermission(self, sender):
        permissionResult = self.getPermission();
        name = self.builder.get_object("nameEntry")
        permission = Permissions(unicode(name.get_text()), str(permissionResult))
        config.db.session.add(permission)
        
        config.db.session.commit()

        child = self.groupTreestore.append(None, (int(permission.id), str(permission.name)))
        
        self.temppath = self.userTreestore.get_path(child)
        self.builder.get_object("permission").hide()
        # self.groupTreeview.scroll_to_cell(self.temppath, None, False, 0, 0)
        # self.groupTreeview.set_cursor(self.temppath, None, False)

    def editGroup(self, sender):
        dialog = self.builder.get_object("permission")
        dialog.set_title(_("Edit Permission"))
        selection = self.groupTreeview.get_selection()
        iter = selection.get_selected()[1]
        id = convertToLatin(self.groupTreestore.get(iter, 0)[0])
        name = self.groupTreestore.get(iter, 1)[0]
        self.setPermission(id)
        self.window = self.builder.get_object("permission")
        self.builder.connect_signals(self)  
        entry = self.builder.get_object("nameEntry")
        entry.set_text(name)
        self.window.show_all()
        # if iter != None :

        #     result = dialog.run()
            
        #     if result == 1:
        #         groupId = convertToLatin(self.userTreestore.get(iter, 0)[0])
        #         name = self.builder.get_object("nameEntry")
        #         permission = self.getPermission()
        #         #self.saveEditUser(userId, unicode(name.get_text()),unicode(username.get_text()), unicode(password.get_text()), type, None, dialog)
        #     dialog.hide()

    def match_func(self, iter, data):
        (column, key) = data   # data is a tuple containing column number, key
        value = self.treestore.get_value(iter, column)
        if value < key:
            return -1
        elif value == key:
            return 0
        else:
            return 1

    def highlightSubject(self, code):
        i = 2
        code = code.decode('utf-8')
        part = code[0:i]
        iter = self.treestore.get_iter_first()
        parent = iter
        
        while iter:
            res = self.match_func(iter, (0, part))
            if res < 0:
                iter = self.treestore.iter_next(iter)
            elif res == 0:
                if len(code) > i:
                    parent = iter
                    iter = self.treestore.iter_children(parent)
                    if iter:
                        if self.treestore.get_value(iter, 0) == "":
                            self.populateChildren(self.treeview, parent, None)
                            iter = self.treestore.iter_children(parent)
                        i += 2
                        part = code[0:i]
                else:
                    break
            else:
                break

        if not iter:
            iter = parent
            
        if iter:
            path = self.treestore.get_path(iter)
            self.treeview.expand_to_path(path)
            self.treeview.scroll_to_cell(path, None, False, 0, 0)
            self.treeview.set_cursor(path, None, False)
            self.treeview.grab_focus()
     
    def on_key_release_event(self, sender, event):
        expand = 0
        selection = self.treeview.get_selection()
        if selection.get_mode() == Gtk.SelectionMode.MULTIPLE:
            return

        iter = selection.get_selected()[1]
        if iter != None :
            if Gdk.keyval_name(event.keyval) == "Left":
                if self.treeview.get_direction() != Gtk.TextDirection.LTR:
                    expand = 1
                else:
                    expand = -1
                    
            if Gdk.keyval_name(event.keyval) == "Right":
                if self.treeview.get_direction() != Gtk.TextDirection.RTL:
                    expand = 1
                else:
                    expand = -1
             
            if expand == 1:
                if self.treestore.iter_has_child(iter):
                    path = self.treestore.get_path(iter)
                    self.treeview.expand_row(path, False)
                    return
            elif expand == -1:
                path = self.treestore.get_path(iter)
                if self.treeview.row_expanded(path):
                    self.treeview.collapse_row(path)
                else: 
                    parent = self.treestore.iter_parent(iter)
                    if parent != None:
                        path = self.treestore.get_path(parent)
                        self.treeview.collapse_row(path)
                        self.treeview.set_cursor(path, None, False)
                        self.treeview.grab_focus()
                return
#            if Gdk.keyval_name(event.keyval) == Ri:
            
    def selectGroupFromList(self, treeview, path, view_column):
        selection = self.groupTreeview.get_selection()
        if selection.get_mode() == Gtk.SelectionMode.MULTIPLE:
            return

        iter = self.treestore.get_iter(path)
        code = convertToLatin(self.treestore.get(iter, 0)[0])
        name = self.treestore.get(iter, 1)[0]
        
        query = config.db.session.query(Subject).select_from(Subject)
        query = query.filter(Subject.code == code)
        sub_id = query.first().id
        self.emit("subject-selected", sub_id, code, name)

    def dbChanged(self, sender, active_dbpath):
        self.window.destroy()

    def on_select_clicked(self, button):
        selection = self.treeview.get_selection()
        items = []
        model, pathes = selection.get_selected_rows()
        for path in pathes:
            iter = self.treestore.get_iter(path)
            code = convertToLatin(self.treestore.get(iter, 0)[0])
            name = self.treestore.get(iter, 1)[0]

            query = config.db.session.query(Subject).select_from(Subject)
            query = query.filter(Subject.code == code)
            sub_id = query.first().id
            items.append((sub_id, code, name))
        self.emit("subject-multi-selected", items)

GObject.type_register(User)
GObject.signal_new("subject-selected", User, GObject.SignalFlags.RUN_LAST,
                   None, (GObject.TYPE_INT, GObject.TYPE_STRING, GObject.TYPE_STRING))
GObject.signal_new("subject-multi-selected", User, GObject.SignalFlags.RUN_LAST,
                   None, (GObject.TYPE_PYOBJECT,))
   
