from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from .llm_client.qwen25_client import Qwen25LocalClient

#  Zorgt ervoor dat Django's CSRF-beveiliging wordt uitgeschakeld (ivm desktopapp)
@csrf_exempt        

def chat_view(request: HttpRequest) -> HttpResponse:
    """
    Afhandeling van HTTP requests voor chat functionaliteit.
    CSRF is uitgeschakeld omdat dit een desktop applicatie betreft.

    Functionaliteit:
        1. Accepteert alleen POST requests voor berichten naar local LLM server
        2. Client is ondergebracht in model/ voor clean front-end/back-end scheiding
        3. GET requests renderen de standaard chat template
    """
    
    if request.method == 'POST':     
        try:              
            user_message = request.POST.get('message', '')
            if not user_message:
                return JsonResponse({"error":"No message provided"}, status=400)
            
            client = Qwen25LocalClient()
            response = client.message_handler(user_message)
            
            return JsonResponse({'message': response}) 
        
        except Exception as e:
            return JsonResponse({
                "error": f"Server Error {str(e)}"
            }, status=500)
        
    elif request.method == 'GET':
        return render(request, 'index.html')    # Betreft chat template
    
    else:
        return JsonResponse({"error": "Invalid Request"}, status=405)