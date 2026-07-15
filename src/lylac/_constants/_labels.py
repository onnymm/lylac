class ERROR_LABEL:
    class EXECUTION:
        ACTION = 'No puedes ejecutar manualmente funciones registradas como validaciones.'
        AUTOMATION = 'No puedes ejecutar manualmente funciones registradas como automatizaciones.'
        ENV = 'No puedes ejecutar manualmente funciones registradas como resoluciones de variables de entorno.'
        POLICY = 'No puedes ejecutar manualmente funciones registradas como políticas.'
        SERVER_TASK = 'No puedes ejecutar manualmente funciones registradas como tareas de servidor.'
        VALIDATION = 'No puedes ejecutar manualmente funciones registradas como validationes.'
    class AUTHENTICATION:
        EXPIRED_SESSION = 'La sesión expiró.'
        INCORRECT_PASSWORD = 'La contraseña no es correcta.'
        INVALID_SESSION_UUID = 'Datos de autenticación inválidos.'
        USER_NOT_ACTIVE = 'El usuario está desactivado.'
        USER_NOT_FOUND = 'El usuario no existe.'
    class CONTEXT:
        MALFORMED_FIELD_DECLARATION = 'Formato inválido en declaración de campo.'
        MALFORMED_SEARCH_CRITERIA = 'Estructura de criterio de búsqueda mal formada.'
    class INTEGRITY:
        VALIDATIONS_FAILED = 'Las validaciones no pasaron.'
        POLICY_VERIFICATIONS_FAILED = 'Las verificaciones no pasaron.'
    class MODULE:
        ALREADY_LOADED = 'El módulo ya ha sido cargado.'

class MONITOR:
    INITIALIZATION_FINISHED = 'La base de datos de inicializó correctamente.'
