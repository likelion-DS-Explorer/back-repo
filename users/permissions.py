python
from rest_framework import permissions

class IsClubManager(permissions.BasePermission):
    def has_permission(self, request, view):
        club_code = request.data.get('club_code')
        return request.user.can_manage_club(club_code)