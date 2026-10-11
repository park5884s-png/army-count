from datetime import datetime
import streamlit as st
import time

# ---------------------------------------------------------
# 페이지 설정 (와이드 모드)
# ---------------------------------------------------------
st.set_page_config(
    page_title="실시간 친구들 전역율 대시보드", page_icon="🪖", layout="wide"
)

# ---------------------------------------------------------
# 친구들 복무 정보 데이터
# ---------------------------------------------------------
friends = [
    {
        "name": "오진규",
        "enlistment": "2025-04-28",
        "discharge": "2026-10-27",
        "branch": "해병",
    },
    {
        "name": "정지우",
        "enlistment": "2025-09-29",
        "discharge": "2027-03-28",
        "branch": "육군",
    },
    {
        "name": "호영",
        "enlistment": "2026-04-07",
        "discharge": "2027-10-06",
        "branch": "육군",
    },
    {
        "name": "신만수",
        "enlistment": "2026-05-11",
        "discharge": "2027-11-10",
        "branch": "육군",
    },
    {
        "name": "나시원",
        "enlistment": "2026-05-18",
        "discharge": "2027-11-17",
        "branch": "육군",
    },
    {
        "name": "윤명호",
        "enlistment": "2026-05-25",
        "discharge": "2027-11-25",
        "branch": "육군",
    },
    {
        "name": "강유민",
        "enlistment": "2026-06-08",
        "discharge": "2027-12-07",
        "branch": "육군",
    },
    {
        "name": "함영현",
        "enlistment": "2026-06-08",
        "discharge": "2027-12-07",
        "branch": "육군",
    },
    {
        "name": "박동순",
        "enlistment": "2026-06-15",
        "discharge": "2027-12-14",
        "branch": "육군",
    },
    {
        "name": "이진우",
        "enlistment": "2026-06-22",
        "discharge": "2028-03-21",
        "branch": "공군",
    },
    {
        "name": "정지율",
        "enlistment": "2026-07-27",
        "discharge": "2028-01-26",
        "branch": "육군",
    },
    {
        "name": "김광진",
        "enlistment": "2026-08-10",
        "discharge": "2028-02-09",
        "branch": "육군",
    },
    {
        "name": "한준형",
        "enlistment": "2026-08-18",
        "discharge": "2028-02-17",
        "branch": "육군",
    },
    {
        "name": "양동규",
        "enlistment": "2026-09-28",
        "discharge": "2028-03-27",
        "branch": "육군",
    },
    {
        "name": "조민석",
        "enlistment": "2026-10-06",
        "discharge": "2028-04-05",
        "branch": "육군",
    },
    {
        "name": "방성배",
        "enlistment": "2026-10-13",
        "discharge": "2028-04-12",
        "branch": "상근",
    },
    {
        "name": "엄희성",
        "enlistment": "2026-10-19",
        "discharge": "2028-04-18",
        "branch": "육군",
    },
    {
        "name": "권유신",
        "enlistment": "2026-12-01",
        "discharge": "2028-06-01",
        "branch": "육군",
    },
]


# ---------------------------------------------------------
# 전역율 및 D-day 계산 함수 (47,347,200초 기준)
# ---------------------------------------------------------
def calculate_status(enlistment_str, discharge_str):
  fmt = "%Y-%m-%d"
  enlistment = datetime.strptime(enlistment_str, fmt)
  discharge = datetime.strptime(discharge_str, fmt)
  now = datetime.now()

  total_seconds = 47347200.0  # 548일 기준 고정 (47,347,200초 = 100%)
  elapsed_seconds = (now - enlistment).total_seconds()

  d_day_delta = (discharge.date() - now.date()).days
  if d_day_delta > 0:
    d_day_str = f"D-{d_day_delta}"
  elif d_day_delta == 0:
    d_day_str = "D-DAY 🎉"
  else:
    d_day_str = "전역 완료"

  actual_total_seconds = (discharge - enlistment).total_seconds()
  months = round(actual_total_seconds / (30.4375 * 24 * 3600))

  if elapsed_seconds < 0:
    return 0.0, "입대 대기", f"{months}개월", "입대 전"
  if elapsed_seconds >= total_seconds:
    return 100.0, "전역 완료", f"{months}개월", d_day_str

  rate = (elapsed_seconds / total_seconds) * 100
  return max(0.0, min(100.0, rate)), "복무 중", f"{months}개월", d_day_str


# ---------------------------------------------------------
# 웹 UI 구성
# ---------------------------------------------------------
st.title("🪖 친구들 실시간 군 복무 전역율 대시보드")
st.markdown("---")

placeholder = st.empty()

try:
  while True:
    with placeholder.container():
      now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      st.caption(f"🕒 현재 시간: {now_str} (1초마다 자동 갱신 중)")

      table_data = []
      for friend in friends:
        rate, status, service_months, d_day_str = calculate_status(
            friend["enlistment"], friend["discharge"]
        )
        table_data.append({
            "이름": friend["name"],
            "전역율": f"{rate:9.7f}%",
            "상태": status,
            "D-day": d_day_str,
            "전역일": friend["discharge"],
            "복무 개월 수": service_months,
            "군종": friend["branch"],
        })

      st.dataframe(table_data, use_container_width=True, hide_index=True)

      st.markdown("### 📊 실시간 진행 게이지")
      for friend in friends:
        rate, status, _, d_day_str = calculate_status(
            friend["enlistment"], friend["discharge"]
        )
        col1, col2, col3 = st.columns([1, 6, 2])
        with col1:
          st.text(f"{friend['name']} ({friend['branch']})")
        with col2:
          st.progress(float(rate / 100.0))
        with col3:
          st.text(f"{rate:6.4f}% ({d_day_str})")

    time.sleep(1)
    st.rerun()

except Exception as e:
  st.write("대시보드가 종료되었습니다.")
