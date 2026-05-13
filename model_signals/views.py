import json

from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User


class UsersView(View):

    def get(self, request):
        users = User.objects.all().values('id', 'username', 'email')
        return JsonResponse(list(users), safe=False)
    
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email}, status=201)


class ProfileView(View):
    
    def get(self, request, pk=None):
        if pk:
            profile = User.objects.get(id=pk).profile
            return JsonResponse({'user': profile.user.username, 'bio': profile.bio})
        else:
            profiles = User.objects.filter(profile__isnull=False).values('id', 'username', 'profile__bio')
            return JsonResponse(list(profiles), safe=False)
    
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=data['user_id'])
        profile, created = user.profile.get_or_create(user=user)
        profile.bio = data.get('bio', profile.bio)
        profile.save()
        return JsonResponse({'user': profile.user.username, 'bio': profile.bio}, status=201)
    
    def put(self, request, pk):
        data = json.loads(request.body)
        profile = User.objects.get(id=pk).profile
        profile.bio = data.get('bio', profile.bio)
        profile.save()
        return JsonResponse({'user': profile.user.username, 'bio': profile.bio})
    
    def delete(self, request, pk):
        profile = User.objects.get(id=pk).profile
        profile.delete()
        return JsonResponse({'message': 'Profile deleted'}, status=204)
    