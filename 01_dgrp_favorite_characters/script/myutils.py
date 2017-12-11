import re

def normalize_names(x):
    string = str(x.strip()).lower()
    
    # Normarlize names
    string = re.sub(re.compile("kokichi oma|kokichi ouma|ouma"),"kokichi",string)
    string = re.sub(re.compile("maki harukawa|harukawa"),"maki",string)
    string = re.sub(re.compile("rantaro amami|amami|rantarou"),"rantaro",string)
    string = re.sub(re.compile("ryoma hoshi|ryouma|hoshi"),"ryoma",string)
    string = re.sub(re.compile("kiibo|keebo|k1-b0"),"kibo",string)
    string = re.sub(re.compile("miu iruma|iruma"),"miu",string)
    
    return(string)