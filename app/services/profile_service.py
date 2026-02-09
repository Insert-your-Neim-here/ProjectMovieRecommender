from app.models import Profile

def get_or_create_profile(request) -> Profile:
    if not request.session.session_key:
        request.session.save()

    profile_id = request.session.get("profile_id")
    if profile_id:
        return Profile.objects.get(id=profile_id)

    profile = Profile.objects.create()
    request.session["profile_id"] = str(profile.id)
    return profile