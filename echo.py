import re

def echo_loop():
    """
    사용자가 문장을 반복 입력하고,
    !quit 입력 시 종료하는 함수
    """
    quit_pattern = re.compile(r'^!quit$')

    while True:
        text = input("문장을 입력하세요 (!quit 입력 시 종료): ")

        if quit_pattern.match(text):
            print("echo 프로그램을 종료합니다.")
            break

        print(text)

if __name__ == "__main__":
    echo_loop()