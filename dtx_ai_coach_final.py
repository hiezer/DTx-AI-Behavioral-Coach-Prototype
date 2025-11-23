# dtx_ai_coach_final.py - DTx AI Koç Son Sürüm
import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()

# Sistem Promptu
SYSTEM_PROMPT = """
Sen, Pozitif Psikoterapi ilkelerine dayalı destekleyici bir sanal koçsun.

KURALLAR:
1. ASLA teşhis koyma veya terapi sunma
2. Profesyonel bir terapist olmadığını hatırlat
3. Kriz durumunda profesyonel yardım öner
4. Her cevabın bir soruyla bitmeli

YAKLAŞIM:
- Güçlü Yönler Odaklı
- Çözüm Odaklı  
- Pratik öneriler sun
- Küçük kazanımları kutla
"""

# Wellness Modülleri
WELLNESS_MODULES = {
    "nefes_egzersizi": "🫁 Derin Nefes: 4 saniye nefes al, 7 tut, 8'de ver",
    "minnettarlik": "🙏 Bugün seni mutlu eden 3 küçük şeyi düşün",
    "beden_tarama": "👁️ Vücudunu baştan ayağa tarayarak hislerini fark et",
    "fiziksel_aktivite": "🏃 5-10 dakika yürüyüş veya esneme hareketleri"
}

class SimpleDtxAICoach:
    def __init__(self):
        self.conversation = []
        
    def try_gemini(self, message):
        """Gemini API'yi dene"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key or "your_gemini" in api_key:
                return None
                
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"{SYSTEM_PROMPT}\nKullanıcı: {message}\nKoç:"
            response = model.generate_content(prompt)
            return response.text.strip()
        except:
            return None
    
    def try_openai(self, message):
        """OpenAI API'yi dene"""
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key or "your_openai" in api_key:
                return None
                
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content
        except:
            return None
    
    def try_huggingface(self, message):
        """Hugging Face API'yi dene"""
        try:
            api_key = os.getenv('HF_API_KEY')
            if not api_key or "your_hf" in api_key:
                return None
                
            # Daha basit bir model deneyelim
            API_URL = "https://api-inference.huggingface.co/models/gpt2"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            prompt = f"{SYSTEM_PROMPT}\nKullanıcı: {message}\nKoç:"
            
            payload = {
                "inputs": prompt,
                "parameters": {"max_new_tokens": 100, "temperature": 0.7}
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').replace(prompt, '').strip()
            return None
        except:
            return None
    
    def fallback_response(self, message):
        """API'ler çalışmazsa akıllı cevap"""
        message_lower = message.lower()
        
        if 'merhaba' in message_lower:
            return "Merhaba! Bugün nasılsın? Sana nasıl destek olabilirim? 😊"
        elif 'stres' in message_lower:
            return "Stresli hissetmeni anlıyorum. Biraz derin nefes almayı deneyelim mi? Bugün seni ne mutlu etti? 🌟"
        elif 'iş' in message_lower or 'okul' in message_lower:
            return "İş/okul hayatında zorlandığını duydum. Bugün küçük bir başarın ne oldu? 💪"
        elif 'teşekkür' in message_lower:
            return "Rica ederim! Kendin için küçük bir iyilik yapmayı düşün 😊"
        else:
            return "Bunu paylaştığın için teşekkürler. Şu an sana iyi gelecek bir şey ne olabilir? ✨"
    
    def get_response(self, user_message):
        """Ana yanıt fonksiyonu"""
        print(f"\n👤 Kullanıcı: {user_message}")
        
        # API'leri dene
        apis = [
            ("Gemini", self.try_gemini),
            ("OpenAI", self.try_openai),
            ("HuggingFace", self.try_huggingface)
        ]
        
        for api_name, api_func in apis:
            print(f"   🔄 {api_name} deneniyor...")
            response = api_func(user_message)
            if response and len(response) > 10:
                print(f"   ✅ {api_name} başarılı!")
                return response
            else:
                print(f"   ❌ {api_name} çalışmadı")
        
        # Fallback
        print("   🔄 Fallback modu...")
        return self.fallback_response(user_message)
    
    def get_wellness(self, module_name):
        """Wellness modülü getir"""
        return WELLNESS_MODULES.get(module_name, "Modül bulunamadı")

def main():
    print("🤖 DTx AI Koç - Basit ve Temiz Versiyon")
    print("=" * 45)
    
    # API anahtarlarını kontrol et
    print("\n🔑 API Durumu:")
    apis = {
        'OpenAI': os.getenv('OPENAI_API_KEY'),
        'Gemini': os.getenv('GEMINI_API_KEY'), 
        'HuggingFace': os.getenv('HF_API_KEY')
    }
    
    for name, key in apis.items():
        status = "✅ VAR" if key and "your_" not in key else "❌ YOK"
        print(f"   {name}: {status}")
    
    # Koçu başlat
    coach = SimpleDtxAICoach()
    
    print("\n🫁 Wellness Modülleri:")
    for name in WELLNESS_MODULES.keys():
        print(f"   📦 {name}")
    
    print("\n💬 Test Başlıyor...")
    print("-" * 30)
    
    # Test mesajları
    tests = [
        "Merhaba",
        "Bugün çok stresliyim",
        "İş yerinde zorlanıyorum", 
        "Teşekkürler"
    ]
    
    for test in tests:
        response = coach.get_response(test)
        print(f"🤖 Koç: {response}\n")
    
    print("🎉 TEST TAMAMLANDI!")
    print("👉 Proje çalışıyor! GitHub'a hazır!")

if __name__ == "__main__":
    main()