from django.shortcuts import redirect
from django.views.generic  import ListView
from .models import Favorite
from apps.Acount_app.mixin import CheckLogin
from apps.Tutorial_app.models import VideoTutorial
from django.http import JsonResponse

class FavoritView(CheckLogin,ListView):
    template_name = "Favorite_app/favorite.html"
    model = Favorite
    def get_context_data(self,**kwargs):

        context=super(FavoritView,self).get_context_data(**kwargs)
        favorite_video=Favorite.objects.filter(user=self.request.user)

        context["video"]=favorite_video


        return context


def LikeVideo(request,pk):


    if request.user.is_authenticated:
        user = request.user
        video = VideoTutorial.objects.get(id=pk)

        try:
            f = Favorite.objects.get(user=user,video=video)
            f.delete()

            return JsonResponse({"response":"unlike"})

        except:

            Favorite.objects.create(user=user, video=video)

            return JsonResponse({"response":"like"})
    
    else:
        return redirect("Tutorial:detail_video",pk)