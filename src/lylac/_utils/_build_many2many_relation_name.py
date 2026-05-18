import hashlib

def build_many2many_relation_name(
    model_x_name: str,
    model_y_name: str,
    field_x_name: str,
) -> str:

    x = model_x_name[:12]
    y = model_y_name[:12]
    field = field_x_name[:12]

    name = f'_rel_{x}__{field}__{y}'

    signature = (
        hashlib.md5(name.encode())
        .hexdigest()
        [:8]
    )

    name = name + '_' + signature

    return name