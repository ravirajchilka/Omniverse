def compute(db):
    """
    TokenToFloat Script Node
    Converts a token/string input to a float for downstream nodes.
    """

    try:
        # Access the input attribute exactly as created (case-sensitive)
        raw_value = db.inputs.in_token_angle  # do NOT use .get()

        # Convert to float
        db.outputs.out_float_angle = float(str(raw_value))

        print(f"[TokenToFloat Node] Converted '{raw_value}' → {db.outputs.out_float_angle}")

    except Exception as e:
        db.outputs.out_float_angle = 0.0
        print(f"[TokenToFloat Node] Conversion failed: {e}")

    return True
