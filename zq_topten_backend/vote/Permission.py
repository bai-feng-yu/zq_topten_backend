from tempfile import TemporaryFile
from rest_framework.permissions import BasePermission
from .models import Member

class VotePermission(BasePermission):
    # TODO 传递学号和密码的加密
    def has_permission(self, request, view):
        user_id = request.POST.get('user_id',None)
        if user_id != None:
            user_id = user_id.strip()
        password = request.POST.get('password',None)
        if password != None:
            password = password.strip()
        if not (user_id and password):
            self.message = '缺少学号或者密码'
            return False
        try:
            member = Member.objects.get(student_id = user_id)
            if password != member.password:
                raise
        except:
            self.message = '学号或者密码错误'
            return False
        request.Stu = member
        return True
            