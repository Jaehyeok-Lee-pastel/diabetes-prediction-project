import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.family"]=["Malgun Gothic"]
plt.rcParams["axes.unicode_minus"] = False

# ------------------------
# 설정
# ------------------------
st.set_page_config(page_title="혈당 예측 대시보드", layout="wide")
st.title("🩸 혈당 예측 대시보드")

# ------------------------
# 사이드바 메뉴
# ------------------------
st.sidebar.title("📋 메뉴")
page = st.sidebar.selectbox("페이지 선택", ["예측", "데이터 분석", "모델 평가", "도움말"])

# ------------------------
# 선형 회귀 방정식 함수
# ------------------------
def calculate_diabetes_risk(glucose):
    """
    선형 회귀 방정식을 사용하여 당뇨병 위험도 계산
    당뇨병 위험도 = -0.6422 + 0.0081 * 혈당수치
    """
    risk_score = -0.6422 + 0.0081 * glucose
    return risk_score

# ------------------------
# 페이지: 예측
# ------------------------
if page == "예측":
    st.header("🔍 실시간 혈당 예측")

    # 사용자 입력
    glucose = st.slider("혈당 수치 (mg/dL)", min_value=50, max_value=200, step=1, value=100)

    if st.button("예측 실행"):
        # 선형 회귀 방정식을 사용한 당뇨병 위험도 계산
        risk_score = calculate_diabetes_risk(glucose)
        
        # 결과 표시
        st.subheader("📊 선형 회귀 예측 결과")
        st.metric(
            label="당뇨병 위험도 점수", 
            value=f"{risk_score:.4f}"
        )
        
        # 위험도 점수 해석
        if risk_score < -0.2:
            st.success("🟢 당뇨병 위험도: 낮음")
            st.info("위험도 점수가 낮습니다. 현재 혈당 수치는 양호한 편입니다.")
        elif risk_score < 0.2:
            st.warning("🟡 당뇨병 위험도: 보통")
            st.info("위험도 점수가 보통입니다. 지속적인 관리가 필요합니다.")
        elif risk_score < 0.6:
            st.warning("🟠 당뇨병 위험도: 높음")
            st.info("위험도 점수가 높습니다. 전문의 상담을 권장합니다.")
        else:
            st.error("🔴 당뇨병 위험도: 매우 높음")
            st.info("위험도 점수가 매우 높습니다. 즉시 전문의 상담을 받으시기 바랍니다.")
        
        # 회귀 방정식 설명
        st.subheader("📈 회귀 방정식 상세")
        st.info(f"""
        **사용된 선형 회귀 방정식:**
        
        당뇨병 위험도 = -0.6422 + 0.0081 × {glucose}
        
        **계산 과정:**
        - 기본값: -0.6422
        - 혈당 효과: 0.0081 × {glucose} = {0.0081 * glucose:.4f}
        - **최종 위험도: {risk_score:.4f}**
        
        **해석:**
        - 혈당이 1mg/dL 증가할 때마다 위험도가 0.0081 증가합니다.
        - 위험도 0을 기준으로 음수면 낮은 위험, 양수면 높은 위험을 의미합니다.
        """)
        
        # 시각화: 혈당 수치에 따른 위험도 변화
        st.subheader("📊 혈당 수치별 위험도 변화")
        glucose_range = np.linspace(50, 200, 150)
        risk_range = [calculate_diabetes_risk(g) for g in glucose_range]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(glucose_range, risk_range, 'b-', linewidth=3, label='당뇨병 위험도')
        ax.axhline(0, color='black', linestyle='-', alpha=0.3, label='위험도 기준선 (0)')
        ax.axvline(glucose, color='red', linestyle='--', alpha=0.8, linewidth=2, 
                  label=f'현재 입력값: {glucose} mg/dL')
        ax.axhline(risk_score, color='red', linestyle='--', alpha=0.8, linewidth=2,
                  label=f'현재 위험도: {risk_score:.4f}')
        
        # 참고 구간 표시
        ax.axvspan(50, 100, alpha=0.1, color='green', label='정상 구간')
        ax.axvspan(100, 126, alpha=0.1, color='orange', label='전당뇨 구간')
        ax.axvspan(126, 200, alpha=0.1, color='red', label='당뇨 구간')
        
        # 위험도 구간 표시
        ax.axhspan(-1, -0.2, alpha=0.1, color='green')
        ax.axhspan(-0.2, 0.2, alpha=0.1, color='yellow')
        ax.axhspan(0.2, 0.6, alpha=0.1, color='orange')
        ax.axhspan(0.6, 1.5, alpha=0.1, color='red')
        
        ax.set_xlabel('혈당 수치 (mg/dL)', fontsize=12)
        ax.set_ylabel('당뇨병 위험도 점수', fontsize=12)
        ax.set_title('혈당 수치에 따른 당뇨병 위험도 예측', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # y축 범위 설정
        ax.set_ylim(-1, 1.2)
        
        st.pyplot(fig, use_container_width=True)
        
        # 추가 정보
        st.subheader("📋 위험도 점수 해석 기준")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            **🟢 낮음**
            - 점수: < -0.2
            - 혈당: ~75mg/dL 이하
            - 상태: 양호
            """)
        
        with col2:
            st.markdown("""
            **🟡 보통**
            - 점수: -0.2 ~ 0.2
            - 혈당: ~75-105mg/dL
            - 상태: 주의 관찰
            """)
        
        with col3:
            st.markdown("""
            **🟠 높음**
            - 점수: 0.2 ~ 0.6
            - 혈당: ~105-155mg/dL
            - 상태: 관리 필요
            """)
        
        with col4:
            st.markdown("""
            **🔴 매우 높음**
            - 점수: > 0.6
            - 혈당: ~155mg/dL 이상
            - 상태: 즉시 상담
            """)

# ------------------------
# 페이지: 데이터 분석
# ------------------------
elif page == "데이터 분석":
    st.header("📊 데이터 시각화 분석")
    
    # 샘플 데이터 생성 (실제 데이터가 없는 경우를 대비)
    try:
        df = pd.read_csv("data/processed.csv")
    except:
        # 샘플 데이터 생성
        np.random.seed(42)
        n_samples = 500
        glucose_normal = np.random.normal(85, 10, n_samples//3)
        glucose_prediabetes = np.random.normal(110, 8, n_samples//3)
        glucose_diabetes = np.random.normal(150, 15, n_samples//3)
        
        glucose_data = np.concatenate([glucose_normal, glucose_prediabetes, glucose_diabetes])
        glucose_data = np.clip(glucose_data, 50, 200)  # 50-200 범위로 제한
        
        outcome = np.concatenate([
            np.zeros(n_samples//3), 
            np.random.binomial(1, 0.3, n_samples//3),
            np.ones(n_samples//3)
        ])
        
        df = pd.DataFrame({
            'Glucose': glucose_data,
            'Outcome': outcome
        })
        st.info("💡 실제 데이터를 찾을 수 없어 시연용 샘플 데이터를 사용합니다.")

    # 혈당 분포 히스토그램
    st.subheader("🔹 혈당 분포 (히스토그램)")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.histplot(df["Glucose"], bins=30, ax=ax1, kde=True, alpha=0.7)
    ax1.axvline(100, color='green', linestyle='--', linewidth=2, label='정상 상한선 (100)')
    ax1.axvline(126, color='red', linestyle='--', linewidth=2, label='당뇨 기준선 (126)')
    ax1.set_xlabel('혈당 수치 (mg/dL)')
    ax1.set_ylabel('빈도')
    ax1.set_title('혈당 수치 분포')
    ax1.legend()
    st.pyplot(fig1, use_container_width=True)
    
    # 선형 회귀 기반 위험도 분포
    st.subheader("🔹 선형 회귀 기반 위험도 점수 분포")
    df['Risk_Score'] = df['Glucose'].apply(calculate_diabetes_risk)
    
    fig2, (ax2, ax3) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 위험도 점수 히스토그램
    sns.histplot(df['Risk_Score'], bins=30, ax=ax2, kde=True, alpha=0.7, color='skyblue')
    ax2.axvline(0, color='black', linestyle='-', alpha=0.5, label='위험도 기준선 (0)')
    ax2.axvline(-0.2, color='green', linestyle='--', alpha=0.7, label='낮음 기준')
    ax2.axvline(0.2, color='orange', linestyle='--', alpha=0.7, label='높음 기준')
    ax2.axvline(0.6, color='red', linestyle='--', alpha=0.7, label='매우 높음 기준')
    ax2.set_xlabel('위험도 점수')
    ax2.set_ylabel('빈도')
    ax2.set_title('위험도 점수 분포')
    ax2.legend()
    
    # 혈당 vs 위험도 산점도
    colors = df['Outcome'].map({0: 'blue', 1: 'red'})
    ax3.scatter(df['Glucose'], df['Risk_Score'], c=colors, alpha=0.6)
    
    # 회귀선 그리기
    glucose_line = np.linspace(50, 200, 100)
    risk_line = [calculate_diabetes_risk(g) for g in glucose_line]
    ax3.plot(glucose_line, risk_line, 'black', linewidth=2, label='회귀선')
    
    ax3.axhline(0, color='black', linestyle='-', alpha=0.3)
    ax3.axvline(100, color='green', linestyle='--', alpha=0.5)
    ax3.axvline(126, color='red', linestyle='--', alpha=0.5)
    ax3.set_xlabel('혈당 수치 (mg/dL)')
    ax3.set_ylabel('위험도 점수')
    ax3.set_title('혈당 수치 vs 위험도 점수')
    ax3.legend(['회귀선', '정상인', '당뇨환자'])
    
    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    
    # 통계 요약
    st.subheader("🔹 통계 요약")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**혈당 수치 통계**")
        st.write(f"- 평균: {df['Glucose'].mean():.1f} mg/dL")
        st.write(f"- 표준편차: {df['Glucose'].std():.1f} mg/dL")
        st.write(f"- 최솟값: {df['Glucose'].min():.1f} mg/dL")
        st.write(f"- 최댓값: {df['Glucose'].max():.1f} mg/dL")
    
    with col2:
        st.write("**위험도 점수 통계**")
        st.write(f"- 평균: {df['Risk_Score'].mean():.4f}")
        st.write(f"- 표준편차: {df['Risk_Score'].std():.4f}")
        st.write(f"- 최솟값: {df['Risk_Score'].min():.4f}")
        st.write(f"- 최댓값: {df['Risk_Score'].max():.4f}")

# ------------------------
# 페이지: 모델 평가
# ------------------------
elif page == "모델 평가":
    st.header("📈 선형 회귀 모델 평가")

    st.subheader("🔹 회귀 방정식 정보")
    st.info("""
    **사용된 선형 회귀 방정식:**
    당뇨병 위험도 = -0.6422 + 0.0081 × 혈당수치
    
    **계수 해석:**
    - **절편 (-0.6422)**: 혈당이 0일 때의 기본 위험도 (이론적 값)
    - **기울기 (0.0081)**: 혈당이 1mg/dL 증가할 때마다 위험도 0.0081 증가
    - **零점 혈당**: 위험도가 0이 되는 혈당 = 0.6422 ÷ 0.0081 ≈ 79.3 mg/dL
    """)
    
    # 혈당 범위별 위험도 분석
    st.subheader("🔹 혈당 범위별 위험도 분석")
    glucose_ranges = [
        ("매우 낮음 (50-70 mg/dL)", 50, 70),
        ("정상 (70-99 mg/dL)", 70, 99),
        ("경계 (100-125 mg/dL)", 100, 125), 
        ("높음 (126-140 mg/dL)", 126, 140),
        ("매우 높음 (141-200 mg/dL)", 141, 200)
    ]
    
    analysis_data = []
    for name, min_val, max_val in glucose_ranges:
        min_risk = calculate_diabetes_risk(min_val)
        max_risk = calculate_diabetes_risk(max_val)
        avg_glucose = (min_val + max_val) / 2
        avg_risk = calculate_diabetes_risk(avg_glucose)
        
        analysis_data.append({
            '구간': name,
            '최소 위험도': f"{min_risk:.4f}",
            '평균 위험도': f"{avg_risk:.4f}",
            '최대 위험도': f"{max_risk:.4f}"
        })
        
        st.write(f"**{name}**")
        col1, col2, col3 = st.columns(3)
        col1.metric(f"최소 ({min_val}mg/dL)", f"{min_risk:.4f}")
        col2.metric(f"평균 ({avg_glucose:.0f}mg/dL)", f"{avg_risk:.4f}")
        col3.metric(f"최대 ({max_val}mg/dL)", f"{max_risk:.4f}")
        st.write("")
    
    # 분석 결과를 DataFrame으로 표시
    analysis_df = pd.DataFrame(analysis_data)
    st.dataframe(analysis_df, use_container_width=True)
    
    # 민감도 분석
    st.subheader("🔹 민감도 분석")
    glucose_values = [60, 80, 100, 120, 140, 160, 180, 200]
    risk_scores = [calculate_diabetes_risk(g) for g in glucose_values]
    
    # 민감도 분석 시각화
    fig_sens, ax_sens = plt.subplots(figsize=(12, 6))
    
    # 막대 그래프로 표시
    bars = ax_sens.bar(glucose_values, risk_scores, alpha=0.7, color='steelblue', width=8)
    
    # 각 막대 위에 값 표시
    for bar, risk in zip(bars, risk_scores):
        height = bar.get_height()
        ax_sens.text(bar.get_x() + bar.get_width()/2., height + 0.01 if height > 0 else height - 0.03,
                    f'{risk:.3f}', ha='center', va='bottom' if height > 0 else 'top', fontweight='bold')
    
    # 기준선 추가
    ax_sens.axhline(0, color='black', linestyle='-', alpha=0.5, label='위험도 기준선')
    ax_sens.axhline(-0.2, color='green', linestyle='--', alpha=0.7, label='낮음 기준')
    ax_sens.axhline(0.2, color='orange', linestyle='--', alpha=0.7, label='높음 기준')
    ax_sens.axhline(0.6, color='red', linestyle='--', alpha=0.7, label='매우 높음 기준')
    
    ax_sens.set_xlabel('혈당 수치 (mg/dL)', fontsize=12)
    ax_sens.set_ylabel('위험도 점수', fontsize=12)
    ax_sens.set_title('혈당 수치별 위험도 점수', fontsize=14, fontweight='bold')
    ax_sens.legend()
    ax_sens.grid(True, alpha=0.3)
    
    st.pyplot(fig_sens, use_container_width=True)
    
    # 민감도 분석 표
    sensitivity_df = pd.DataFrame({
        '혈당 수치 (mg/dL)': glucose_values,
        '위험도 점수': [f"{r:.4f}" for r in risk_scores],
        '위험 수준': [
            '낮음' if r < -0.2 else 
            '보통' if r < 0.2 else 
            '높음' if r < 0.6 else 
            '매우 높음' for r in risk_scores
        ]
    })
    
    st.dataframe(sensitivity_df, use_container_width=True)

# ------------------------
# 페이지: 도움말
# ------------------------
elif page == "도움말":
    st.header("ℹ️ 사용자 가이드 및 정보")
    st.markdown("""
    ### 🛠 사용 방법 안내
    - 좌측 사이드바에서 **예측 / 데이터 분석 / 모델 평가 / 도움말** 메뉴를 선택합니다.
    - **예측**: 혈당 수치를 입력하여 당뇨병 위험도를 예측합니다.
    - **데이터 분석**: 혈당 데이터의 분포와 위험도 점수를 시각화합니다.
    - **모델 평가**: 선형 회귀 모델의 성능과 민감도를 분석합니다.
    - **도움말**: 프로젝트 및 앱 사용법에 대한 안내를 제공합니다.
    
    ### 📊 선형 회귀 방정식 정보
    **사용된 선형 회귀 방정식:**
    ```
    당뇨병 위험도 = -0.6422 + 0.0081 × 혈당수치
    ```
    
    **특징:**
    - **선형 관계**: 혈당과 위험도 사이의 직선적 관계를 모델링
    - **해석 용이성**: 혈당 1mg/dL 증가 시 위험도 0.0081 증가
    - **범위**: 혈당 50-200mg/dL로 제한하여 현실적 범위 내에서 예측
    - **기준점**: 위험도 0을 중심으로 음수는 낮은 위험, 양수는 높은 위험
    
    ### 🎯 위험도 점수 해석
    - **🟢 낮음 (< -0.2)**: 현재 혈당 수치는 양호한 편입니다.
    - **🟡 보통 (-0.2 ~ 0.2)**: 지속적인 관리와 모니터링이 필요합니다.
    - **🟠 높음 (0.2 ~ 0.6)**: 생활습관 개선과 전문의 상담을 권장합니다.
    - **🔴 매우 높음 (> 0.6)**: 즉시 전문의 상담을 받으시기 바랍니다.
    
    ### 📈 혈당 수치 기준 (의학적 참고)
    - **정상**: 70-99mg/dL
    - **경계성 (전당뇨)**: 100-125mg/dL
    - **당뇨**: 126mg/dL 이상
    - **저혈당**: 70mg/dL 미만
    
    ### 💡 참고 사항
    - 혈당 수치만을 입력하여 위험도를 예측하는 단순 모델입니다.
    - 본 앱은 의료 진단용이 아닌 **교육 및 연구용**입니다.
    - 실제 당뇨병 진단은 반드시 전문의의 종합적 판단이 필요합니다.
    - 선형 회귀 모델의 특성상 극값에서는 예측 정확도가 떨어질 수 있습니다.
    
    ### 🔧 기술적 정보
    - **모델 유형**: 선형 회귀 (Linear Regression)
    - **입력 변수**: 혈당 수치 (mg/dL)
    - **출력 변수**: 당뇨병 위험도 점수
    - **혈당 범위**: 50-200 mg/dL
    - **프레임워크**: Streamlit, NumPy, Matplotlib, Seaborn
    """)