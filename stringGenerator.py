import string
import random
# from Farms.models import Farm

def generate(size=10, chars=string.ascii_lowercase+string.digits+"[]()!^$#~"):
    st=""
    for i in range(size):
        st+=random.choice(chars)
    return st

def generateUnicque(model, field:str, size=10, chars=string.ascii_lowercase+string.digits+"[]()!^$#~"):
    while True:
        for i in range(500):
            try:
                g=generate(size, chars)
                f={field:g}
                model.objects.get(**f)
            except:
                return g
        size+=1

# print(generate())

# print(generateUnicque(Farm, "token",size=1, chars="10"))