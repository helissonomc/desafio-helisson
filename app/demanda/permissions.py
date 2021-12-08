from rest_framework import permissions


class BlockAdministradorRequest(permissions.BasePermission):

    message = "Apenas Anunciantes podem usar endpoint!"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Anunciante').exists()