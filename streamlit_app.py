import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="세로셈 곱셈 학습", page_icon="✏️", layout="wide")

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = None
if "problems" not in st.session_state:
    st.session_state.problems = []
if "current_problem" not in st.session_state:
    st.session_state.current_problem = 0
if "scores" not in st.session_state:
    st.session_state.scores = []
if "current_stage" not in st.session_state:
    st.session_state.current_stage = 0  # 0: 백의자리, 1: 십의자리, 2: 일의자리
if "answers" not in st.session_state:
    st.session_state.answers = [None, None, None]

# CSS 스타일
st.markdown("""
<style>
    .home-button { background-color: #FFE5B4; }
    .easy-button { background-color: #B4E5FF; }
    .hard-button { background-color: #FFB4D4; }
</style>
""", unsafe_allow_html=True)

def generate_problems(difficulty, count=5):
    """문제 생성"""
    problems = []
    if difficulty == "easy":
        # 올림 없는 곱셈 (예: 12 × 3 = 36)
        for _ in range(count):
            a = random.randint(10, 99)
            b = random.randint(2, 9)
            problems.append((a, b))
    else:
        # 올림 있는 곱셈 (예: 15 × 6 = 90)
        for _ in range(count):
            a = random.randint(10, 99)
            b = random.randint(2, 9)
            problems.append((a, b))
    return problems

def get_digits(num):
    """수를 자리수별로 분해"""
    tens = num // 10
    ones = num % 10
    return tens, ones

def show_home():
    """홈 화면"""
    st.markdown("# ✏️ 세로셈 곱셈 학습")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌟 초등학생을 위한 곱셈 배우기!")
        st.write("세로셈으로 곱셈의 원리를 차근차근 배워보세요.")
        st.write("각 자리수를 따로 계산한 후 더하는 방식을 이해하면 곱셈이 쉬워져요!")
    
    with col2:
        st.markdown("### 📚 이 앱의 특징")
        st.write("✅ 한 자리씩 천천히 배워요")
        st.write("✅ 즉시 피드백으로 실수를 바로 고쳐요")
        st.write("✅ 5문제 풀고 결과를 확인해요")
    
    st.divider()
    st.markdown("### 난이도 선택")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🟦 올림 없는 곱셈 (쉬움)", use_container_width=True, key="easy_btn"):
            st.session_state.difficulty = "easy"
            st.session_state.page = "learn"
            st.rerun()
    
    with col2:
        if st.button("🟩 올림 있는 곱셈 (어려움)", use_container_width=True, key="hard_btn"):
            st.session_state.difficulty = "hard"
            st.session_state.page = "learn"
            st.rerun()

def show_learn():
    """단계별 배우기 화면"""
    st.markdown("# 📚 세로셈 곱셈 배우기")
    
    if st.button("← 뒤로가기"):
        st.session_state.page = "home"
        st.session_state.difficulty = None
        st.rerun()
    
    st.divider()
    
    difficulty_name = "올림 없는 곱셈" if st.session_state.difficulty == "easy" else "올림 있는 곱셈"
    st.markdown(f"### {difficulty_name}")
    
    if st.session_state.difficulty == "easy":
        # 예시: 12 × 3
        st.markdown("#### 예시: 12 × 3 = ?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 단계 1️⃣: 십의 자리 × 3")
            st.write("**10** × 3 = **30**")
            st.write("→ 십의 자리 10에 3을 곱해요")
        
        with col2:
            st.markdown("#### 단계 2️⃣: 일의 자리 × 3")
            st.write("**2** × 3 = **6**")
            st.write("→ 일의 자리 2에 3을 곱해요")
        
        with col3:
            st.markdown("#### 단계 3️⃣: 모두 더하기")
            st.write("30 + 6 = **36**")
            st.write("→ 답은 36이에요!")
    
    else:
        # 올림 있는 곱셈 예시
        st.markdown("#### 예시: 15 × 6 = ?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 단계 1️⃣: 십의 자리 × 6")
            st.write("**10** × 6 = **60**")
            st.write("→ 십의 자리 10에 6을 곱해요")
        
        with col2:
            st.markdown("#### 단계 2️⃣: 일의 자리 × 6")
            st.write("**5** × 6 = **30**")
            st.write("→ 일의 자리 5에 6을 곱해요")
        
        with col3:
            st.markdown("#### 단계 3️⃣: 모두 더하기")
            st.write("60 + 30 = **90**")
            st.write("→ 답은 90이에요!")
    
    st.divider()
    
    if st.button("✅ 배웠어요! 문제 풀기 →", use_container_width=True, key="start_practice"):
        st.session_state.page = "practice"
        st.session_state.problems = generate_problems(st.session_state.difficulty, 5)
        st.session_state.current_problem = 0
        st.rerun()

def show_practice():
    """단계별 입력 화면"""
    st.markdown("# 💪 곱셈 연습하기")
    
    # 진행 상황 표시
    progress = st.session_state.current_problem / 5
    st.progress(progress, text=f"문제 {st.session_state.current_problem + 1} / 5")
    
    if st.button("← 뒤로가기"):
        st.session_state.page = "home"
        st.session_state.difficulty = None
        st.session_state.current_problem = 0
        st.session_state.current_stage = 0
        st.session_state.answers = [None, None, None]
        st.rerun()
    
    st.divider()
    
    if st.session_state.current_problem >= len(st.session_state.problems):
        st.session_state.page = "result"
        st.rerun()
    
    num1, num2 = st.session_state.problems[st.session_state.current_problem]
    tens, ones = get_digits(num1)
    
    st.markdown(f"### 문제: {num1} × {num2} = ?")
    
    st.markdown("""
    ```
         {num1}
        ×  {num2}
        -----
    ```
    """.format(num1=num1, num2=num2))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 단계 1️⃣: 십의 자리 계산")
        st.write(f"**{tens * 10}** × {num2} = ?")
        ans1 = st.number_input("십의 자리 결과:", min_value=0, max_value=9999, key=f"ans1_{st.session_state.current_problem}")
        if st.button("✓ 다음", key=f"next1_{st.session_state.current_problem}"):
            if ans1 == tens * 10 * num2:
                st.session_state.answers[0] = ans1
                st.session_state.current_stage = 1
                st.rerun()
            else:
                st.error(f"❌ 오답이에요! {tens * 10} × {num2} = {tens * 10 * num2}를 다시 확인해보세요.")
    
    if st.session_state.current_stage >= 1:
        with col2:
            st.markdown("#### 단계 2️⃣: 일의 자리 계산")
            st.write(f"**{ones}** × {num2} = ?")
            ans2 = st.number_input("일의 자리 결과:", min_value=0, max_value=999, key=f"ans2_{st.session_state.current_problem}")
            if st.button("✓ 다음", key=f"next2_{st.session_state.current_problem}"):
                if ans2 == ones * num2:
                    st.session_state.answers[1] = ans2
                    st.session_state.current_stage = 2
                    st.rerun()
                else:
                    st.error(f"❌ 오답이에요! {ones} × {num2} = {ones * num2}를 다시 확인해보세요.")
    
    if st.session_state.current_stage >= 2:
        with col3:
            st.markdown("#### 단계 3️⃣: 최종 답")
            result = num1 * num2
            st.write(f"**{tens * 10 * num2}** + **{ones * num2}** = ?")
            ans3 = st.number_input("최종 답:", min_value=0, max_value=9999, key=f"ans3_{st.session_state.current_problem}")
            if st.button("✓ 완료", key=f"complete_{st.session_state.current_problem}"):
                if ans3 == result:
                    st.session_state.answers[2] = ans3
                    st.session_state.scores.append(True)
                    st.success("🎉 정답이에요! 정말 잘했어요!")
                    st.balloons()
                else:
                    st.session_state.scores.append(False)
                    st.error(f"❌ 오답이에요! 정답은 {result}입니다.")
                
                st.session_state.current_problem += 1
                st.session_state.current_stage = 0
                st.session_state.answers = [None, None, None]
                
                # 모든 문제를 풀었으면 결과 화면으로 이동
                if st.session_state.current_problem >= len(st.session_state.problems):
                    st.session_state.page = "result"
                
                st.rerun()

def show_result():
    """결과 확인 화면"""
    st.markdown("# 🏆 연습 완료!")
    
    total = len(st.session_state.scores)
    correct = sum(st.session_state.scores)
    percentage = (correct / total * 100) if total > 0 else 0
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 성적")
        st.metric("정답률", f"{percentage:.0f}%")
        st.metric("맞은 문제", f"{correct}/{total}")
    
    with col2:
        st.markdown("### 문제별 결과")
        for i, score in enumerate(st.session_state.scores):
            if score:
                st.success(f"문제 {i+1}: ✅ 정답")
            else:
                st.error(f"문제 {i+1}: ❌ 오답")
    
    st.divider()
    
    if percentage == 100:
        st.balloons()
        st.markdown("### 🌟 완벽해요! 정말 잘했어요!")
    elif percentage >= 80:
        st.markdown("### 😊 좋아요! 거의 다 맞았어요!")
    else:
        st.markdown("### 💪 다시 한 번 도전해볼까요?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 다시 풀기", use_container_width=True, key="retry_btn"):
            st.session_state.current_problem = 0
            st.session_state.current_stage = 0
            st.session_state.answers = [None, None, None]
            st.session_state.scores = []
            st.session_state.problems = generate_problems(st.session_state.difficulty, 5)
            st.session_state.page = "practice"
            st.rerun()
    
    with col2:
        if st.button("🏠 홈으로 돌아가기", use_container_width=True, key="home_btn"):
            st.session_state.page = "home"
            st.session_state.difficulty = None
            st.session_state.current_problem = 0
            st.session_state.current_stage = 0
            st.session_state.answers = [None, None, None]
            st.session_state.scores = []
            st.rerun()

# 페이지 라우팅
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "learn":
    show_learn()
elif st.session_state.page == "practice":
    show_practice()
elif st.session_state.page == "result":
    show_result()
