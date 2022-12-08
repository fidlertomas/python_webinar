from flask import Flask, redirect, render_template, request


import skripty_predelane as sk

app = Flask(__name__)

zarizeni = dict(enumerate(sk.switche))


@app.route("/")
def flask_uvodni():
    return render_template("Seznam.html", zarizeni=zarizeni)


@app.route("/flask_error_disable/<int:index>", methods=["GET"])
def flask_error_disable(index):
    return sk.vypis_error_disable(zarizeni[index])


@app.route("/flask_podrobnosti_error_disable/<int:index>", methods=["GET"])
def flask_podrobnosti_error_disable(index):
    podrobnosti = sk.vypis_podrobnosti_error_disable(zarizeni[index])
    if podrobnosti is not None:
        return render_template(
            "tabulka_podrobnosti.html", info=podrobnosti, ip=zarizeni[index]
        )
    return "neni co zobrazit"


@app.route("/flask_podrobnosti_error_disable/", methods=["GET"])
def flask_podrobnosti_error_disable_all():
    data = dict()
    for ip in zarizeni.values():
        podrobnosti = sk.vypis_podrobnosti_error_disable(ip)
        if podrobnosti is not None:
            data[ip] = podrobnosti
    return render_template("tabulka_podrobnosti_vsech.html", data=data)


@app.route("/nahozeni_portu", methods=["POST"])
def flask_nahozeni_portu():
    port = request.form["port"]
    switch = request.form["switch"]
    print(f"vybran port {port} switche {switch}")
    sk.odblokuj_port(switch, port)
    return redirect("/", code=302)


app.run()
