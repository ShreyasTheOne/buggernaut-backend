from rest_framework import permissions


class IsAuth(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user:
            return True
        else:
            return False


class IsTeamMemberOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):

        project = request.project
        user = request.user
        if user.is_superuser or user in project.members:
            return True
        else:
            return False


class IsReportedByOrTeamMemberOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        issue = request.issue
        user = request.user
        project = request.project
        if user.is_superuser or user in project.members or user == issue.reported_by:
            return True
        else:
            return False


class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True
        else:
            return False