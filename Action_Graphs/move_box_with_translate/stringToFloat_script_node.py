def compute(db):
    """
    TokenToFloat Script Node
    Converts a token/string input to a float for downstream nodes.
    """

    try:
        # Access the input attribute exactly as created (case-sensitive)
        raw_value = db.inputs.Input_token  # do NOT use .get()

        # Convert to float
        db.outputs.Output_float = float(str(raw_value))

        print(f"[TokenToFloat Node] Converted '{raw_value}' → {db.outputs.Output_float}")

    except Exception as e:
        db.outputs.Output_float = 0.0
        print(f"[TokenToFloat Node] Conversion failed: {e}")

    return True

