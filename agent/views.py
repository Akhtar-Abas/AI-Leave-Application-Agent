from django.shortcuts import render
from django.conf import settings
from .agent import app  # LangGraph Agent
from .pdf_generator import generate_pdf 

def generate_leave_application(request):
    context = {}
    
    if request.method == "POST":
        data = request.POST
        action = data.get('action') 
        
        # Context maintain karna taake page refresh par data na jaye
        context = {
            'name': data.get('name', ''),
            'position': data.get('position', ''),
            'company': data.get('company', ''),
            'reason': data.get('reason', ''),
            'days': data.get('days', '1'),
            'application_text': data.get('application_text', ""),
            'user_feedback': data.get('user_feedback', ""),
        }

        # --- CASE 1: PDF GENERATION ---
        if action == "approve":
            if context['application_text']:
                pdf_path = generate_pdf(context['application_text'], context['name'])
                context['pdf_url'] = f"{settings.MEDIA_URL}{pdf_path}"
                context['success_message'] = "Mubarak ho! Aapki PDF tayyar hai."
                return render(request, 'index.html', context)

        # --- CASE 2: AI DRAFTING / UPDATING ---
        try:
            # Days ko safely integer mein convert karna
            try:
                days_val = int(context['days'])
            except:
                days_val = 1

            # LangGraph invoke: 'feedback' key wahi hai jo agent.py mein use ho rahi hai
            result = app.invoke({
                "name": context['name'],
                "position": context['position'],
                "company": context['company'],
                "reason": context['reason'],
                "days": days_val,
                "application_text": context['application_text'],
                "feedback": context['user_feedback'], 
                "retry_count": 0
            })
            
            # AI ka naya response context mein update karein
            context['application_text'] = result.get('application_text', '')
            context['show_preview'] = True 
            
        except Exception as e:
            context['error'] = f"AI Error: {str(e)}"

    return render(request, 'index.html', context)