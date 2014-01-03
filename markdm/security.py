from .models import *

def groupfinder(userid, request):
    user = Users.by_id(userid)
    ret = []
    for g in user.mygroups:
        ret.append(g.groupname)
    return ret
