"""
pages/community.py — Community User mode for WePet MVP.
Daily 1-minute climate-help task for street animals.
"""
import streamlit as st
from datetime import datetime

from services.weather_service import get_weather_for_location
from services.risk_engine import compute_community_heat_score
from services.citizen_task_engine import select_task, get_best_task_time
from services.storage_service import log_task_completion, get_total_points, get_streak_days
from components.styles import RISK_COLORS, RISK_BG
from components.ui import (
    render_page_header,
    render_section_label,
    render_weather_metric,
    render_error_banner,
    render_info_banner,
)


def _render_heat_badge(level: str, score: float):
    color = RISK_COLORS.get(level, "#94a3b8")
    bg = RISK_BG.get(level, "rgba(148,163,184,0.1)")
    icons = {"Low": "🟢", "Moderate": "🟡", "High": "🟠", "Critical": "🔴"}
    icon = icons.get(level, "⚪")
    st.markdown(
        f"""
        <div style="background:{bg};border:1px solid {color}40;border-radius:12px;
             padding:14px 20px;display:inline-flex;align-items:center;gap:12px;margin-bottom:16px;">
            <span style="font-size:1.6rem;">{icon}</span>
            <div>
                <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;
                     color:#64748b;font-weight:600;">Community Heat Level</div>
                <div style="font-size:1.3rem;font-weight:700;color:{color};line-height:1.1;">
                    {level} <span style="font-size:0.85rem;font-weight:400;color:#64748b;">
                    ({score:.0f}/100)</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_task_card(task: dict, best_time: str):
    st.markdown(
        f"""
        <div class="task-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;
                 margin-bottom:14px;flex-wrap:wrap;gap:8px;">
                <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;
                     color:#63b3ed;font-weight:600;">TODAY'S TASK</div>
                <span class="points-badge">+{task.get('points', 10)} pts &nbsp;·&nbsp;
                    ⏱ {task.get('effort', '1 min')}</span>
            </div>
            <div style="font-size:1.1rem;font-weight:600;color:#f1f5f9;
                 line-height:1.5;margin-bottom:10px;">
                {task.get('task', '')}
            </div>
            <div style="font-size:0.85rem;color:#94a3b8;line-height:1.6;margin-bottom:14px;">
                <strong style="color:#64748b;">Why it matters:</strong>
                {task.get('why', '')}
            </div>
            <div style="font-size:0.82rem;color:#63b3ed;border-top:1px solid rgba(255,255,255,0.06);
                 padding-top:12px;margin-top:4px;">
                {best_time}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_stats(points: int, streak: int):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size:1.2rem;margin-bottom:4px;">⭐</div>
                <div class="metric-value">{points}</div>
                <div class="metric-label">Total Points</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size:1.2rem;margin-bottom:4px;">🔥</div>
                <div class="metric-value">{streak}</div>
                <div class="metric-label">Day Streak</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render():
    render_page_header(
        title="Community",
        subtitle="One small action a day makes a real difference for animals in your city.",
        icon="🤝",
    )

    # ── Location Input ────────────────────────────────────────────────────────
    col_input, col_main = st.columns([1, 2], gap="large")

    with col_input:
        render_section_label("📍 YOUR LOCATION")
        location = st.text_input(
            "City / Area",
            placeholder="e.g. Pune, Chennai, Hyderabad",
            key="comm_location",
        )
        fetch = st.button(
            "🌤️ Get Today's Task",
            use_container_width=True,
            key="comm_fetch",
        )

        # Stats panel
        render_section_label("🏆 YOUR IMPACT")
        total_pts = get_total_points()
        streak = get_streak_days()
        _render_stats(total_pts, streak)

        st.markdown(
            """
            <div style="margin-top:12px;font-size:0.78rem;color:#475569;line-height:1.6;
                 padding:10px 14px;background:rgba(255,255,255,0.03);border-radius:8px;">
                💡 Tasks are chosen daily based on live heat conditions.
                Each completion helps street animals survive the heat.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Fetch Task on Button Click ─────────────────────────────────────────────
    if fetch:
        if not location.strip():
            with col_input:
                render_error_banner("Please enter your city to continue.")
        else:
            with col_main:
                with st.spinner("Checking today's conditions…"):
                    weather_data = get_weather_for_location(location.strip())

            if "error" in weather_data:
                with col_main:
                    render_error_banner(
                        f"Could not fetch weather: {weather_data['error']}"
                    )
            else:
                current = weather_data["current"]
                heat_data = compute_community_heat_score(current)
                heat_level = heat_data["level"]
                heat_score = heat_data["score"]

                task = select_task(heat_level)
                current_hour = datetime.now().hour
                best_time = get_best_task_time(current_hour)

                st.session_state["comm_data"] = {
                    "current": current,
                    "location_display": weather_data["location"]["display"],
                    "heat_level": heat_level,
                    "heat_score": heat_score,
                    "task": task,
                    "best_time": best_time,
                    "location_raw": location.strip(),
                    "completed": False,
                }

    # ── Render Task Area ───────────────────────────────────────────────────────
    comm = st.session_state.get("comm_data")

    with col_main:
        if not comm:
            st.markdown(
                """
                <div style="display:flex;flex-direction:column;align-items:center;
                     justify-content:center;height:280px;gap:12px;">
                    <div style="font-size:3rem;opacity:0.3;">🤝</div>
                    <div style="color:#475569;font-size:0.95rem;text-align:center;
                         max-width:280px;line-height:1.6;">
                        Enter your location and click
                        <strong style="color:#64748b;">Get Today's Task</strong>
                        to see how you can help today.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        current = comm["current"]

        # Mini weather row
        render_section_label("🌡️ CONDITIONS IN " + comm["location_display"].upper())
        w_cols = st.columns(4)
        with w_cols[0]:
            render_weather_metric(
                "Temperature", f"{current['temperature']:.1f}", "°C", "🌡️"
            )
        with w_cols[1]:
            render_weather_metric(
                "Feels Like", f"{current['apparent_temperature']:.1f}", "°C", "🤔"
            )
        with w_cols[2]:
            render_weather_metric(
                "Humidity", f"{current['humidity']:.0f}", "%", "💧"
            )
        with w_cols[3]:
            render_weather_metric(
                "UV Index", f"{current.get('uv_index', 0) or 0:.0f}", "", "☀️"
            )

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

        # Heat level badge
        _render_heat_badge(comm["heat_level"], comm["heat_score"])

        # Task card
        _render_task_card(comm["task"], comm["best_time"])

        # Completion flow
        if not comm.get("completed"):
            complete = st.button(
                "✅ I completed this task!",
                use_container_width=True,
                key="comm_complete",
            )
            if complete:
                task = comm["task"]
                entry = log_task_completion(
                    task_id=task.get("id", "default"),
                    task_text=task.get("task", ""),
                    points=task.get("points", 10),
                    location=comm["location_raw"],
                )
                st.session_state["comm_data"]["completed"] = True
                st.rerun()
        else:
            task = comm["task"]
            pts_earned = task.get("points", 10)
            new_total = get_total_points()
            new_streak = get_streak_days()

            st.markdown(
                f"""
                <div style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.25);
                     border-radius:14px;padding:20px 24px;text-align:center;margin-bottom:16px;">
                    <div style="font-size:2rem;margin-bottom:8px;">🎉</div>
                    <div style="font-size:1.05rem;font-weight:600;color:#4ade80;margin-bottom:6px;">
                        Task complete! +{pts_earned} points earned.
                    </div>
                    <div style="font-size:0.85rem;color:#64748b;">
                        Every action you take makes a real difference for animals nearby.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            _render_stats(new_total, new_streak)