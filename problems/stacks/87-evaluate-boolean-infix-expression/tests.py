def visible():
    return [{'in': {'expr': '!F & T | F'}}, {'in': {'expr': '!!(T & !F)'}}, {'in': {'expr': 'F | T ^ T & F'}}]

def hidden():
    return [{'in': {'expr': 'T'}}, {'in': {'expr': 'F'}}, {'in': {'expr': '!!!T'}}, {'in': {'expr': 'T ^ T ^ T'}}, {'in': {'expr': '!(T | F) & T'}}, {'in': {'expr': '(T | F) & !(T ^ F)'}}, {'in': {'expr': 'F & T | !F ^ T'}}, {'in': {'expr': '!(!T | !F) ^ (T & !F)'}}, {'in': {'expr': '!((!((F | (!F & T ^ !T ^ !F ^ T & T ^ T) | (T & F & T & !F) ^ F)) | ((!F & F ^ !F | T) ^ ((!F & !T) ^ !(!F | !F)) | !((!(((F | F) ^ (!T | !T))) & (T & (!T | T)))) & !((!(F ^ T) ^ !T | F) | F ^ ((F | !F) ^ !T ^ T & !(!T ^ F) & !(T ^ !F))))) | (T ^ (F & !F) ^ !(!T | !T) & F & T ^ !T & T & !(F & F) ^ F & T | !F | T & !F | !((F | (T | !F & T)) & !(!(!F | T) | T ^ !T | T))))'}}]
