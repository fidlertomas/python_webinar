import skripty_predelane as sp

switche = {1: "10.200.1.205", 2: "10.200.1.204"}


def get_response(message: str) -> str:
    p_message = message.lower().strip()
    if p_message == "ahoj":
        return "Ahojte."

    if p_message == "!help":
        return "`Zkus napsat [vypis]`"

    slova_zpravy = p_message.split()
    if slova_zpravy[0] in ["vypiš", "vypis"]:
        if len(slova_zpravy) == 1:
            return "musíš napsat co chceš vypsat ... možnosti jsou:\n error-disable,\n switche nebo\n mac <uzivate>"
        if slova_zpravy[1] == "switche":
            return "\n".join(f"{key} : {value}" for key, value in switche.items())
        if slova_zpravy[1] == "error-disable":
            if len(slova_zpravy) == 3 and slova_zpravy[2].isnumeric():
                list_odpoved = []
                list_odpoved.append(
                    "vystup pro switch switch: " + switche[int(slova_zpravy[2])]
                )
                navrat = sp.vypis_podrobnosti_error_disable(
                    switche[int(slova_zpravy[2])]
                )
                if navrat:
                    for key, value in navrat.items():
                        list_odpoved.append(key + ":")
                        list_odpoved.append(value)
                odpoved = "\n".join(list_odpoved)
                return odpoved
            else:
                return f"Tohle musis napsat formou napriklad: vypis error-disable 1... testy {len(slova_zpravy) == 2} a {slova_zpravy[2].isnumeric()}:"

    return "Nerozumim. Zkus napsat [vypis]."


async def send_message(message, user_message, is_private=False):
    try:
        response = get_response(user_message)
        await message.author.send(
            response
        ) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
