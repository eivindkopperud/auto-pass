def convert_date(datestring):
    year, month, date = datestring.split("-")
    month_dict = {
        "01": "januar",
        "02": "februar",
        "03": "mars",
        "04": "april",
        "05": "mai",
        "06": "juni",
        "07": "juli",
        "08": "august",
        "09": "september",
        "10": "oktober",
        "11": "november",
        "12": "desember",
    }
    return f"{date}. {month_dict[month]} {year}"