import mimetypes

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .server import server
from django.http import HttpResponse,JsonResponse
import time
import pandas as pd
from django.db import connection
import json
import csv
import plotly.graph_objs as go

def fetch_data(q):
    with connection.cursor() as cursor:
        cursor.execute(q)
        result = pd.read_sql(
        sql=q,
        con=connection
        )
        cursor = connection.cursor();

    return result

def test(request, value):
    return HttpResponse('sdfghjkl')

################################    GRAPH   ##########################3
@csrf_exempt
def draw_season_points_graph(request,methods=['POST']):
    print("result for updation is : ")
    #print(results['opponent'])
    print(request.POST)
    data = json.loads(request.body)
    print('#######################request.body')

    print()
    print (data["xdata"])
    print (data["ydata"])
    print (data["graph"])

    #print((request.POST['results']))
    #print(json.dumps(results))
    xdata =(data["xdata"])
    ydata = (data["ydata"])
    graph =(data["graph"])
    if  graph=="bar-chart":
        #print(dates)
        print(graph)
        figure = go.Figure(
        data=[
            go.Bar(x=xdata, y=ydata)
        ],
        layout=go.Layout(
            title='Points Accumulation',
            showlegend=True
            )
        )
    else:
         figure = go.Figure(
        data=[
            go.Scatter(x=xdata, y=ydata, mode='lines+markers')
        ],
        layout=go.Layout(
            title='Points Accumulation',
            showlegend=False
        )
    )



    return JsonResponse(figure,safe=False)


def login_get_data(request,user_id):
    print("in login_get_data api")
    respData=''
    if request.method=='GET':
        query = ( f''' SELECT DISTINCT * FROM viz_testuser WHERE Userid='{user_id}' ''' )
        #query = ( f''' SELECT DISTINCT GrpTab FROM UserGroup WHERE UserDomain=(SELECT DISTINCT UserDomain FROM viz_testuser WHERE Userid='{user_id}') ''' )
        userlist = pd.DataFrame(fetch_data(query))
        print('########################userlist is')
        print(userlist)


        if  not(userlist.empty) :
            respData = {"pwd":""}
            respData['pwd'] = (userlist.get_value(0,"Password"))
            userDomain =(userlist.get_value(0,"UserDomain"))
            respData['domainTabs'] = userDomain
            #print(respData['domainTabs'])
            #tableData = getTableData(respData['domainTabs'])
            #if  not(usrGrp.empty) :
             #   for item in usrGrp:
              #      query=( f''' SELECT DISTINCT * FROM '{item}' ''')
               #     #print(query)
                #    tabData  = pd.DataFrame(fetch_data(query))
                 #   print(tabData)
                  #  respData['tabData'].append(tabData)

    else:
        return HttpResponse('get worked')
    #print(respData)
    return JsonResponse(respData)


def getDomainData(request,domain):
    print("in domainData api")

    if request.method=='GET':
        print("starting delay")
        #time.sleep(5)
        print("ending delay")
        respData = {"domainTabs":""}
        #query = ( f''' SELECT DISTINCT * FROM viz_testuser WHERE Userid='{user_id}' ''' )
        query = ( f''' SELECT DISTINCT GrpTab FROM UserGroup WHERE UserDomain='{domain}' ''' )
        #query = (f'''  ''')
        #query = (f'''SELECT *  FROM soccer-stats.INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE''')
        userlist = pd.DataFrame(fetch_data(query))
        print('########################userlist is')
        print(userlist)

        if  not(userlist.empty) :
            #respData['pwd'] = "superpwd1" #(userlist.get_value(0,"Password"))
            domainTabs =(userlist.get_value(0,"GrpTab"))
            respData['domainTabs'] = domainTabs
            print(respData['domainTabs'])
            #tableData = getTableData(respData['domainTabs'])
            #if  not(usrGrp.empty) :
             #   for item in usrGrp:
              #      query=( f''' SELECT DISTINCT * FROM '{item}' ''')
               #     #print(query)
                #    tabData  = pd.DataFrame(fetch_data(query))
                 #   print(tabData)
                  #  respData['tabData'].append(tabData)

    else:
        return HttpResponse('get worked')
    print(respData)
    return JsonResponse(respData)



def getTabData(request,tables):
    #print("in tabData api")
    if request.method=='GET':
        respData = {}

        respData['dtyp'] =None
        #print(request)
        #print(tables)
            #tableData = getTableData(respData['domainTabs'])
        if (tables) :
            tables = tables.split("-")
            for item in tables:

              query=( f''' SELECT DISTINCT * FROM '{item}' ''')
              query2 = (f'''PRAGMA table_info('{item}') ''')
              #df=pd.DataFrame(fetch_data(query))
              types =pd.DataFrame(fetch_data(query2))
              print('###################datatypes are theseeeee')
              #print(dtyp)
              tabData  = (pd.DataFrame(fetch_data(query))).to_json()
              #dtyp = (dtyp).to_json()
              #print(dtyp)
              respData[item]=(tabData)
              print(types)
              respData[item+"type"]=types.to_json()
              #print(respData['dtyp'])
              print('##########response to  be sent')
              #print(respData)


              #break

    else:
        return HttpResponse('get worked')
    #respData =list(respData.values())
    #respData = json.dumps(respData)
    #print(respData)
    #respData.dropna(inplace = True)
    #data_dict = respData.to_dict('series')
    #respData["status_code"]=200
    #return JsonResponse(respData)
    #return HttpResponse((respData), content_type="application/json")
    return JsonResponse((respData))



#@login_required(redirect_field_name='/viz/dash',login_url="/viz/login")
def dispatcher(request):
    '''
    Main function
    @param request: Request object
    '''
    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.content_type
    }
    with server.test_request_context(request.path, **params):
        server.preprocess_request()

        try:
            print('#####################################inside viz.views.try block')
            print(server.full_dispatch_request())                           #<Response 1069 bytes [200 OK]>
            response = server.full_dispatch_request()
        except Exception as e:
            response = server.make_response(server.handle_exception(e))

        response.direct_passthrough = False
        print('#######################################data from response')
        print(response.get_data)                        #<bound method BaseResponse.get_data of <Response 1069 bytes [200 OK]>>
        return response.get_data()


@csrf_exempt
def dash_json(request, **kwargs):
    """Handle Dash JSON API requests"""
    print('###################after processing /viz/_dash- the requested  url is: ')
    print(request.get_full_path())
    return HttpResponse(dispatcher(request), content_type='application/json')


def dash_index(request, **kwargs):
    """Handle Dash CSS requests"""
    print('##################after processing /viz/')
    return HttpResponse(dispatcher(request), content_type='text/html')


def dash_guess_mimetype(request, **kwargs):
    """Handle Dash requests and guess the mimetype. Needed for static files."""
    url = request.get_full_path().split('?')[0]
    print('#######################aftre processing /viz/assests/ link, url is:')
    print(url)
    content_type, _encoding = mimetypes.guess_type(url)
    return HttpResponse(dispatcher(request), content_type=content_type)