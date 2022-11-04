from flask import (
    Flask,
    render_template,
    request,
    Response,
    make_response,
)
from get_info import get_data, to_json, to_csv
from types import NoneType
from functools import cache


STATE_NAME_LIST = [
    "Andaman and Nicobar Islands",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chandigarh",
    "Chattisgarh",
    "Dadra and Nagar Haveli",
    "Daman and Diu",
    "Delhi",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jammu and Kashmir",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Lakshadweep Islands",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Pondicherry",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
]

app = Flask(__name__)


def check(li: list, i: int = 0, j: int = 25):
    try:
        dl = li[i:j]
    except IndexError:
        dl = li[i : len(li)]
    return dl


@app.route("/")
def home():
    return render_template("index.html")


@cache
@app.route("/data", methods=["GET", "POST"])
def data():
    pg = request.args.get("pg", type=int, default=1)
    stte = request.args.get("state", type=str)
    if request.method == "POST":
        global il, ste
        st = request.form.get("state", type=int)
        if isinstance(st, NoneType):
            return "Invalid Input"
        ste = STATE_NAME_LIST[st - 1]
        il = get_data(ste, 2)
        if isinstance(il, str):
            return il
        dl = check(il)
        return render_template(
            "data_view.html",
            info=dl,
            total_records=len(il),
            state=ste,
            n=len(dl),
            prev="#",
            nxt="?pg=2" if len(dl) > 25 else "#",
            pg=1,
        )
    if stte is not None:
        il2 = get_data(stte, 2)
        if isinstance(il2, str):
            return "Error"
        dl = check(il2)
        return render_template(
            "data_view.html",
            info=dl,
            total_records=len(il2),
            state=stte,
            n=len(dl),
            prev="#",
            nxt="?pg=2" if len(dl) > 25 else "#",
            pg=1,
        )
    if pg > 1:
        dl = check(il, 25 * (pg - 1), 25 * pg)
        return render_template(
            "data_view.html",
            info=dl,
            total_records=len(il),
            state=ste,
            n=len(dl),
            prev=f"?pg={pg-1}" if pg > 2 else f"?pg=1&state={ste}",
            nxt=f"?pg={pg+1}" if pg != 5 and len(dl) > 0 else f"?pg=1&state={ste}",
            pg=pg,
        )
    return render_template(
        "data_view_home.html", n=len(STATE_NAME_LIST), sl=STATE_NAME_LIST
    )


@app.route("/download/<string:state>/<string:filename>")
def download(state: str, filename: str) -> Response:
    if filename == "json":
        f1 = to_json(state)
        resp = make_response(f1)
        resp.headers[
            "Content-Disposition"
        ] = f"attachement; filename=data_{state.lower().replace(' ', '_')}.json"
        resp.mimetype = "application/json"
        return resp
    elif filename == "csv":
        f1 = to_csv(state)
        resp = make_response(f1)
        resp.headers[
            "Content-Disposition"
        ] = f"attachement; filename=data_{state.lower().replace(' ', '_')}.csv"
        resp.mimetype = "text/csv"
        return resp


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
