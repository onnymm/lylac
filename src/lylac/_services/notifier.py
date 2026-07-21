from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any
from typing import Union
from .._typing.generics import ItemOrList
from .._typing.literals import LiteralTarget
from .._typing.structures import NotificationTarget
from .._utils import to_list

@dataclass
class Notification:
    name: str
    target: LiteralTarget | list[int]
    payload: dict[str, Any]

class Notifier(ABC):
    Notification = Notification
    NotificationTarget = NotificationTarget
    _post_commit_notifications: list[Notification]

    def notify(
        self,
        name: str,
        target: Union[LiteralTarget, ItemOrList[int]],
        payload: dict[str, Any],
        after_commit: bool,
    ) -> None:

        # Si el objetivo es una ID de usuario como escalar...
        if isinstance(target, int):
            # Se envuelve ésta en una lista
            target = to_list(target)

        # Inicialización de objeto de notificación
        notification = Notification(name, target, payload)

        # Si la notificación debe hacerse después después del commit
        if after_commit:
            self._post_commit_notifications.append(notification)

        # Si la notificación debe ser enviada inmediatamente
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

    def __init__(
        self,
        uid: int,
    ) -> None:

        # Asignación de valores
        self._uid = uid
        # Inicialización de lista de notificaciones a enviar después de commit
        self._post_commit_notifications = []

    def send(
        self,
        notification,
    ):

        if notification.target == 'current_user':
            print(notification.name, notification.payload)
