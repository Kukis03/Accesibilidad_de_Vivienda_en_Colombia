def fmt_cop(val):
    return f"$ {val:,.0f}"

def fmt_cop_short(val):
    if val >= 1_000_000_000:
        return f"$ {val/1_000_000_000:.1f}B"
    elif val >= 1_000_000:
        return f"$ {val/1_000_000:.1f}M"
    else:
        return f"$ {val:,.0f}"

def fmt_pct(val):
    return f"{val:.1f}%"

def fmt_iah(val):
    return f"{val:.1f} años"
