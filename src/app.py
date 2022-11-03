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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        st = request.form.get("state", type=int)
        ste = STATE_NAME_LIST[st - 1]
        il = get_data(ste, 2)
        if isinstance(il, str):
            return render_template("error_view.html", Error=il)
        return render_template(
            "data_view.html",
            info=il[:100:5],
            total_records=len(il),
            state=ste,
            n=len(il[:100:5]),
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
