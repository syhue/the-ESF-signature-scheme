
"""
Created on Mon Jun 22 15:28:29 2020

@author: Hue
"""
import hashlib
import timeit
import math
import sympy
from Crypto import Random
import Crypto.Random.random
import xlsxwriter

N=100

workbook = xlsxwriter.Workbook('(FDH).xlsx')
worksheet = workbook.add_worksheet()
    

print("\n\n'''This is FDH Signature Scheme'''\n")


def key_generation():
 
    
    p = Crypto.Util.number.getPrime(1536, Random.new().read)
    q = Crypto.Util.number.getPrime(1536, Random.new().read)
      
    n = p*q
    phi = (p-1)*(q-1)
 
    while True:
        e = Crypto.Util.number.getRandomRange(1, phi-1, randfunc=None) 
        
        if math.gcd(e,phi) == 1:
            break
        
    d=sympy.mod_inverse(e,phi)
    return (e,d,n)

    


def generate_hash2(param_str):
  dk = hashlib.sha256()
  bparam_str = param_str.encode('utf-8')
  dk.update(bparam_str)
  return dk.hexdigest()



def sign_generation(d,n):
  

    m='Please send me a check of RM200.'  
    h=generate_hash2(m)
    H=int(h,16)
    x=pow(H,d,n)

   
    return x,m;
    

def sign_verification(x,e,m,n):

    h=generate_hash2(m)
    H=(int(h,16))%n
    
    if pow(x,e,n)==H:
        result='valid'
    else:
        result='invalid'
    print('hash value = %d...\n'%(int(str(H)[:20])))
    print('The signature is %s\n\n'%result)
    return result

j,totalkey,totalsign,totalveri,count1,i,t,sum=0,0,0,0,0,0,0,0


ESF,Time_Sign,Time_Ver,Key_e,Key_d,Key_n=[],[],[],[],[],[]

Signature,Message,Hash_Value,Result,Time_Key=[],[],[],[],[]


for _ in range(N):
    i+=1
    t+=1
    
    
    start2 = timeit.time.process_time()
    (e,d,n)=key_generation()
    end2 = timeit.time.process_time()
    time_KeyGen = end2 - start2
    totalkey += time_KeyGen
    
       
    for _ in range(N):
        j+=1
        
        print('__Operation %s__\n'% j)
        print('e = %d...' %(int(str(e)[:20])))
        print('d = %d...' %(int(str(d)[:20])))
        print('n = %d...' %(int(str(n)[:20])))
       
            
        start = timeit.time.process_time() 
        (x,m)=sign_generation(d,n)
        end = timeit.time.process_time()
        time_SignGen = end - start
        totalsign += time_SignGen
        h=generate_hash2(m)
        H=(int(h,16))%n
        print('signature = %d...' %(int(str(x)[:20])))
        print('message = %s.' %m)
            
        start1 = timeit.time.process_time()         
        result=sign_verification(x,e,m,n)
        end1 = timeit.time.process_time()
        time_SignVeri = end1 - start1
        totalveri += time_SignVeri
        print('Time taken for key generation %s is %.7lfs '%(j,time_KeyGen))
        print('Time taken for signing operation %s is %.7lfs '%(j,time_SignGen))
        print('Time taken for verifying operation %s is %.7lfs \n\n'%(j,time_SignVeri))
       
        ESF.append(j)
        Time_Sign.append(float(str(time_SignGen)[:9]))
        Time_Ver.append(float(str(time_SignVeri)[:9]))
        Time_Key.append(float(str(time_KeyGen)[:9]))
        Key_e.append(str(e))
        Key_d.append(str(d))
        Key_n.append(str(n))
        Signature.append(str(x))
        Message.append(m)
        Hash_Value.append(str(H))
        Result.append(result)


        
average_time_KeyGen=totalkey/N
average_time_signing=totalsign/pow(N,2)
average_time_verifying=totalveri/pow(N,2)

print('Average time taken for key operations is %.7lfs '%average_time_KeyGen)
print('Average time taken for signing operations is %.7lfs '%average_time_signing)
print('Average time taken for verifying operations is %.7lfs '%average_time_verifying)
    
 
    
row=1
for x in (ESF):
    worksheet.write(row, 0, x)
    
    row += 1


row=1
for y in (Time_Key):
    worksheet.write(row,8,y)
    row +=1
    
    
    
row=1
for y in (Time_Sign):
    worksheet.write(row,9,y)
    row +=1
    
    
row=1
for y in (Time_Ver):
    worksheet.write(row,10,y)
    row +=1   
    
    
row=1
for y in (Key_e):
    worksheet.write(row,1,y)
    row +=1      
    
 
    
row=1
for y in (Key_d):
    worksheet.write(row,2,y)
    row +=1  
    
  
    
row=1
for y in (Key_n):
    worksheet.write(row,3,y)
    row +=1      
    
 

    
row=1
for y in (Signature):
    worksheet.write(row,4,y)
    row +=1      
    
 
    
row=1
for y in (Message):
    worksheet.write(row,5,y)
    row +=1 
    
    
row=1
for y in (Hash_Value):
    worksheet.write(row,6,y)
    row +=1 
    
    
row=1
for y in (Result):
    worksheet.write(row,7,y)
    row +=1     
    
    
bold = workbook.add_format({'bold': True})
worksheet.set_column('N:N',20)
worksheet.set_column('I:K',13)  
worksheet.write(0, 0, 'No.',bold)
worksheet.write(0, 1, 'e',bold)
worksheet.write(0, 2, 'd',bold)
worksheet.write(0, 3, 'n',bold)
worksheet.write(0, 4, 'signature',bold)
worksheet.write(0, 5, 'message',bold)
worksheet.write(0, 6, 'hash value',bold)
worksheet.write(0, 7, 'Result',bold)
worksheet.write(0, 8, 'T_{KeyGen}',bold)
worksheet.write(0, 9, 'T_{Signing}',bold)
worksheet.write(0, 10, 'T_{Verifying}',bold)
worksheet.write(2, 13, 'Average T_{KeyGen}',bold)
worksheet.write(3, 13, 'Average T_{Signing}',bold)
worksheet.write(4, 13, 'Average T_{Verifying}',bold)
worksheet.write(2, 14, average_time_KeyGen)
worksheet.write(3, 14, average_time_signing)
worksheet.write(4, 14, average_time_verifying)
workbook.close()


