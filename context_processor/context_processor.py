from apps.Tutorial_app.models import Category
from apps.Acount_app.models import Techer


def categorydata(request):

    context=Category.objects.all()

    return {
        "category":context
    }

def check_activ_teacher(request):

    if request.user.is_authenticated:
        user=request.user
        
        
        
        if Techer.objects.filter(user=user,is_active=True).exists():

        
            return {"is_teacher":True}
        
        else:
            
            return {"is_teacher":False}
        
    print("test2")
    return {"is_teacher": False}