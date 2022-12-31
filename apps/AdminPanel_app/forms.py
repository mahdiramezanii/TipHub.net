from django import forms
from apps.Tutorial_app.models import VideoTutorial


class CreateVideoForm(forms.ModelForm):

    class Meta:
        model=VideoTutorial
        
        fields=["titel", "discription", "video_time", "video_cover", "video", "category", "tag","is_active","special_video"]


        widgets={
            "titel":forms.TextInput(attrs={
                "class":"form-control","placeholder":"عنوان ویدیو را وارد کنید"
            }),



            "discription": forms.Textarea(attrs={
                "class": "form-control", "placeholder": "توضیحات ویدیو را وارد کنید"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-label",
            }),

            "special_video": forms.CheckboxInput(attrs={
                "class": "form-check-label",
            }),
            "video_time":forms.TextInput(attrs={
                "placeholder":"تایم ویدیو را وارد کنید"
            })
            
            
        }




