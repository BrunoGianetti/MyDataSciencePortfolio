#!/usr/bin/env python
# coding: utf-8

# ![Fixed%20Bruno%20Data%20Scientist%20LinkedIn%20Banner.png](attachment:Fixed%20Bruno%20Data%20Scientist%20LinkedIn%20Banner.png)

# ---
# # BACKTESTING USING BT LIBRARY WITH PYTHON
# ---

# ## Instalando e importando bibliotecas

# In[128]:


get_ipython().system('pip install bt')


# In[129]:


get_ipython().system('pip install yfinance')


# In[130]:


import bt
import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.style.use('seaborn-darkgrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Acessando a base de dados do Banco Central

# In[131]:


def consulta_bc(codigo_bcb):
    url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
    df = pd.read_json(url)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df.set_index('data', inplace=True)
    return df


# ## Calculando o CDI acumulado

# In[132]:


def cdi_acumulado(data_inicio, data_fim):
    cdi = consulta_bc(12)
    cdi_acumulado = (1 + cdi[data_inicio : data_fim] / 100).cumprod()
    cdi_acumulado.iloc[0] = 1
    return cdi_acumulado


# ## Obtendo e Tratando os dados

# In[133]:


data_inicio = '2018-01-02'
data_fim = '2023-01-28'


# In[134]:


cdi = cdi_acumulado(data_inicio, data_fim)
cdi.index[0]


# In[135]:


tickers_carteira = ['BOVA11.SA', 'SMAL11.SA']


# In[136]:


carteira = yf.download(tickers_carteira, start=data_inicio, end=data_fim, ignore_tz = True)['Adj Close']


# In[137]:


carteira['renda_fixa'] = cdi
carteira.dropna(inplace=True)


# In[138]:


carteira


# ## Backtesting

# In[139]:


rebalanceamento = bt.Strategy('rebalanceamento', [
    bt.algos.RunMonthly(run_on_end_of_period=True),
    bt.algos.SelectAll(),
    bt.algos.WeighEqually(),
    bt.algos.Rebalance()
])


# In[140]:


buy_hold = bt.Strategy('Buy&Hold',[
    bt.algos.RunOnce(),
    bt.algos.SelectAll(),
    bt.algos.WeighEqually(),
    bt.algos.Rebalance()
])


# In[141]:


bt1 = bt.Backtest(rebalanceamento, carteira)
bt2 = bt.Backtest(buy_hold, carteira[['BOVA11.SA', 'SMAL11.SA']])


# In[142]:


resultados = bt.run(bt1, bt2)


# ## Resultados

# In[143]:


resultados.display()


# In[144]:


resultados.plot()


# ## Operações

# In[145]:


resultados.get_transactions()


# ## Pesos

# In[146]:


resultados.get_security_weights()


# In[147]:


resultados.plot_security_weights()


# In[ ]:




