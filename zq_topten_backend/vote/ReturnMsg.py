class ReturnMsg(object):
    _Code = 200
    _Msg = 'Ok'
    _Data = None
    
    def __init__(self,Code = None,Msg = None,Data = None):
        if Code:
            self._Code  = Code
        if Msg:
            self._Msg = Msg
    
    def Update(self,Code = None,Msg = None,Data = None):
        if Code:
            self._Code  = Code
        if Msg:
            self._Msg = Msg

    @property
    def Data(self):
        return {
            'Code' : self._Code,
            'Msg' : self._Msg,
            'Data' : [] if self._Data == None else self._Data
        }

    
    