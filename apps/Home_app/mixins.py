from apps.Tutorial_app.models import VideoTutorial
from django.shortcuts import redirect

class CheckSoecial:

    def dispatch(self,request,pk):
        video=VideoTutorial.objects.get(id=pk)
        teacher=video.teacher.user.id

        if video.special_video == True:
            if request.user.is_authenticated:
                if request.user.is_specialuser() or request.user.is_admin or request.user.id == teacher:
                    return super(CheckSoecial,self).dispatch(request,pk)
                else:
                    return redirect("Home:Home")
            return redirect("Home:Home")
        else:
            return super(CheckSoecial,self).dispatch(request,pk)
        

class RedirectLogin:
    
    def dispatch(self,request,*args,**kwargs):
        
        if not request.user.is_authenticated:
            
            return redirect("Acount_app:Login")
        
        else:
            
            return super(RedirectLogin,self).dispatch(request,*args,**kwargs)