import pandas as pd
import numpy as np
import statistics #Tính toán thống kê
import os #lấy đường dẫn

# Đáp án chuẩn
ANSWER_KEY = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(",")

#Hàm mở file
def openFile():
    """Mở file và đọc dữ liệu thành DataFrame pandas"""
    #Đường dẫn thư mục
    folder = "data-files/Data Files"
    while True:
        fileName = input("Enter a class file to grade (i.e. class1 for class1.txt):")
        filepath = os.path.join(folder, f"{fileName}.txt")
        try:
            #Mở file chỉ đọc
            with open(filepath, "r", encoding="utf-8") as fp:
                print(f"Successfully opened '{fileName}.txt'")
                #Đọc toàn bộ nội dung file và tách thành từng dòng
                lines = fp.read().splitlines()
                #Tách chuỗi theo dấu , thành một list nhỏ
                data = [line.split(",") for line in lines]
                df = pd.DataFrame(data)
                return df, fileName   # trả cả DataFrame và tên file (class1, class2...)
        except FileNotFoundError:
            print(f"\nSorry, I can't find this '{fileName}.txt'\n")
        except Exception as e:
            print(f"Unexpected error while opening file: {e}")

#Hàm kiểm tra dữ liệu và phân tích hợp lệ hay ko
def checkData(df: pd.DataFrame):
    """Kiểm tra dữ liệu hợp lệ trong DataFrame"""
    invalid_rows = []

    print("**** ANALYZING ****")
    try:
        for idx, row in df.iterrows():
            ID = str(row[0]) if pd.notna(row[0]) else ""

            # kiểm tra số lượng cột
            if row.count() != 26:
                invalid_rows.append(idx)
                print("Invalid line of data: does not contain exactly 26 values:\n", ",".join(row.astype(str)))
                continue

            # kiểm tra định dạng ID bắt đầu bằng N và đằng sau là các số nguyên
            if len(ID) != 9 or not ID.startswith("N") or not ID[1:].isdigit():
                invalid_rows.append(idx)
                print("Invalid line of data: N# is invalid\n", ",".join(row.astype(str)))

        if len(invalid_rows) == 0:
            print("No errors found!")

        print("**** REPORT ****")
        print("Total valid lines of data:", len(df) - len(invalid_rows))
        print("Total invalid lines of data:", len(invalid_rows))

        # Trả về DataFrame chỉ gồm dòng hợp lệ
        return df.drop(invalid_rows)

    except Exception as e:
        print(f"Error during data validation: {e}")
        return df  # fallback: trả nguyên df

#Hàm tính toán điểm số
def score(df: pd.DataFrame, fileName: str):
    """Chấm điểm và in thống kê"""
    try:
        ids = df.iloc[:, 0]      #Lấy ra cột ID
        answers = df.iloc[:, 1:] #Lấy ra các câu trả lời
        scores = []

        for i in range(len(answers)):
            student_answers = answers.iloc[i].fillna("")   # thay NaN = ""
            score_val = 0
            for j, key in enumerate(ANSWER_KEY):
                ans = student_answers.iloc[j] if j < len(student_answers) else ""
                if ans == "":        # bỏ trống
                    score_val += 0
                elif ans == key:     # đúng
                    score_val += 4
                else:                # sai
                    score_val -= 1
            scores.append(score_val)

        # --- Lưu kết quả ra file ---
        out_file = f"{fileName}_grades.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"# This is what {fileName}_grades.txt should look like\n")
            for i in range(len(ids)):
                f.write(f"{ids.iloc[i]},{scores[i]}\n")
        print(f"Grades have been saved to '{out_file}'")

        # thống kê bằng numpy
        meanScore = np.mean(scores)
        highScore = np.max(scores)
        lowScore = np.min(scores)
        rangeScore = highScore - lowScore
        medianScore = statistics.median(scores)

        print(f"Mean (average) score: {meanScore:.2f}")
        print(f"Highest score: {highScore}")
        print(f"Lowest score: {lowScore}")
        print(f"Range of scores: {rangeScore}")
        print(f"Median score: {medianScore}")

        return scores

    except Exception as e:
        print(f"Error during scoring: {e}")
        return []

#Hàm main
def main():
    try:
        df, fileName = openFile()
        df_valid = checkData(df)
        score(df_valid, fileName)
    except Exception as e:
        print(f"Unexpected error in main: {e}")

if __name__ == "__main__":
    main()
