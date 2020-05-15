from CommandContent import MakeUI as mk
import webInterface as wi


ui = mk()
ui.setFinishedOrderCommand(wi.finishOrder)
ui.setTakeOrderCommand(wi.takeOrder)
ui.setOrderGetterCommand(wi.getCrtOrderContent)
ui.setOrderSetterCommand(wi.setCrtOrderID)
ui.setOrderListGetterCommand(wi.getCrtClientOrderList)
ui.setClientSelectGetterCommand(wi.setCrtClient)
ui.setClientListGetter(wi.getAllClients)
ui.make()

