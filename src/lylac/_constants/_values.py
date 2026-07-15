RELATION_PATH_SEPARATOR = '.'
ROOT_PATH = ''

class FIELD_SUFFIX:
    """
    ### Sufijo de campo
    Sufijo usado en leyendas de instancias de campo para localizar fragmentos de
    valores compuestos y unirlos en el procesamiento de conversión de datos de
    salida.
    """
    ID = '@@id'
    NAME = '@@name'
    REF_ID = '@@ref_id'
    AGG = '@@agg'

class ENCODE_REF:
    ( START, END ) = ( '__#@#', '#@#__' )

class DEFAULTS:
    CHAR_FIELD_LENGHT = 255
    SELECTION_FIELD_LENGHT = 255
    EXPIRATION_TOKEN_DAYS = 30
