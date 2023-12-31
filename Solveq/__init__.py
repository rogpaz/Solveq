'''
#Como usar:
from Solveq import *
exemplo1()
'''
nums='1234567890.'
ops='+-*/'
def ehop(val): #verifica se 'val' é operando
  return val=='+' or val=='-' or val=='*' or val=='/'
def ehnum(val): #verifica se 'val' é número
  return (type(val)==int or type(val)==float)
def ehvar(val): #verifica se 'val' é incógnita
  if val==None:
    return False
  return (ehnum(val)==False) and (val not in ops) and (val not in '()')
def temvar(eq): #verifica se tem incógnita em eq
  for i in eq:
    if ehvar(i):
      return True
  return False
def indice(val,lista):
  cnt=0
  while cnt<len(lista):
    if val==lista[cnt]:
      return cnt
    cnt=cnt+1
def disp_eq(eq):
  ret=''
  for i in eq:
    ret=ret+str(i)
  return ret
def isola0(eq):
  vret=''
  for i in eq:
    if i!='=':
      vret=vret+i
    else:
      vret=vret+'-1*('
  return vret+')'
def par_inc(eq,lista):
  vret=[]
  for i in eq:
    if i in lista:
      vret.append('(')
      vret.append('0')
      vret.append('+')
      vret.append(i)
      vret.append(')')
    else:
      vret.append(i)
  return vret
def separa_termos(eq):
  vret=[]
  cnt1=0
  lneq=len(eq)
  while cnt1<lneq:
    if eq[cnt1] in nums:
      ini=cnt1
      cnt2=cnt1+1
      if cnt2>=lneq:
        vret.append(float(eq[cnt1:]))
        return vret
      while eq[cnt2] in nums:
        cnt2=cnt2+1
        if cnt2>=lneq:
          vret.append(float(eq[cnt1:]))
          return vret
      vret.append(float(eq[cnt1:cnt2]))
      cnt1=cnt2-1
    elif eq[cnt1]=='(':
      vret.append('(')
      vret.append(0)
      vret.append('+')
    elif eq[cnt1]==')':
      vret.append('+')
      vret.append(0)
      vret.append(')')
    else:
      vret.append(eq[cnt1])
    cnt1=cnt1+1
  return vret
def tiranone(eq):
  vret=[]
  for i in eq:
    if i!=None:
      vret.append(i)
  return vret
def par_antes(eq,pos):
  #pos é o índice do primeiro parentesis
  par=1
  while par!=0:
    pos=pos-1
    if eq[pos]==')':
      par=par+1
    elif eq[pos]=='(':
      par=par-1
  return pos
def par_depois(eq,pos):
  #pos é o índice do primeiro parentesis
  par=1
  pos=pos+1
  while par!=0:
    if eq[pos]==')':
      par=par-1
    elif eq[pos]=='(':
      par=par+1
    pos=pos+1
  return pos
def par_par(eq):
  vret=[]
  cnt=0
  lneq=len(eq)
  while cnt<lneq:
    if eq[cnt]=='*':
      if eq[cnt-1]==')' and eq[cnt+1]=='(':
        p_dep=par_depois(eq,cnt+1)
        p_ant=par_antes(eq,cnt-1)+1
        ss1=eq[cnt+2:p_dep-1]
        ss2=eq[p_ant:cnt-1]
        erro1=temvar(ss1)
        erro2=temvar(ss2)
        if erro1 and erro2:
          return 'erro: sistema não linear'
        if not erro2:
          eq[p_ant-1]=simplifica(ss2)
          cnt2=p_ant
          while cnt2<=cnt-1:
            eq[cnt2]=None
            cnt2=cnt2+1
        if not erro1:
          eq[cnt+1]=simplifica(ss1)
          cnt2=cnt+2
          while cnt2<=p_dep-1:
            eq[cnt2]=None
            cnt2=cnt2+1
      elif ehvar(eq[cnt-1]) and eq[cnt+1]=='(':
        p_dep=par_depois(eq,cnt+1)
        ss1=eq[cnt+2:p_dep-1]
        #print(ss1)
        if temvar(ss1):
          return 'erro: sistema não linear'
        eq[cnt+1]=simplifica(ss1)
        cnt2=cnt+2
        while cnt2<=p_dep-1:
          eq[cnt2]=None
          cnt2=cnt2+1
      elif ehvar(eq[cnt+1]) and eq[cnt-1]==')':
        p_ant=par_antes(eq,cnt-1)+1
        ss2=eq[p_ant:cnt-1]
        #print(ss2)
        if temvar(ss2):
          return 'erro: sistema não linear'
        eq[p_ant-1]=simplifica(ss2)
        cnt2=p_ant
        while cnt2<=cnt-1:
          eq[cnt2]=None
          cnt2=cnt2+1
      elif ehvar(eq[cnt+1]) and ehvar(eq[cnt-1]):
          return 'erro: sistema não linear'
    cnt=cnt+1
  return tiranone(eq)
def simplifica(eq):
  vret=[]
  cnt=0
  lneq=len(eq)
  while cnt<lneq:
    if eq[cnt]=='(':
      fim_par=par_depois(eq,cnt+1)
      simp=simplifica(eq[cnt+1:fim_par-1])
      eq=eq[:cnt]+[simp]+eq[fim_par:]
      cnt=-1
      lneq=len(eq)
    cnt=cnt+1
  cnt=0
  while cnt<lneq:
    if eq[cnt]=='*':
      eq[cnt-1]=eq[cnt-1]*eq[cnt+1]
      eq[cnt]=None
      eq[cnt+1]=None
      eq=tiranone(eq)
      cnt=-1
      lneq=len(eq)
    elif eq[cnt]=='/':
      eq[cnt-1]=eq[cnt-1]/eq[cnt+1]
      eq[cnt]=None
      eq[cnt+1]=None
      eq=tiranone(eq)
      cnt=-1
      lneq=len(eq)
    cnt=cnt+1
  cnt=0
  while cnt<lneq:
    if eq[cnt]=='+':
      eq[cnt-1]=eq[cnt-1]+eq[cnt+1]
      eq[cnt]=None
      eq[cnt+1]=None
      eq=tiranone(eq)
      cnt=-1
      lneq=len(eq)
    elif eq[cnt]=='-':
      eq[cnt-1]=eq[cnt-1]-eq[cnt+1]
      eq[cnt]=None
      eq[cnt+1]=None
      eq=tiranone(eq)
      cnt=-1
      lneq=len(eq)
    cnt=cnt+1
  return eq[0]
def corrigepar(eq):
  vret=[]
  cnt1=0
  lneq=len(eq)
  while cnt1<lneq:
    if eq[cnt1]=='(' or ehvar(eq[cnt1]):
      if cnt1==0:
        eq=[1.0,'*']+eq
        return corrigepar(eq)
      if eq[cnt1-1]=='+' or eq[cnt1-1]=='-':
        eq=eq[:cnt1]+[1.0,'*']+eq[cnt1:]
        lneq=len(eq)
    cnt1=cnt1+1
  return eq
def corrigemenos(eq):
  vret=[]
  cnt1=0
  lneq=len(eq)
  while cnt1<lneq:
    if eq[cnt1]=='-':
      eq[cnt1]='+'
      eq[cnt1+1]=-eq[cnt1+1]
    cnt1=cnt1+1
  return eq
def corrigemaismenos(eq):
  vret=[]
  cnt1=0
  while cnt1<len(eq):
    if eq[cnt1]=='+':
      if eq[cnt1+1]=='-':
          eq=eq[:cnt1]+['-']+eq[cnt1+2:]
          cnt1=-1
    cnt1=cnt1+1
  return eq
def reduz1(eq):
  vret=[]
  cnt1=0
  ant=0
  lneq=len(eq)
  while cnt1<lneq:
    if eq[cnt1]=='(':
      fim=par_depois(eq,cnt1)
      if temvar(eq[cnt1+1:fim-1])==False:
        eq=eq[:cnt1]+[simplifica(eq[cnt1+1:fim-1])]+eq[fim:]
        lneq=len(eq)
    cnt1=cnt1+1
  return eq

def reduz2(eq):
  #print(eq)
  vret=[]
  cnt1=0
  ant=0
  lneq=len(eq)
  while cnt1<lneq:
    if eq[cnt1]=='+' or eq[cnt1]=='-':
      if len(eq[ant:cnt1])!=0:
        #print(eq[ant:cnt1])
        ss=simplifica(eq[ant:cnt1])
        eq=eq[:ant]+[ss]+([None]*(len(eq[ant:cnt1])-1))+eq[cnt1:]
      ant=cnt1+1
    elif eq[cnt1]=='(':
      if len(eq[ant:cnt1-1])!=0:
        #print(eq[ant:cnt1-1])
        ss=simplifica(eq[ant:cnt1-1])
        eq=eq[:ant]+[ss]+([None]*(len(eq[ant:cnt1-1])-1))+eq[cnt1-1:]
      ant=cnt1+1
    elif ehvar(eq[cnt1]) or eq[cnt1]==')':
      if len(eq[ant:cnt1-1])!=0:
        #print(eq[ant:cnt1-1])
        ss=simplifica(eq[ant:cnt1-1])
        eq=eq[:ant]+[ss]+([None]*(len(eq[ant:cnt1-1])-1))+eq[cnt1-1:]
      ant=cnt1+2
    cnt1=cnt1+1
  return tiranone(eq)

def multiplica_rl_par(eq):
  vret=[]
  cnt1=0
  lneq=len(eq)
  while cnt1<lneq:
    if eq[cnt1]=='*':
      if eq[cnt1+1]=='(': #Neste caso é ...*(...)
        fim=par_depois(eq,cnt1+1)
        if eq[fim]=='*': #Neste caso é (...)*...
          eq[cnt1-1]=eq[cnt1-1]*eq[fim+1]
          eq[fim]=None
          eq[fim+1]=None
    cnt1=cnt1+1
  return tiranone(eq)
def multiplica_rl_inc(eq):
  vret=[]
  cnt1=0
  lneq=len(eq)
  while cnt1<lneq:
    if eq[cnt1]=='*' and ehvar(eq[cnt1+1]): #Neste caso é ...*x*...
      if cnt1+2>=lneq:
        return tiranone(eq)
      if eq[cnt1+2]=='*':
        eq[cnt1-1]=eq[cnt1-1]*eq[cnt1+3]
        eq[cnt1+2]=None
        eq[cnt1+3]=None
    cnt1=cnt1+1
  return tiranone(eq)
def distribui(eq):
  vret=[]
  cnt=0
  lneq=len(eq)
  while cnt<lneq:
    if eq[cnt]=='*':
      if eq[cnt+1]=='(':
        mult=eq[cnt-1]
        eq[cnt-1]=None
        eq[cnt]=None
        eq[cnt+1]=None
        cnt=cnt+2
        while eq[cnt]!=')':
          if ehnum(eq[cnt]):
            eq[cnt]=eq[cnt]*mult
          if eq[cnt]=='(':
            cnt=par_depois(eq,cnt)-1
          cnt=cnt+1
        eq[cnt]=None
    cnt=cnt+1
  return tiranone(eq)
def retira1(eq):
  vret=[]
  cnt=0
  lneq=len(eq)
  while cnt<lneq:
    if eq[cnt]=='*' and eq[cnt-1]==1 and eq[cnt+1]=='(':
      p_depois=par_depois(eq,cnt+1)-1
      eq[cnt-1]=None
      eq[cnt]=None
      eq[cnt+1]=None
      eq[p_depois]=None
    cnt=cnt+1
  return tiranone(eq)
def isola_independentes(eq):
  cnt=0
  lneq=len(eq)
  while cnt<lneq:
    if eq[cnt]=='*':
      eq.append('+')
      eq.append(eq[cnt-1])
      eq.append(eq[cnt])
      eq.append(eq[cnt+1])
      eq[cnt-1]=None
      eq[cnt]=None
      eq[cnt+1]=None
    cnt=cnt+1
  cnt=0
  eq=tiranone(eq)
  lneq=len(eq)
  #print(eq)
  while cnt<lneq:
    if eq[cnt]=='+':
      tmp=cnt+1
      while eq[tmp]=='+':
        eq[tmp]=None
        tmp=tmp+1
    cnt=cnt+1
  #print(eq)
  if eq[0]=='+':
    eq[0]=None
  return tiranone(eq)
def soma_independentes(eq):
  cnt=0
  lneq=len(eq)
  while cnt<lneq:
    if eq[cnt]=='*':
      return [simplifica(eq[:cnt-2])]+eq[cnt-2:]
    cnt=cnt+1
  return tiranone(eq)
def pega_incognitas(eq):
  lista=[]
  for i in eq:
    if ehvar(i):
      if i not in lista:
        lista.append(i)
  return lista
def junta_incognitas(eq,lista):
  coefs=[0]*len(lista)
  cnt=0
  lneq=len(eq)
  while cnt<lneq:
    if eq[cnt] in lista:
      ind=indice(eq[cnt],lista)
      coefs[ind]=coefs[ind]+eq[cnt-2]
    cnt=cnt+1
  return coefs
def removedup(lista):
  cnt1=0
  while cnt1<len(lista):
    cnt2=cnt1+1
    while cnt2<len(lista):
      if lista[cnt2]==lista[cnt1]:
        lista[cnt2]=None
      cnt2=cnt2+1
    cnt1=cnt1+1
  return tiranone(lista)
def pega_numeradores(eq):
  cnt=0
  lneq=len(eq)
  vret=[]
  while cnt<lneq:
    if eq[cnt]=='/':
      if eq[cnt+1]=='(':
        cnt=par_depois(eq,cnt+1)-1
      elif ehnum(eq[cnt+1]) or ehvar(eq[cnt+1]):
        cnt=cnt+1
    else:
      vret.append(eq[cnt])
    cnt=cnt+1
  return vret

def corrigediv1(eq):
  cnt=0
  lneq=len(eq)
  while cnt<lneq:
    if eq[cnt]=='/':
      if ehnum(eq[cnt+1]):                  #divisão por número
        eq[cnt]='*'
        eq[cnt+1]=1/eq[cnt+1]
      elif eq[cnt+1]=='(':
        fim=par_depois(eq,cnt+1)
        if temvar(eq[cnt+2:fim-1])==False:  #divisão por parentesis com apenas números
          ss=resolvem(eq[cnt+2:fim-1])
          ss=simplifica(ss)
          eq[cnt]='*'
          eq=eq[:cnt+1]+[1/ss]+eq[fim:]
          lneq=len(eq)
        else:                               #divisão por parentesis com números e incógnitas
          #numeradores=pega_numeradores(eq)
          #denominadores=pega_denominadores(eq)
          #print(numeradores)
          #if temvar(numeradores):
          return 'erro: sistema não linear'
      elif ehvar(eq[cnt+1]):                #divisão por incógnita
        #numeradores=pega_numeradores(eq)
        #denominadores=pega_denominadores(eq)
        #print(numeradores)
        #if temvar(numeradores):
        return 'erro: sistema não linear'
    cnt=cnt+1
  return tiranone(eq)

def coluna(n,m):
  vet=[]
  for i in m:
    vet.append(i[n])
  return vet
def transposta(m1):
  a=[]
  cnt1=0
  while cnt1<len(m1[0]):
    a.append(coluna(cnt1,m1))
    cnt1=cnt1+1
  return a
def escalona_matriz(m1,b1):
  m=m1
  b=b1
  cnt1=0
  while cnt1<len(m):
    cnt2=cnt1+1
    while cnt2<len(m):
      if m[cnt1][cnt1]!=0:
        r=m[cnt2][cnt1]/m[cnt1][cnt1]
        b[cnt2]=b[cnt2]-b[cnt1]*r
        cnt3=cnt1
        while cnt3<len(m[0]):
          m[cnt2][cnt3]=m[cnt2][cnt3]-m[cnt1][cnt3]*r
          cnt3=cnt3+1
        cnt2=cnt2+1
    cnt1=cnt1+1
  return (m,b)

def incmat(m,lim):
  final=len(m)-1
  while final>=0:
    m[final]=m[final]+1
    if m[final]>=lim[final]:
      m[final]=0
      final=final-1
    else:
      return m
def verificadiag(m):
  cnt=0
  while cnt<len(m):
    if m[cnt][cnt]==0:
      return True
    cnt=cnt+1
  return False
def resolvediag(m,b):
  poss=[]
  trocas=[0]*len(m)
  cnt1=0
  matcopia=list(m)
  bcopia=list(b)
  while cnt1<len(m):
    cnt2=0
    poss.append([])
    while cnt2<len(m):
      if m[cnt2][cnt1]!=0:
        poss[cnt1].append(cnt2)
      cnt2=cnt2+1
    cnt1=cnt1+1
  lim=[]
  for i in poss:
    lim.append(len(i))
  cnt1=0
  while cnt1<len(trocas):
    cnt2=cnt1+1
    while cnt2<len(trocas):
      if poss[cnt2][trocas[cnt2]]==poss[cnt1][trocas[cnt1]]:
        trocas=incmat(trocas,lim)
        #print(trocas)
        cnt1=-1
        cnt2=len(trocas)
      cnt2=cnt2+1
    cnt1=cnt1+1
  while verificadiag(m):
    cnt1=0
    while cnt1<len(trocas):
      matcopia[cnt1]=m[poss[cnt1][trocas[cnt1]]]
      bcopia[cnt1]=b[poss[cnt1][trocas[cnt1]]]
      cnt1=cnt1+1
    m=list(matcopia)
    b=list(bcopia)
    #print('matriz')
    #print(m)
  return (m,b)

def metodo1(m1,b1): # eliminação de gauss
  m1b1=resolvediag(m1,b1)
  m1=m1b1[0]
  b1=m1b1[1]
  mb=escalona_matriz(m1,b1)
  m=mb[0]
  b=mb[1]
  C=[]
  for i in b:
    C.append(0)
  cnt1=len(m)-1
  while cnt1>=0:
    cnt2=len(m)-1
    C[cnt1]=b[cnt1]
    while cnt2>cnt1:
      C[cnt1]=C[cnt1]-m[cnt1][cnt2]*C[cnt2]
      cnt2=cnt2-1
    C[cnt1]=C[cnt1]/m[cnt1][cnt2]
    cnt1=cnt1-1
  return C
def resolvem(eq):
  #eq=separa_termos(eq)     #transforma string em lista
  eq=corrigediv1(eq)
  #print(eq)
  eq=corrigepar(eq)         #1* antes dos parentesis
  #print(eq)
  eq=corrigemaismenos(eq)   #['+','-',valor] vira ['-',valor]
  #print(eq)
  eq=corrigemenos(eq)       #['-',valor] vira ['+',-valor]
  #print(eq)
  eq=reduz1(eq)             #aqui não tem mais (...)*(...)
  eq=eq+['+',0]
  while eq!=multiplica_rl_par(eq):
    eq=multiplica_rl_par(eq)#coloca os coeficientes sempre a esquerda dos parentesis
  eq=eq+['+',0]
  while eq!=multiplica_rl_inc(eq):
    eq=multiplica_rl_inc(eq)#coloca os coeficientes sempre a esquerda das incógnitas
  eq=eq+['+',0]
  eq=reduz2(eq)             #junta os termos independentes (todos os produtos são da forma numero*(...) ou numero*incognita)
  eq=eq+['+',0]
  while eq!=distribui(eq):
    eq=distribui(eq)        #aplica distributiva nos parentesis - não há mais parentesis aqui
  eq=eq+['+',0]
  eq=isola_independentes(eq)#move incógnitas para a direita da expressão
  eq=soma_independentes(eq) #soma termos independentes
  return eq
def resolve(eq): #retorna uma equação que deve resultar em 0
  cnt=0
  while eq[cnt]!='=':
    cnt=cnt+1
  esq=resolvem(separa_termos(eq[:cnt]))
  dir=resolvem(separa_termos('0-('+eq[cnt+1:]+')+0'))
  lista=pega_incognitas(esq)+pega_incognitas(dir)
  lista=removedup(lista)
  esqdir=par_inc(esq+['+']+dir,lista)
  termos_reduzidos=resolvem(esq+['+']+dir)
  coefs=junta_incognitas(termos_reduzidos,lista)
  cnt=0
  vret={'TI':termos_reduzidos[0]}
  while cnt<len(coefs):
    vret.update({lista[cnt]:coefs[cnt]})
    cnt=cnt+1
  return vret
def substituiinc(eq,nomes,nomesl1):
  cnt=0
  while cnt<len(nomes):
    while nomes[cnt] in eq:
      eq=eq[:eq.index(nomes[cnt])]+nomesl1[cnt]+eq[eq.index(nomes[cnt])+len(nomes[cnt]):]
    cnt=cnt+1
  return eq
def resolve_sistema(lista_eqs):
  nomesl1='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  tmp=[]
  for i in nomesl1:
    tmp.append(i)
  nomesl1=tmp

  reservados='1234567890.+-*/()='
  incs=[]
  for i in lista_eqs:
      cnt1=0
      while cnt1<len(i):
          if i[cnt1] not in reservados: #é incógnita
              cnt2=cnt1
              while cnt2<len(i) and i[cnt2] not in '.+-*/()=':
                  cnt2=cnt2+1
              if cnt2<len(i):
                  incog=i[cnt1:cnt2]
              else:
                  incog=i[cnt1:]
              cnt1=cnt2
              if incog not in incs:
                  incs.append(incog)
          cnt1=cnt1+1
  nomes=incs
  nomes2=[]
  cnt=0
  for i in nomes:
    nomes2.append('_____'+str(cnt)+'_____')
    cnt=cnt+1
  if len(nomes)!=0:
    cnt1=0
    while cnt1<len(lista_eqs):
      lista_eqs[cnt1]=substituiinc(lista_eqs[cnt1],nomes,nomes2)
      cnt1=cnt1+1
    cnt1=0
    while cnt1<len(lista_eqs):
      lista_eqs[cnt1]=substituiinc(lista_eqs[cnt1],nomes2,nomesl1)
      cnt1=cnt1+1
  else:
    nomes=nomesl1
  #print(lista_eqs)
  termos=[]
  inc={}
  for i in lista_eqs:
    termos.append(resolve('0+'+i))
  #print(termos)
  for i in termos:
    for j in i.keys():
      if j not in inc.keys():
        inc.update({j:[]})
  #print(inc)
  for i in inc.keys():
    for j in termos:
      if i in j.keys():
        inc.update({i:inc[i]+[j[i]]})
      else:
        inc.update({i:inc[i]+[0]})
  #print(inc)
  matriz=[]
  b=inc[list(inc.keys())[0]]
  for i in list(inc.keys())[1:]:
    matriz.append(inc[i])
  #print(matriz)
  matriz=transposta(matriz)
  cnt=0
  while cnt<len(b):
    b[cnt]=-b[cnt]
    cnt=cnt+1
  resultados=metodo1(matriz,b)
  cnt=0
  ret=[]
  while cnt<len(matriz):
    ret.append(nomes[nomesl1.index(list(inc.keys())[1:][cnt])]+'='+str(resultados[cnt]))
    cnt=cnt+1
  return ret
def exemplo1():
  print('eqs=[')
  print("'2.3*x+1.3*y+1.2*z+0.9*w=1-x',")
  print("'2.1*x+2.1*z+0.3*w+1.9*y=2+x+3*y',")
  print("'1.3*y+2.9*z+1.6*x+2*w=2.3*w-3',")
  print("'1.7*x+2*z+0.2*w=4-y'")
  print(']')
  print('res=resolve_sistema(eqs)')
  print("print(res)")
  print('#Reportar bugs para rogpaz1998@gmail.com')
def exemplo2():
  print("eq1='(8+9*3/4)+(2*3+y)*(2+3*1)+(2*3)*(2+3*1)+10.3*2+3*x-(12+3*2)+(2*3)*(2+3*1)=4*(x+y+2*3/6*10*(2+30-49*2*3*4*1*10/100)*1*3/10)+(2*3)*(2+3*1*x)*2-3*2*90/3+(2*3)*(2+3*1)'")
  print("eq2='(8+9*(3/4))+10.3*2+3*x-(12+3*2)=4*(x+y+2*(3/6)*10*(2+30-49*2*3*4*1*(10/100))*1*3/10)*2-3*2*(90/3)'")
  print("eq3='2*3*x*1+2*4+(2*3+90)*3-10+3*x+2*(2*2+x+y+3*2)*1.5-2*4+z+k+w=21'")
  print("eq4='2.3*x+1.3*y+1.2*z+0.9*w=1'")
  print("eq5='(1+2*9-3*5)*(23+3*10.4-100)*4*z/2+w*10/(1+5+5*5/5)+k*3*2+(1+2*9-3*5-2*2)*3*0*2*1*(10-4)*(23+3*10.4-100+4)*(10-4)*(23+3*10.4-100+4)*(10-4)*(23+3*10.4-100+4)*(23+3*10.4-100+4)*(10-4)*(23+3*10.4-100+4)+(1+2*9-3*5-2*(2+3*9*(2-4*4*3-100*x)*3+2*(9-2)*1.4)*3)*(23+3*10.4-100*0)+(1+2*9-3*5-y)*(23+3*10.4*0-100)*3/(2+3*9*(3-1+8*3/(2+2-10/(2+3))))+4*(1-3*x)+x*(2+5*4)-(1-3*x)*4+(2+5-4)*x+x-(2-3*(3*3+1-(9*1)))=(1+2*9-3*5)*(23+3*10.4-100)+5*(2+3*x)+3*2+x*(9*10+1-40)-(1+2*9-3*5)*(23+3*10.4-100)*4+(1+2*9-3*5-2*2)*3*0*2*1*(10-4)*(23+3*10.4-100+4)*(10-4)*(23+3*10.4-100+4)*(10-4)*(23+3*10.4-100+4)*(23+3*10.4-100+4)*(10-4)*(23+3*10.4-100+4)+(1+2*9-3*5-2*(2+3*9*(2-4*4*3-100*x)*3+2*(9-2)*1.4)*3)*(23+3*10.4-100*0)+(1+2*9-3*5-y)*(23+3*10.4*0-100)*3+4*(1-3*x)+x*(2+5*4)-(1-3*x)*4+(2+5-4)*x+x-(2-3*(3*3+1-(9*1)))'")
  print("res=resolve_sistema([eq1,eq2,eq3,eq4,eq5])")
  print("print(res)")
  print('#Reportar bugs para rogpaz1998@gmail.com')
def exemplo3():
  print('eqs=[')
  print("'2.3*x1+1.3*x2+1.2*x3+0.9*x4=1-x1',")
  print("'2.1*x1+2.1*x3+0.3*x4+1.9*x2=2+x1+3*x2',")
  print("'1.3*x2+2.9*x3+1.6*x1+2*x4=2.3*x4-3',")
  print("'1.7*x1+2*x3+0.2*x4=4-x2'")
  print(']')
  print("res=resolve_sistema(eqs)")
  print("print(res)")
  print('#Reportar bugs para rogpaz1998@gmail.com')
