from flask import (
    Flask,
    render_template,
    send_file,
    request,
    Response,
    send_from_directory,
)
from get_info import get_data
import os
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

app.config["UPLOAD_FOLDER"] = "../downloads"
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


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
            return f"{il}, {pg}, {st}, {ste}, {request.url}"
        # print(il[25 * (pg - 1 ): 25 * (pg)])
        return render_template(
            "data_view.html",
            info=il[25 * (pg - 1) : 25 * (pg)],
            total_records=len(il),
            state=ste,
            n=25,
            prev="#",
            nxt="?pg=2",
            pg=1,
        )
    if stte is not None:
        il2 = get_data(stte, 2)
        if isinstance(il2, str):
            return "Error"
        # print(il[25 * (pg - 1 ): 25 * (pg)])
        return render_template(
            "data_view.html",
            info=il2[25 * (pg - 1) : 25 * (pg)],
            total_records=len(il2),
            state=stte,
            n=25,
            prev="#",
            nxt="?pg=2",
            pg=1,
        )
    if pg > 1:
        return render_template(
            "data_view.html",
            info=il[25 * (pg - 1) : 25 * (pg)],
            total_records=len(il),
            state=ste,
            n=25,
            prev=f"?pg={pg-1}" if pg > 2 else f"?pg=1&state={ste}",
            nxt=f"?pg={pg+1}" if pg != 5 else f"?pg=1&state={ste}",
            pg=pg,
        )
    return render_template(
        "data_view_home.html", n=len(STATE_NAME_LIST), sl=STATE_NAME_LIST
    )


@app.route("/data/download/<string:state>/<string:filetype>")
def download(state: str, filetype: str) -> Response:
    dirc = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])
    if filetype == "json":
        f1 = send_from_directory(
            dirc,
            path=f"./json/data_{state}.json",
            mimetype="application/json",
            download_name=f"data_{state}.json",
            as_attachment=True,
        )
        return f1

    elif filetype == "csv":
        file_csv = send_file(
            f"../downloads/csv/data_{state}.csv",
            mimetype="text/csv",
            download_name=f"data_{state}.csv",
            as_attachment=True,
        )
        return file_csv


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
