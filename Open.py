from xml.etree.ElementTree import XML
import time
import requests
import datetime
from bs4 import BeautifulSoup
from decimal import Decimal
import pandas as pd
import MetaTrader5 as mt5

###AJUSTE 


#config pandas
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
while(True):
    
    #traz o html
    html_text = requests.get('https://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-ajustes-do-pregao-ptBR.asp').text
    soup =BeautifulSoup (html_text, 'lxml')
    #Filtra dados
    tabela_bruta=soup.find('table')
    #traz tabela desejada
    df= pd.read_html(str(tabela_bruta))[0].head(400)

    #Lógia do contrato atual 
    hoje=datetime.datetime.now()
    mes= hoje.month
    ano=hoje.year-2000

    if mes==1:
        vencimento="G"

    if mes==2:
        vencimento="H"

    if mes ==3:
        vencimento='J'
        
    if mes==4:
        vencimento="K"

    if mes==5:
        vencimento="M"

    if mes ==6:
        vencimento='N'

    if mes==7:
        vencimento="Q"

    if mes==8:
        vencimento="U"

    if mes ==9:
        vencimento='V'

    if mes ==10:
        vencimento='X'

    if mes==11:
        vencimento="Z"

    if mes==12:
        vencimento="F"

    contrato=(vencimento + str(ano) )
    #print(contrato)
    #print(df)
    dol1=df.loc[df["Mercadoria"]=="DOL - Dólar comercial"]
    #print(dol1)
    
    #identificador de qual linha esta o ajuste.
    indice_ajuste_atual  =  dol1.index[0]
    

    
    
    #agora vamos verificar se o contarto do primeiro esta certo
    dol2=dol1.reset_index()
    #condição de vencimento estar correto.
    if dol2["Vencimento"][0] != contrato:
        indice_ajuste_atual=indice_ajuste_atual+1
        
    
    
    ajuste=df.loc[indice_ajuste_atual][3]
    
    


    
    
    


  
    
    ajuste_replace=ajuste.replace(',','')

    ajuste=float(ajuste_replace)
    #print(ajuste)






    #Obter contrato DI atual 
    hoje=datetime.datetime.now()
    mes= hoje.month
    ano=hoje.year-2000

    if mes==1:
        vencimento="G"

    if mes==2:
        vencimento="H"

    if mes ==3:
        vencimento='J'
        
    if mes==4:
        vencimento="K"

    if mes==5:
        vencimento="M"

    if mes ==6:
        vencimento='N'

    if mes==7:
        vencimento="Q"

    if mes==8:
        vencimento="U"

    if mes ==9:
        vencimento='V'

    if mes ==10:
        vencimento='X'

    if mes==11:
        vencimento="Z"

    if mes==12:
        vencimento="F"

    contrato=(vencimento + str(ano) )
    contrato="DI1"+str(contrato)

    mt5.initialize()
    # tentamos ativar a exibição do símbolo EURCAD no MarketWatch
    selected=mt5.symbol_select(contrato,True)
    if not selected:
        print("Erro ao adicionar ativo na OBS. de mercado=",mt5.last_error())
    else:
        stts_mt5='OK'
   
    mt5.shutdown()

    #print(contrato)#########

    #Obter cotação DI
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    ultimo=mt5.symbol_info_tick(contrato).last 

    #print(ultimo)########


    #obter dias uteis do ano atual 
    dias_uteis_2022=252


    #dias para vencimento do contrato (obter na b3)

    import datetime
    from datetime import date
    hoje=datetime.datetime.now()
    dia=hoje.day
    mes=hoje.month
    ano=hoje.year

    vec_ano=ano
    vec_dia=1
    vec_mes=mes+1
    if vec_mes>12:
        vec_mes=1
        vec_ano=vec_ano+1

    primeiro_outro_mes=vec_ano,vec_mes,vec_dia



    
    def numOfDays(date1, date2):
        return (date2-date1).days
        
    date1 = date(ano,mes,dia)
    date2 = date(vec_ano,vec_mes,vec_dia)
    dias_para_vencer=numOfDays(date1, date2)

    #print ('dias para vencer:',dias_para_vencer)####






    Over = ((1+ultimo)**(1/dias_uteis_2022)-1)* dias_para_vencer

    #print ('over: ',(f'{Over:.4f}'))##########




    #####################################
    #dolar comercial BC

    html_text = requests.get('https://valor.globo.com/valor-data/').text
    soup =BeautifulSoup (html_text, 'lxml')
    dolar_comercial=soup.find('div',class_="cell auto data-cotacao__ticker_quote").text
    dolar_comercial=(dolar_comercial.replace(',','.'))
    dolar=dolar_comercial




    #Justo=Justo=Dolar comercial +(Dolar comercial * over%)
    var= Decimal(Over) /100
    var2 = Decimal(dolar) * Decimal(var)
    Justo= (Decimal(var2)+Decimal(dolar))
    Justo=(f'{Justo:.4f}')
    #print(Justo)



    #Traz dados de maxima e minima de acortdo com o preço que o dólar trabalhou na madrugada.



    html_text = requests.get('https://br.investing.com/currencies/brl-usd-historical-data').text
    soup =BeautifulSoup (html_text, 'lxml')
    soup= soup.find('div',class_="trading-hours_value__2MrOn",)
    data= soup.find_next('div',class_="trading-hours_value__2MrOn")
    data= data.find_next('div',class_="trading-hours_value__2MrOn").text


    a=data[:7]
    b= data [9:]

    mylist=[a,b]

    maxima=max(mylist,)
    minima=min(mylist,)

    maxima=maxima.replace(',','.')
    minima=minima.replace(',','.')


    maxima=1/Decimal(maxima)
    minima=1/Decimal(minima)

    maxima=(f'{maxima:.4f}')
    minima=(f'{minima:.4f}')

    #print ('MAx, minima',maxima,',',minima)




    pontos_padrao=[Justo,maxima,minima,ajuste]

    #print(pontos_padrao)

    #Pontos FIBO
    #Calculo Fibonacci
    def fibonacci (maxima,minima):



        if maxima<minima:
            maxima,minima=minima,maxima

            
        

        #Dados

        fibo=38.2  #VALOR A SER DESCOBERTO %
        parceio=  maxima-minima
        
        
        #calculo

        cal1=     fibo  /  100
        cal2=     cal1 * parceio

        #Resultado
        fibo_1=cal2+minima
        


        #61.8%
        fibo=61.8  #VALOR A SER DESCOBERTO %
        #CALCULO

        parceio=maxima-minima
        cal1=  fibo  /  100
        cal2= cal1 * parceio

        fibo_2=cal2+minima
        pontos=[fibo_1,fibo_2]
        #torna a variavel multavel pela função
        global pontos_padrao 
        pontos_padrao=pontos_padrao+pontos

        


        


    #fibo_min_max
    fibonacci(float(pontos_padrao[1]),float(pontos_padrao[2]))
    #print (pontos_padrao)



    #fibo_justo_max
    fibonacci(float(pontos_padrao[0]),float(pontos_padrao[1]))
    #print (pontos_padrao)


    #fibo_ajuste_min
    fibonacci(float(pontos_padrao[0]),float(pontos_padrao[2]))
    #print (pontos_padrao)




    ####Sucesso

    print (pontos_padrao[0:])
    time.sleep(180)
