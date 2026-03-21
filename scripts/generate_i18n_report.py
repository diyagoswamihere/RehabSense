import ast
import json
import pathlib
import re


def main() -> None:
    app_path = pathlib.Path("backend/app.py")
    src = app_path.read_text(encoding="utf-8")
    mod = ast.parse(src)

    supported_languages = []
    translations = {}
    for node in mod.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "SUPPORTED_LANGUAGES":
                supported_languages = ast.literal_eval(node.value)
            if isinstance(target, ast.Name) and target.id == "TRANSLATIONS":
                translations = ast.literal_eval(node.value)

    # Apply static TRANSLATIONS['xx'].update({...}) overrides from the same file.
    for node in mod.body:
        if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
            continue
        call = node.value
        if not isinstance(call.func, ast.Attribute) or call.func.attr != "update":
            continue
        sub = call.func.value
        if not isinstance(sub, ast.Subscript):
            continue
        if not isinstance(sub.value, ast.Name) or sub.value.id != "TRANSLATIONS":
            continue
        if isinstance(sub.slice, ast.Constant) and isinstance(sub.slice.value, str):
            lang_code = sub.slice.value
        else:
            continue
        if not call.args:
            continue
        arg0 = call.args[0]
        if not isinstance(arg0, ast.Dict):
            continue
        updates = ast.literal_eval(arg0)
        if isinstance(translations.get(lang_code), dict):
            translations[lang_code].update(updates)

    # Mirror backend runtime fallback behavior: fill missing keys from English.
    en_dict = translations.get("en", {})
    for lang_code, lang_dict in translations.items():
        if not isinstance(lang_dict, dict):
            continue
        for key, value in en_dict.items():
            lang_dict.setdefault(key, value)

    # Mirror backend quality fallback for selected regional languages.
    hi_dict = translations.get("hi", {})
    for lang_code in ["mr", "ta", "kn", "te", "or", "pa", "hry", "gu", "bho", "ur"]:
        lang_dict = translations.get(lang_code, {})
        for key, en_value in en_dict.items():
            if lang_dict.get(key) == en_value and key in hi_dict:
                lang_dict[key] = hi_dict[key]

    template_keys = []
    pattern = re.compile(r"\{\{\s*t\('([a-zA-Z0-9_]+)'\)\s*\}\}")
    for tpl in pathlib.Path("frontend/templates").glob("*.html"):
        template_keys.extend(pattern.findall(tpl.read_text(encoding="utf-8", errors="ignore")))
    template_keys = sorted(set(template_keys))

    en = translations.get("en", {})
    report = {
        "template_keys": template_keys,
        "languages": {},
        "priority_by_fallback_ratio": []
    }

    for lang in supported_languages:
        lang_dict = translations.get(lang, {})
        missing = [k for k in template_keys if k not in lang_dict]
        fallback_equals_english = [
            k
            for k in template_keys
            if lang != "en" and k in lang_dict and k in en and lang_dict.get(k) == en.get(k)
        ]
        report["languages"][lang] = {
            "missing_count": len(missing),
            "fallback_count": len(fallback_equals_english),
            "fallback_ratio": (len(fallback_equals_english) / len(template_keys)) if template_keys else 0.0,
            "missing": missing,
            "fallback_equals_english": fallback_equals_english,
        }

    # Prioritize languages that still show most English fallback content.
    scored = []
    for lang in supported_languages:
        if lang == "en":
            continue
        info = report["languages"][lang]
        scored.append((lang, info["fallback_ratio"], info["fallback_count"]))
    scored.sort(key=lambda x: (-x[1], -x[2], x[0]))
    report["priority_by_fallback_ratio"] = [
        {
            "lang": lang,
            "fallback_ratio": ratio,
            "fallback_count": count,
        }
        for lang, ratio, count in scored
    ]

    out_path = pathlib.Path("i18n_missing_report.json")
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # Human-readable summary for quick tracking.
    summary_lines = [
        "# i18n Coverage Summary",
        "",
        f"- Template keys analyzed: {len(template_keys)}",
        f"- Languages analyzed: {len(supported_languages)}",
        "",
        "## By Language",
        "",
        "| Language | Missing Keys | English Fallback | Fallback Ratio |",
        "|---|---:|---:|---:|",
    ]
    for lang in supported_languages:
        info = report["languages"][lang]
        summary_lines.append(
            f"| {lang} | {info['missing_count']} | {info['fallback_count']} | {info['fallback_ratio']:.1%} |"
        )

    summary_lines.extend([
        "",
        "## Prioritized Native Translation Work",
        "",
        "| Priority | Language | Fallback Count | Fallback Ratio |",
        "|---:|---|---:|---:|",
    ])
    for idx, row in enumerate(report["priority_by_fallback_ratio"], start=1):
        summary_lines.append(
            f"| {idx} | {row['lang']} | {row['fallback_count']} | {row['fallback_ratio']:.1%} |"
        )

    pathlib.Path("i18n_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(f"written {out_path} keys={len(template_keys)} langs={len(supported_languages)}")
    for lang in supported_languages:
        info = report["languages"][lang]
        print(f"{lang}: missing={info['missing_count']} fallback_en={info['fallback_count']}")


if __name__ == "__main__":
    main()
