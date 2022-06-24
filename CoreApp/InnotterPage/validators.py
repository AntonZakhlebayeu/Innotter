from InnotterPage.models import Page
from InnotterUser.models import User


def IsUserOwner(user: User, pk: int):
    return user.pk == Page.objects.get(pk=pk).owner_id


def IsUserAdminOrModerator(user: User):
    return user.role == 'admin' or user.role == 'moderator'


def IsPublicPage(pk: int):
    return not Page.objects.get(pk=pk).is_private
