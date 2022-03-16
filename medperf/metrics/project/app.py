# Hello World Script
#
# This script is unrelated to the MLCube interface. It could be run
# independently without issues. It provides the actual implementation
# of the metrics. This file is executed by MLCube through mlcube.py
import argparse, os
import yaml
import SimpleITK as sitk
import medpy.metric.binary.dc as dice

def check_subject_validity(subject_dir):
    """Checks if a subject folder is valid.
    Args:
        subject_dir (str): The subject folder.
    Returns:
        bool: True if the subject folder is valid, False otherwise.
    """
    subject_valid = True
    strings_to_check = ["_seg.nii.gz"]

    for string in strings_to_check:
        if not os.path.isfile(os.path.join(subject_dir, os.path.basename(subject_dir) + string)):
            subject_valid = False
            break
    
    return subject_valid



def generate_metrics(gt, pred):
    """Generates the metrics for the provided data and predictions
    Args:
        gt (str): File name of ground truth.
        pred (str): File name of prediction.
    Returns:
        dict: dictionary containing key-value pairs for identified the labels-of-interest and the common identifier column.
    """
    results = {}
    ## might make sense to wait for sage response
    gt_array = sitk.GetArrayFromImage(sitk.ReadImage(gt))
    pred_array = sitk.GetArrayFromImage(sitk.ReadImage(pred))
    brats_labels_definitions = {"NET":"1", "ED":"2", "ET":"4", "TC":"1||4", "WT":"1||2||4"}

    for key in brats_labels_definitions:
        if "||" in brats_labels_definitions[key]:  # special case
            class_split = brats_labels_definitions[key].split("||")
            gt_array_split = gt_array == int(class_split[0])
            pred_array_split = pred_array == int(class_split[0])
            for i in range(1, len(class_split)):
                gt_array_split = gt_array_split | (
                    gt_array == int(class_split[i])
                )
                pred_array_split = pred_array_split | (
                    pred_array == int(class_split[i])
                )
        else:
            # assume that it is a simple int
            gt_array_split = gt_array == int(brats_labels_definitions[key])
            pred_array_split = pred_array == int(brats_labels_definitions[key])

        results_dict = {}
        results_dict["Dice"] = dice(gt_array_split, pred_array_split)

    return results


def generate_stats(data_path, preds_path):
    """Generates the metrics for the provided data and predictions
    Args:
        data_path (str): The path to the data folder
        preds_path (str): The path to the predictions folder
    """
    all_subjects_gt = os.listdir(data_path)
    all_subjects_preds = os.listdir(preds_path)

    for folders in all_subjects_gt:
        current_subject = os.path.join(data_path, folders)
        if os.path.isdir(current_subject):

            assert check_subject_validity(current_subject), "Subject {} does not contain ground truth".format(current_subject)

            prediction = os.path.join(preds_path, folders)

            for each_pred in all_subjects_preds:
                if folders in each_pred:
                    prediction_file = os.path.join(preds_path, each_pred)
                    break
                    
            # generate metrics
class ACC:
    # Given this is a toy example, the metric is implemented by hand
    # It is recommended that metrics are obtained from trusted
    # libraries
    @staticmethod
    def run(labels, preds):
        total_count = len(labels)
        correct_count = (labels == preds).sum()
        return correct_count / total_count


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
    results = generate_stats(args.data_path, args.preds_dir)

    with open(args.output_file, "w") as f:
        yaml.dump(results, f)


if __name__ == "__main__":
    main()