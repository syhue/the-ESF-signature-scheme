#from random import randrange, getrandbits
from fractions import Fraction
from random import seed
from random import randint
import hashlib
import timeit
import Crypto.Random.random
from Crypto import Random
import xlsxwriter

N=100

workbook = xlsxwriter.Workbook('ESF.xlsx')
worksheet = workbook.add_worksheet()


print("\n\n'''This is the modified ESF Signature Scheme'''\n")

def solve_Dioph(a,b,c):
    m1=1
    m2=0
    n1=0
    n2=1
    r1=a
    r2=b
    while r1%r2!=0:
        q=r1//r2
        aux=r1%r2
        r1=r2
        r2=aux
        aux3=n1-(n2*q)
        aux2=m1-(m2*q)
        m1=m2
        n1=n2
        m2=aux2
        n2=aux3
    return m2*c,n2*c;


    

def key_generation():
    
    p = Crypto.Util.number.getPrime(1536, Random.new().read)
    q = Crypto.Util.number.getPrime(1536, Random.new().read)
    
    n=p*q
    f=Fraction(p-1,q-1)
    s=f.denominator
    omega=s*(p-1)+1
    seed(1)
    for _ in range(1):
        u = Crypto.Util.number.getRandomRange(1, n, randfunc=None) 
        gamma = Crypto.Util.number.getRandomRange(1, n, randfunc=None)
       
    
    (a,b)=solve_Dioph(u, gamma, omega)
    (v,Lambda)=(a%n,b%n)
    
    for _ in range(1):
        x = randint(1,n)
       

    X1=pow(x,u,n)
    X2=pow(x,gamma,n)

    
    return n,u,gamma,X1,X2,v,Lambda,omega,x;


def generate_hash2(secret, param_str):
  dk = hashlib.sha256()
  bsecret = secret.encode('utf-8')
  bparam_str = param_str.encode('utf-8')
  dk.update(bsecret)
  dk.update(bparam_str)
  return dk.hexdigest()


def sign_generation(n,u,gamma,X1,X2,v,Lambda,omega,x):
  
 
    for _ in range(1):
        y = Crypto.Util.number.getRandomRange(1, n, randfunc=None)
   

    Y1=pow(y,u,n)
    Y2=pow(y,gamma,n)
    I=Y1*Y2
    M="Please send me a check of RM200."    
    c=(int(generate_hash2(str(I),M), 16))
    
    z=(pow(x,c,n)*(y%n))%n
    
    return (I,c,z,M);


def sign_verification(n, u, gamma, X1, X2,I,c,z,M):
    

    
    C=int(generate_hash2(str(I),M), 16)
 
    
    if pow(z,u+gamma,n)==(pow((X1*X2),C,n)*(I%n))%n:
        result='valid'
    else:
        result='invalid'
        
    print('hash value = %d...\n' %(int(str(C)[:7])))
    print('The signature is %s.\n'%result)
    return result


j,totalkey,totalsign,totalveri,count1,i,m,sum=0,0,0,0,0,0,0,0

ESF,Time_Sign,Time_Ver,Key_u,Key_gamma,Key_v,Key_Lambda,Key_omega,Key_n=[],[],[],[],[],[],[],[],[]
Signature,Message,Hash_Value,Result,Time_Key=[],[],[],[],[]


for _ in range(N):
    i+=1
    m+=1
    start2 = timeit.time.process_time()
    (n,u,gamma,X1,X2,v,Lambda,omega,x)=key_generation()
    end2 = timeit.time.process_time()
    time_KeyGen = end2 - start2
    totalkey += time_KeyGen
    
       
    for _ in range(N):
        j+=1
        
        print('__Operation %s__\n'% j)
        print('u = %d...' %(int(str(u)[:7])))
        print('gamma = %d...' %(int(str(gamma)[:7])))
        print('v = %d...' %(int(str(v)[:7])))
        print('lambda = %d...' %(int(str(Lambda)[:7])))
        print('omega = %d...' %(int(str(omega)[:7])))
        print('n = %d...' %(int(str(n)[:7])))
            
        start = timeit.time.process_time() 
        (I,c,z,M)=sign_generation(n,u,gamma,X1,X2,v,Lambda,omega,x)
        end = timeit.time.process_time()
        time_SignGen = end - start
        totalsign += time_SignGen
        print('signature = %d...' %(int(str(z)[:7])))
        print('message = %s.' %M)
            
        start1 = timeit.time.process_time()         
        result=sign_verification(n, u, gamma, X1, X2,I,c,z,M)
        end1 = timeit.time.process_time()
        time_SignVeri = end1 - start1
        totalveri += time_SignVeri
        print('Time taken for signing operation %s is %.7lfs '%(j,time_KeyGen))
        print('Time taken for signing operation %s is %.7lfs '%(j,time_SignGen))
        print('Time taken for verifying operation %s is %.7lfs \n\n'%(j,time_SignVeri))
        
        ESF.append(j)
        Time_Sign.append(float(str(time_SignGen)[:9]))
        Time_Ver.append(float(str(time_SignVeri)[:9]))
        Time_Key.append(float(str(time_KeyGen)[:9]))
        Key_u.append(str(u))
        Key_gamma.append(str(gamma))
        Key_v.append(str(v))
        Key_Lambda.append(str(Lambda))
        Key_omega.append(str(omega))
        Key_n.append(str(n))
        Signature.append(str(z))
        Message.append(M)
        Hash_Value.append(str(c))
        Result.append(result)
        
       
       
      
average= totalkey/N   
average_time_signing=totalsign/pow(N,2)
average_time_verifying=totalveri/pow(N,2)

print('Average time taken for key operations is %.7lfs '%average)
print('Average time taken for signing operations is %.7lfs '%average_time_signing)
print('Average time taken for verifying operations is %.7lfs '%average_time_verifying)
    


row=1
for x in (ESF):
    worksheet.write(row, 0, x)
    
    row += 1


row=1
for y in (Time_Key):
    worksheet.write(row,11,y)
    row +=1  
    
    
    
row=1
for y in (Time_Sign):
    worksheet.write(row,12,y)
    row +=1
    
row=1
for y in (Time_Ver):
    worksheet.write(row,13,y)
    row +=1   
    
    
row=1
for y in (Key_u):
    worksheet.write(row,1,y)
    row +=1      
    
 
    
row=1
for y in (Key_gamma):
    worksheet.write(row,2,y)
    row +=1  
    
  
    
row=1
for y in (Key_v):
    worksheet.write(row,3,y)
    row +=1      
    
 
    
row=1
for y in (Key_Lambda):
    worksheet.write(row,4,y)
    row +=1  
    
    
row=1
for y in (Key_omega):
    worksheet.write(row,5,y)
    row +=1      
    
 
    
row=1
for y in (Key_n):
    worksheet.write(row,6,y)
    row +=1  
    
  
    
row=1
for y in (Signature):
    worksheet.write(row,7,y)
    row +=1      
    
 
    
row=1
for y in (Message):
    worksheet.write(row,8,y)
    row +=1 
    
row=1
for y in (Hash_Value):
    worksheet.write(row,9,y)
    row +=1 
    
    
row=1
for y in (Result):
    worksheet.write(row,10,y)
    row +=1     
    
    
bold = workbook.add_format({'bold': True})
worksheet.set_column('P:P',20)
worksheet.set_column('L:N',13)   
worksheet.write(0, 0, 'No.',bold)
worksheet.write(0, 1, 'u',bold)
worksheet.write(0, 2, 'gamma',bold)
worksheet.write(0, 3, 'v',bold)
worksheet.write(0, 4, 'lambda',bold)
worksheet.write(0, 5, 'omega',bold)
worksheet.write(0, 6, 'n',bold)
worksheet.write(0, 7, 'signature',bold)
worksheet.write(0, 8, 'message',bold)
worksheet.write(0, 9, 'hash value',bold)
worksheet.write(0, 10, 'Result',bold)
worksheet.write(0, 11, 'T_{KeyGen}',bold)
worksheet.write(0, 12, 'T_{Signing}',bold)
worksheet.write(0, 13, 'T_{Verifying}',bold)
worksheet.write(2, 15, 'Average T_{KeyGen}',bold)
worksheet.write(3, 15, 'Average T_{Signing}',bold)
worksheet.write(4, 15, 'Average T_{Verifying}',bold)
worksheet.write(2, 16, average)
worksheet.write(3, 16, average_time_signing)
worksheet.write(4, 16, average_time_verifying)
workbook.close()

 
