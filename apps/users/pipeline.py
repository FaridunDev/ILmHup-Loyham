def save_user_profile(backend, user, response, *args, **kwargs):
    """
    Google orqali kirgan foydalanuvchi ma'lumotlarini modelingizga moslab saqlash.
    """
    if backend.name == 'google-oauth2':
        # 1. Ism va familiyani Google'dan olish
        if not user.first_name:
            user.first_name = response.get('given_name', '')
        if not user.last_name:
            user.last_name = response.get('family_name', '')

        # 2. Rolni belgilash
        # Standart bo'yicha is_student=True allaqachon modelda bor, 
        # lekin bu yerda aniq belgilab ketish xavfsizroq.
        if not user.is_instructor:
            user.is_student = True
            
        user.save()
