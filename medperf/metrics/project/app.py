# Code adapted from https://github.com/Sage-Bionetworks-Challenges/brats-dream-challenge-infra/blob/main/Docker/score.py

import argparse, os
import os
import subprocess
import argparse

import pandas as pd


def run_captk(pred, gold, tmp):
    """
    Run BraTS Similarity Metrics computation of prediction scan
    against goldstandard.
    """
    cmd = [
        os.path.join("/work/CaPTk/bin/Utilities"),
        "-i", gold,
        "-lsb", pred,
        "-o", tmp
    ]
    subprocess.check_call(cmd)


def extract_metrics(tmp, subject_id):
    """Get scores for three regions: ET, WT, and TC.
    Metrics wanted:
      - Dice score
      - Hausdorff distance
      - specificity
      - sensitivity
      - precision
    """
    res = (
        pd.read_csv(tmp, index_col="Labels")
        .filter(items=["Labels", "Dice", "Hausdorff95",
                       "Sensitivity", "Specificity",
                       "Precision"])
        .filter(items=["ET", "WT", "TC"], axis=0)
        .reset_index()
        .assign(subject_id=subject_id)
        .pivot(index="subject_id", columns="Labels")
    )
    res.columns = ["_".join(col).strip() for col in res.columns]
    return res


def score(parent, pred_lst, tmp_output="tmp.csv") -> pd.DataFrame:
    """Compute and return scores for each scan."""
    scores = []
    for pred in pred_lst:
        subject_id = pred.replace(".nii.gz", "")
        gold = os.path.join(parent, subject_id, subject_id + "_seg.nii.gz")
        try:
            run_captk(pred, gold, tmp_output)
            scan_scores = extract_metrics(tmp_output, subject_id)
            os.remove(tmp_output)  # Remove file, as it's no longer needed
        except subprocess.CalledProcessError:
            # If no output found, give penalized scores.
            scan_scores = (
                pd.DataFrame({
                    "subject_id": [subject_id],
                    "Dice_ET": [0], "Dice_TC": [0], "Dice_WT": [0],
                    "Hausdorff95_ET": [374], "Hausdorff95_TC": [374],
                    "Hausdorff95_WT": [374], "Sensitivity_ET": [0],
                    "Sensitivity_TC": [0], "Sensitivity_WT": [0],
                    "Specificity_ET": [0], "Specificity_TC": [0],
                    "Specificity_WT": [0], "Precision_ET": [0],
                    "Precision_TC": [0], "Precision_WT": [0]
                })
                .set_index("subject_id")
            )
        scores.append(scan_scores)
    return pd.concat(scores).sort_values(by="subject_id")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--preds_dir",
        "--preds-dir",
        type=str,
        required=True,
        help="Folder containing the labels",
    )
    parser.add_argument(
        "--data_path",
        "--data-path",
        type=str,
        required=True,
        help="Folder containing the data and ground truth",
    )
    parser.add_argument(
        "--output_file",
        "--output-file",
        type=str,
        required=True,
        help="file to store metrics results as YAML",
    )
    args = parser.parse_args()

    # Load all files
    results = score(args.data_path, os.listdir(args.preds_dir))

    results.to_csv(args.output_file)


if __name__ == "__main__":
    main()