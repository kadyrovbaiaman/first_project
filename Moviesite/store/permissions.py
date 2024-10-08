from rest_framework import permissions


class CanWatchMovie(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.status == 'pro':
            return True

        elif request.user.status == 'simple' and obj.movie_status == 'simple':
            return True

        return False

