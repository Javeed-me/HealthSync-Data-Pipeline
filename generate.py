import pandas as pd
import random

def generate_data(n=1000):
    data = []

    for i in range(1, n+1):
        heart_rate = random.randint(50, 140)
        temperature = round(random.uniform(35, 40), 1)
        bp_systolic = random.randint(100, 150)
        bp_diastolic = random.randint(60, 100)

        abnormal = 1 if (
            heart_rate < 40 or heart_rate > 120 or
            temperature < 35 or temperature > 38
        ) else 0

        data.append({
            "patient_id": i,
            "heart_rate": heart_rate,
            "temperature": temperature,
            "bp_systolic": bp_systolic,
            "bp_diastolic": bp_diastolic,
            "abnormal": abnormal
        })

    df = pd.DataFrame(data)
    df.to_csv("data/input/healthcare_large.csv", index=False)

generate_data(1000)