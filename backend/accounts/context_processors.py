from .serializers import UserProfileSerializer

def user_profile_processor(request):
    if request.user.is_authenticated:
        serializer = UserProfileSerializer(request.user)
        return {"user_profile": serializer.data}
    return {}