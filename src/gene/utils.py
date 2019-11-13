def min_length(min_length):
    def validate(s):
        if len(s) >= min_length:
            return s
        raise ValidationError("String must be at least %i characters long" % min)
    return validate