import time
def generate_feedback(time_analysis):
    feedback = []
    
    if time_analysis.get("Social Media", 0) >   120:  # >2 hours
        feedback.append("⚠️ Reduce social media usage!")
    
    if time_analysis.get("Productivity", 0) < 60:  # <1 hour
        feedback.append("🚀 Try focusing for longer periods!")
    
    return feedback if feedback else ["✅ Great productivity!"]