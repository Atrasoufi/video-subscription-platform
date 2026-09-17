from django.shortcuts import render
from .services import create_user_subscription 

def payment_callback(request):
    
    if payment_is_successful:
        
        
        create_user_subscription(user=request.user, plan=selected_plan)
        
        return render(request, "success.html")
