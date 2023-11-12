import json
import polib
import os
import collections
import datetime
import copy


def entry_check(pofile):
    lines_tranlated = len(po.translated_entries())
    lines_untranlated = len(po.untranslated_entries())

    words_tranlated = sum([len(entry.msgid.split(" "))
                          for entry in po.translated_entries()])
    words_untranlated = sum([len(entry.msgid.split(" "))
                            for entry in po.untranslated_entries()])

    result = {
        "words": collections.Counter({
            "trans": words_tranlated,
            "untrans": words_untranlated,
        }),
        "lines": collections.Counter({
            "trans": lines_tranlated,
            "untrans": lines_untranlated,
        }),
    }

    return result


if __name__ == "__main__":

    template = {
        "words": collections.Counter({
            "trans": 0,
            "untrans": 0,
        }),
        "lines": collections.Counter({
            "trans": 0,
            "untrans": 0,
        }),
    }

    directories = ["c-api", "distributing", "extending", "faq", "howto", "includes",
                   "installing", "library", "reference", "tutorial", "using", "whatsnew", ""]

    summary = {}

    for dir_name in directories:

        fixed_dir_name = dir_name
        if dir_name == "":
            fixed_dir_name = "root"
        summary[fixed_dir_name] = copy.deepcopy(template)

        for root, dirs, files in os.walk(f"../{dir_name}"):
            for file in files:
                if file.endswith(".po"):
                    filepath = os.path.join(root, file)
                    po = polib.pofile(filepath)
                    result = collections.Counter(entry_check(po))
                    summary[fixed_dir_name]["lines"] += result["lines"]
                    summary[fixed_dir_name]["words"] += result["words"]

    for key, value in summary.items():
        # print(key)
        summary[key]["words"] = dict(value["words"])
        summary[key]["lines"] = dict(value["lines"])

    file = open(
        f"calculate_progress/dist/result_{datetime.datetime.today().strftime("%Y%m%d_%H%M%S")}.json", "w")
    file.write(json.dumps(summary))
    file.close()
