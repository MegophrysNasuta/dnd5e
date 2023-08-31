import re


CURRENCY_REGEX = re.compile(r'(\$(?P<L>\d+)\s?)?((?P<s>[0-9\-]+)\/(?P<d>[0-9\-]+))?')


def parse_currency(currency_str):
    """
    Input examples:
        $1 2/3
           -/6
    Output examples:
        L: 1, s: 2, d: 3
        L: 0, s: 0, d: 6
    """
    currency = re.match(CURRENCY_REGEX, currency_str)

    if not currency:
        raise ValueError("Malformed currency string: should be [$a ]b/c with 0 as -")
    else:
        currency = currency.groupdict()

    for key in 'Lsd':
        if not currency[key] or currency[key] == '-':
            currency[key] = 0

    return currency


def convert_to_denarii(L, s, d):
    shillings = (20 * int(L)) + int(s)
    return (12 * shillings) + int(d)


def subtract_currency(currency_dict, denarii_amt):
    d = convert_to_denarii(**currency_dict)
    if d < int(denarii_amt):
        raise ValueError("You can't afford it =(")

    s, d = divmod(int(denarii_amt), 12)
    L, s = divmod(s, 20)

    currency_dict['d'] = int(currency_dict.get('d', 0)) - d
    if currency_dict['d'] < 0:
        currency_dict['s'] -= 1
        currency_dict['d'] += 12

    currency_dict['s'] = int(currency_dict.get('s', 0)) - s
    currency_dict['L'] = int(currency_dict.get('L', 0))
    if currency_dict['s'] < 0:
        currency_dict['L'] -= 1
        currency_dict['s'] += 20

    currency_dict['L'] -= L
    return currency_dict

if __name__ == '__main__':
    while True:
        currency_str = input("Write the amount you have in L/s/d here: ")
        try:
            currency = parse_currency(currency_str)
        except ValueError as e:
            print(e)
        else:
            d = convert_to_denarii(**currency)
            print(f"Equivalent to {d}p.")

        price = input("\nAnd how much is what you want? (in pennies)")
        try:
            currency = subtract_currency(currency, int(price))
        except ValueError as e:
            print(e)
        else:
            print("Here's what you have left: %s" % currency)
