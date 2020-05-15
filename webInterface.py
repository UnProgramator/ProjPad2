import requests as req

crtOrderID = None
crtOrderState = None
crtClientID = -1
siteUrl = 'https://padserver1.herokuapp.com'
orderStatus={0:'send', 1:'pending', 2:'done'}


#client page
def getAllClients():
    jsonresp = req.get(siteUrl+'/users').json()
    response = []
    for usr in jsonresp:
        usrName = usr['userName']
        usrID = usr['id']
        response = response + [[usrID, usrName]]
    return response

def setCrtClient(clientID):
    global crtClientID
    crtClientID = clientID

#order list page
def setCrtOrderID(orderID, status):
    global crtOrderID
    global crtOrderState
    crtOrderID = orderID
    crtOrderState = status

def getCrtClientOrderList():
    jsonresp = req.get(siteUrl+'/order/user/' + str(crtClientID)).json()
    response = []
    for order in jsonresp:
        orderID = order['oid']
        itemNr = order['nrItems']
        state = order['state']
        data = order['data']
        data,ceva = data.split('T')
        data += " " + ceva.split('.')[0]
        response = response + [[orderID, data, state, itemNr]]
    return response

#oder page
def finishOrder():
    if crtOrderState == 'done':
       raise Exception('Comanda este deja finalizata')
    resp = req.put(siteUrl+'/order/' + str(crtOrderID) + '/status/done')
    if resp.ok == False:
        raise Exception('Aaparut o eroare de comunicare cu serverul. Incercati din nou')

def takeOrder():
    if crtOrderState == 'pending':
        raise Exception('Comanda a fost preluata')
    if crtOrderState == 'done':
        raise Exception('Comanda a fost finalizata. O comanda finalizata nu mai poate fi preluata')
    resp = req.put(siteUrl+'/order/' + str(crtOrderID) + '/status/pending')
    return resp.ok

def getCrtOrderContent():
    jsonresp = req.get(siteUrl+'/order/' + str(crtOrderID) + '/product').json()
    food = []
    notFood = []
    for resp in jsonresp:
        productID = resp['pid']
        productName = resp['productName']
        productQuantity = resp['quantity']
        isFood = resp['food']
        if isFood:
            food += [[productID, productName, productQuantity]]
        else:
            notFood += [[productID, productName, productQuantity]]
    return {'food':food, 'nonfood':notFood}

