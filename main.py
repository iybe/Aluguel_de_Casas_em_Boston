#--------------------------------------------------------------------
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import metrics
#--------------------------------------------------------------------
from bottle import route, run, request, template, static_file

#--------------------------------------------------------------------
df = pd.read_csv('housingOK.csv')
X = df[["CRIM","RM","DIS","RAD","TAX","PTRATIO","B","LSTAT"]]
y = df["MEDV"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)
lm = linear_model.Ridge(alpha=7)
lm.fit(X_train,y_train)
#--------------------------------------------------------------------

#--------------------------------------------------------------------
def predicao(arr):
    return lm.predict(arr)
#--------------------------------------------------------------------

@route('/')
def pagForm():
    return '''
        <form action='/' method="post">
            CRIM: <input name="crim" type="text" />           
            ZN: <input name="zn" type="text" />             
            INDUS: <input name="indus" type="text" />          
            CHAS: <input name="chas" type="text" />           
            NOX: <input name="nox" type="text" />            
            RM: <input name="rm" type="text" />             
            AGE: <input name="age" type="text" />            
            DIS: <input name="dis" type="text" />            
            RAD: <input name="rad" type="text" />            
            TAX: <input name="tax" type="text" />            
            PTRATIO: <input name="ptradio" type="text" />        
            B: <input name="b" type="text" />
            LSTAT: <input name="lstat" type="text" />
            MEDV: <input name="medv" type="text" />
            <input value="Enviar" type="submit" />  
        </form>
        <img src="grafico.png">
        <h3>(ols)Ordinary Least Squares: RMSE: 4.3334988230071465</h3>
        <h3>Ridge Regression: RMSE: 4.328965508567024</h3>
        <h3>Lasso: RMSE: 4.329449566841697</h3>
        <h3>Bayesian Ridge Regression: RMSE: 4.330414035003646</h3>
        <h1>O algoritmo utilizado e Ridge Regression</h1>
    '''

@route('/', method="POST")
def form():
    #"CRIM","RM","DIS","RAD","TAX","PTRATIO","B","LSTAT"
    parametrosModelo = [[]]
    parametrosModelo[0].append(float(request.forms.get('crim')))
    parametrosModelo[0].append(float(request.forms.get('rm')))
    parametrosModelo[0].append(float(request.forms.get('dis')))
    parametrosModelo[0].append(float(request.forms.get('rad')))
    parametrosModelo[0].append(float(request.forms.get('tax')))
    parametrosModelo[0].append(float(request.forms.get('ptradio')))
    parametrosModelo[0].append(float(request.forms.get('b')))
    parametrosModelo[0].append(float(request.forms.get('lstat')))

    resp = predicao(parametrosModelo)

    return template("MEDV: {{v}}", v = resp[0])

@route('/grafico.png')
def imagem():
    return static_file('grafico.png', root='.')

run(host='localhost', port=8080, debug=True)