from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from utils.data_loader import load_tar_file, load_ecb_file
from utils.comparator import TransactionComparator, format_discrepancies

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/compare", methods=["POST"])
def compare_files():
    if "tar_file" not in request.files or "ecb_file" not in request.files:
        return jsonify({"error": "Both files are required"}), 400

    tar_file = request.files["tar_file"]
    ecb_file = request.files["ecb_file"]

    # Ensure upload directory exists
    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Save files and process
    tar_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], secure_filename(tar_file.filename)
    )
    ecb_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], secure_filename(ecb_file.filename)
    )

    tar_file.save(tar_path)
    ecb_file.save(ecb_path)

    tar_data = load_tar_file(tar_path)
    ecb_data = load_ecb_file(ecb_path)

    comparator = TransactionComparator()
    discrepancies = comparator.compare_files(tar_data, ecb_data)

    # Cleanup
    os.remove(tar_path)
    os.remove(ecb_path)

    return jsonify({"discrepancies": format_discrepancies(discrepancies)})
