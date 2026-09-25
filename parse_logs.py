import argparse
import os

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DRIFT_THRESHOLD = 0.02  # fraction out of tolerance before we flag a row


def load_export(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["deviation"] = (df["measured"] - df["reference"]).abs() / df["reference"]
    return df


def flag_out_of_tolerance(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["deviation"] > DRIFT_THRESHOLD]


def summarize(flagged: pd.DataFrame) -> str:
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )
    rows = flagged.to_csv(index=False)
    resp = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Summarize out-of-tolerance calibration readings for a QC report. Be concise.",
            },
            {"role": "user", "content": rows},
        ],
    )
    return resp.choices[0].message.content


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--summarize", action="store_true")
    args = parser.parse_args()

    df = load_export(args.csv_path)
    flagged = flag_out_of_tolerance(df)
    print(f"{len(flagged)} of {len(df)} readings out of tolerance")

    if args.summarize and not flagged.empty:
        print(summarize(flagged))


if __name__ == "__main__":
    main()
