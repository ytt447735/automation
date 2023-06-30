from fun.csdn import csdn
from fun import pu

token = 'X-Ca-Signature-Headers=x-ca-key,x-ca-nonce;X-Ca-Signature=udFnN3cgRPLxFMUnNanOeAr13CymGZm6/K0dsfKMc8Q=;X-Ca-Nonce' \
        '=c7aaa0f3-db6e-473e-a987-3fed3fb5b37f;X-Ca-Key=203816229;UserName=abczise520;UserToken' \
        '=6902ceb5be664138a92018138b9907bb'
ck = pu.convert_cookies_to_dict(token)

c = csdn(ck['UserToken'], ck['UserName'], ck['X-Ca-Signature'], ck['X-Ca-Signature-Headers'], ck['X-Ca-Nonce'],
         ck['X-Ca-Key'])
c.Getbyusername()
