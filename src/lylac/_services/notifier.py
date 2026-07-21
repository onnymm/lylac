from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Union
from .._resources import Notification
from .._typing.generics import ItemOrList
from .._typing.literals import LiteralTarget
from .._typing.structures import NotificationTarget
from .._utils import to_list

class Notifier(ABC):
    type Notification = Notification
    type NotificationTarget = NotificationTarget
    _post_commit_notifications: list[Notification]

    def __init__(
        self,
        uid: int,
    ) -> None:

        # Asignación de valores
        self._uid = uid
        # Inicialización de lista de notificaciones a enviar después de commit
        self._post_commit_notifications = []

    def notify(
        self,
        event: str,
        target: Union[LiteralTarget, ItemOrList[int]],
        payload: dict[str, Any],
        after_commit: bool,
    ) -> None:

        # Si el objetivo es una ID de usuario como escalar...
        if isinstance(target, int):
            # Se envuelve ésta en una lista
            target = to_list(target)

        # Inicialización de objeto de notificación
        notification = Notification(event, target, payload)

        # Si la notificación debe hacerse después después del commit...
        if after_commit:
            # Se añade la notificación para enviarse tras el commit
            self._post_commit_notifications.append(notification)

        # Si la notificación debe ser enviada inmediatamente...
        else:
            # Envío de la notificación
            self.send(notification)

    def flush(
        self,
    ) -> None:

        # Mientras existan notificaciones por ser enviadas...
        while self._post_commit_notifications:
            # Obtención de la siguiente notificación
            next_notificacion = self._post_commit_notifications.pop(0)
            # Envío de la notificación
            self.send(next_notificacion)

    @abstractmethod
    def send(
        self,
        notification: Notification,
    ) -> None:
        ...

class DefaultNotifier(Notifier):

    def send(
        self,
        notification,
    ):

        # Si el objetivo de la notificación es el usuario de la sesión actual...
        if notification.target == 'current_user':
            # Impresión en terminal
            print(notification.event, notification.payload)
