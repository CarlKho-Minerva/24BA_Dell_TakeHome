from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import logging
from typing import Dict, Tuple, Any
from utils.data_loader import load_tar_file, load_ecb_file
from utils.comparator import TransactionComparator, format_discrepancies

logger = logging.getLogger(__name__)
main = Blueprint("main", __name__)


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/compare", methods=["POST"])
def compare_files() -> Tuple[Dict[str, Any], int]:
    try:
        if current_app.config["DEV_MODE"]:
            # Use default files if paths are provided
            tar_path = request.form.get("tar_file_path", None)
            ecb_path = request.form.get("ecb_file_path", None)

            if not tar_path and (
                "tar_file" in request.files and request.files["tar_file"].filename
            ):
                tar_file = request.files["tar_file"]
                tar_path = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    secure_filename(tar_file.filename),
                )
                tar_file.save(tar_path)

            if not ecb_path and (
                "ecb_file" in request.files and request.files["ecb_file"].filename
            ):
                ecb_file = request.files["ecb_file"]
                ecb_path = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    secure_filename(ecb_file.filename),
                )
                ecb_file.save(ecb_path)

            if not tar_path or not ecb_path:
                return jsonify({"error": "Both TAR and ECB files are required"}), 400
        else:
            # Original file handling code
            if "tar_file" not in request.files or "ecb_file" not in request.files:
                logger.error("Missing required files in request")
                return jsonify({"error": "Both TAR and ECB files are required"}), 400

            tar_file = request.files["tar_file"]
            ecb_file = request.files["ecb_file"]

            # Validate file types
            if not (
                allowed_file(tar_file.filename) and allowed_file(ecb_file.filename)
            ):
                logger.error("Invalid file type submitted")
                return jsonify({"error": "Only CSV files are allowed"}), 400

            # Process files
            logger.info(
                f"Processing files: TAR={tar_file.filename}, ECB={ecb_file.filename}"
            )

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

        try:
            tar_data = load_tar_file(tar_path)
            ecb_data = load_ecb_file(ecb_path)
        except Exception as e:
            logger.error(f"Error loading files: {str(e)}")
            return jsonify({"error": "Error processing files"}), 500

        comparator = TransactionComparator()
        discrepancies = comparator.compare_files(tar_data, ecb_data)

        # Calculate total records
        total_records = len(set(list(tar_data.keys()) + list(ecb_data.keys())))

        # Cleanup
        os.remove(tar_path)
        os.remove(ecb_path)

        # Return discrepancies along with total records
        return jsonify({
            "discrepancies": format_discrepancies(discrepancies),
            "total_records": total_records
        })

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
