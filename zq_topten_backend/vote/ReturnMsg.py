class ReturnMsg(object):
    _Code = 200
    _Msg = 'Ok'
    _Data = None
    _kwdata = None

    def __init__(self,Code = None,Msg = None,Data = None,**kwargs):
        if Code != None:
            self._Code  = Code
        if Msg != None:
            self._Msg = Msg
        if Data != None:
            self._Data = Data
        self._kwdata = kwargs

    @property
    def Data(self):
        ret = {
            'Code' : self._Code,
            'Msg' : self._Msg,
        }
        if self._Data != None:
            ret.update({'Data':self._Data})
        ret.update(self._kwdata)
        return ret

    
    