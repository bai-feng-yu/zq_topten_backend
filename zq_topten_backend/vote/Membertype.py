from .models import Expert,Leader

def get_type(member_id):
    member_type=0

    if Leader.objects.filter(whuid=member_id).exists():
        member_type = 1
    elif Expert.objects.filter(whuid=member_id).exists():
        member_type = 2

    return member_type