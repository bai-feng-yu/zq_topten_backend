class ReturnMsg(object):
    _Code = 200
    _Msg = 'Ok'
    _Data = None
    _kwdata = None

    def __init__(self,Code = None,Msg = None,Data = None,**kwargs):
        if Code:
            self._Code  = Code
        if Msg:
            self._Msg = Msg
          
        self._kwdata = kwargs

    @property
    def Data(self):
        ret = {
            'Code' : self._Code,
            'Msg' : self._Msg,
            'Data' : [] if self._Data == None else self._Data
        }
        ret.update(self._kwdata)
        return ret

    
    