import re
import echo


def is_valid_password(password):
    """
    비밀번호 검증 함수
    조건:
    - 알파벳 1개 이상
    - 숫자 1개 이상
    - 특수문자 1개 이상
    - 최소 6자 이상
    """
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{6,}$'
    return re.match(pattern, password) is not None


def main():
    while True:
        password = input("비밀번호를 입력하세요: ")

        if is_valid_password(password):
            print("비밀번호가 유효합니다.")
            print("echo 프로그램을 실행합니다.")
            echo.echo_loop()
            break
        else:
            print("비밀번호가 유효하지 않습니다. 다시 입력하세요.\n")


if __name__ == "__main__":
    main()