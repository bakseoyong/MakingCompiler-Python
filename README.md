# MakingCompiler-Python

책 '컴파일러 만들기'에서 제공된 C++코드를 참고,학습하여 python으로 컴파일러를 제작하는 프로젝트입니다.

# 설명

Main.py
-------
sourceCode 문자열을 입력하여 Scanner, Parser, Generator, Machined 클래스를 순차적으로 호출시켜 작동시키는 클래스입니다.

Scanner.py
----------
함수, 함수명, 괄호 안에 파라미터 확인, 괄호, 변수타입, 변수명, 관계식, 세미콜론 등 개발자가 고수준의 레별로 작성한 코드를 토큰화 시키는 클래스입니다.

Token.py
--------
Scanner 클래스에서 구분한 키워드들을 타입으로 변경시키기 위한 관련 정보를 담고 있는 클래스 입니다.
ex) Variable = "var"
    For = "for"
    Break = "break" 
    Continue = "continue"
    If = "if"

Parser.py
---------
Scanner를 통해 완성된 토큰 리스트를 매개변수로 받아 문맥트리(Syntax Tree)를 생성하는 클래스 입니다.

Node.py
-------
문맥 트리를 구성하는 노드들에 대한 정보를 제공하는 클래스 입니다.

Generator.py
------------
문맥 트리의 노드들을 이용해 저수준의 언어인 목적코드를 만드는 작업을 진행하는 클래스입니다.

Code.py
-------
목적 코드를 구성하는 코드들에 대한 정보를 제공하는 클래스 입니다.

Machine.py(미완)
------------
목적코드를 통해 실제로 작동시키는 클래스입니다.
