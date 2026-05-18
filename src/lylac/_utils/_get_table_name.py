def get_table_name(
    model_name: str,
) -> str:

    # Obtención del nombre de la tabla del modelo
    model_table_name = model_name.replace('.', '_')

    return model_table_name
