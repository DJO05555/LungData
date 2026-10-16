import re

GREETING = ("Hi! I can answer questions about our 5-million-row lung cancer dataset: what's in it, "
            "how we cleaned it, and what we found. What would you like to know?")

# TODO: add the key findings from the cleaned Power BI dashboard, one sentence each,
# for example "Current smokers have a higher positive rate than never-smokers."
FINDINGS = []

SIZE = "The raw dataset has 5,004,574 rows and 14 columns."
POSITIVE = "21.6% of records have a positive diagnosis."
MESSY_SUMMARY = ("The raw data has 5,004,574 rows and 14 columns. 40.8% of rows have at least one blank cell, "
                 "gender has 11 spelling variants and smoking status 18, 23,316 ages are written as words, "
                 "128,044 values are negative (like ages of -4 and -12) plus ages above 115, about 4,100 dates "
                 "are junk like 'yesterday', and every column was read as text.")
SMOKING_CLEANED = ("Smoking status had 18 spelling variants. Cleaning merged them into standard categories "
                   "and marked blanks as Unknown.")
SMOKING_MISSING = "About 284,593 rows (5.7%) were missing a smoking status in the raw data."
LABELS = ("Gender has 11 spelling and casing variants (like 'f_m', 'male', 'MALE') and smoking status has 18 "
          "(like 'Current-Smk').")
AGES = ("23,316 ages were written as words (like 'Twenty Five'), and 128,044 values were negative "
        "(like ages of -4 and -12), plus ages above 115.")
DATES = ("About 4,100 rows had junk dates such as 'yesterday' or 'N/A', mixed in with ISO, slash, and dash formats.")
TYPES = "Because of the messy values, all 14 columns were read as text, so no numeric operations worked until cleaning."
SYNTHETIC = ("The data is synthetic, generated from published reference distributions, so there are no real "
             "patients and no privacy risk. Its purpose is to practice big-data cleaning and analysis. "
             "It is not medical advice.")
TOOLS = "Python for generating and cleaning, Parquet for storage, and Power BI for the dashboards."
FINDINGS_ANSWER = (" ".join(FINDINGS) if FINDINGS else
                   "The risk-factor breakdown is on the Cleaned Data dashboard. I don't have a verified ranking "
                   "of factors yet, so please check the dashboard.")

FACTS = f"""
- {SIZE}
- {POSITIVE}
- {MESSY_SUMMARY}
- {SMOKING_MISSING}
- {SMOKING_CLEANED}
- {LABELS}
- {AGES}
- {DATES}
- {TYPES}
- {SYNTHETIC}
- {TOOLS}
""" + "\n".join(f"- {f}" for f in FINDINGS)

SYSTEM_PROMPT = (
    "You are the assistant for a university Big Data project about a synthetic lung cancer dataset. "
    "Answer only from the facts below. If the answer is not in the facts, say you don't know. "
    "Never give medical advice. Keep answers under 120 words.\n\nFACTS:" + FACTS
)

SUGGESTIONS = [
    "What does the messy data look like?",
    "How was smoking status cleaned?",
    "Which factor matters most for a positive diagnosis?",
    "Why is the data synthetic?",
]

KB = [
    (["hello", "hi", "hey", "help"], GREETING),
    (["messy", "raw", "wrong", "defects", "problems", "look"], MESSY_SUMMARY),
    (["smoking", "status", "cleaned", "clean", "fixed", "standardized", "standardised"], SMOKING_CLEANED),
    (["smoking", "status", "missing", "blank", "rows", "empty", "many"], SMOKING_MISSING),
    (["factor", "factors", "matters", "matter", "risk", "important", "cause", "predict"], FINDINGS_ANSWER),
    (["synthetic", "fake", "real", "why", "privacy"], SYNTHETIC),
    (["positive", "diagnosis", "rate", "percent"], POSITIVE),
    (["rows", "records", "size", "big", "columns", "scale", "dataset"], SIZE),
    (["gender", "labels", "variants", "casing"], LABELS),
    (["age", "ages", "words", "negative", "impossible"], AGES),
    (["date", "dates", "junk"], DATES),
    (["text", "types", "schema"], TYPES),
    (["tools", "python", "parquet", "power", "bi"], TOOLS),
]


def local_reply(question):
    words = set(re.findall(r"[a-z0-9]+", question.lower()))
    best, score = None, 0
    for keys, answer in KB:
        hits = len(words & set(keys))
        if hits > score:
            best, score = answer, hits
    return best or ("I can only answer from this project's data. Try asking about the messy data, "
                    "how it was cleaned, or why it is synthetic.")