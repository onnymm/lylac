from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any
from typing import Literal

NotificationTarget = Literal['current_user']

@dataclass
class Notification:
    name: str
    target: int | NotificationTarget
    payload: dict[str, Any]

class Notifier(ABC):
    Notification = Notification
    NotificationTarget = NotificationTarget
    _post_commit_notifications: list[Notification]

    def notify(
        self,
        name: str,
        target: int | NotificationTarget,
        payload: dict[str, Any],
        after_commit: bool,
    ) -> None:

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
