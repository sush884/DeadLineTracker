import streamlit as st
from datetime import datetime, timedelta

from database import (
    create_table,
    add_deadline,
    get_deadlines,
    delete_deadline,
    mark_completed,
    update_deadline
)

from utils import (
    get_deadline_status,
    get_reminder_message,
    get_priority_icon
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Deadline Tracker",
    page_icon="📅",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    color: #111827;
}

h2 {
    color: #1f2937;
}

h3 {
    color: #374151;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}

div[data-testid="stForm"] {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

create_table()

deadlines = get_deadlines()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📅 Deadline Tracker")

st.sidebar.caption(
    "Stay organized. Never miss a deadline."
)

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "➕ Add Deadline",
        "📋 All Deadlines",
        "🗓️ Calendar",
        "✅ Completed"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "💡 Tip: Add your assignments, "
    "projects, exams and important tasks here."
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    "<h1>📅 Deadline Tracker</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        font-size:18px;
        color:#6b7280;
        margin-top:-10px;
    ">
    Track assignments, projects, exams and important deadlines
    in one simple dashboard.
    </p>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.header("📊 Dashboard")

    total_deadlines = len(deadlines)

    completed_deadlines = sum(
        1
        for deadline in deadlines
        if deadline[7] == "Completed"
    )

    pending_deadlines = sum(
        1
        for deadline in deadlines
        if deadline[7] == "Pending"
    )

    overdue_deadlines = 0
    today_deadlines = 0

    for deadline in deadlines:

        deadline_status, _ = get_deadline_status(
            deadline[4],
            deadline[5],
            deadline[7]
        )

        if deadline_status == "Overdue":
            overdue_deadlines += 1

        if deadline_status == "Due today":
            today_deadlines += 1


    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "📋 Total",
            total_deadlines
        )

    with col2:
        st.metric(
            "⏳ Pending",
            pending_deadlines
        )

    with col3:
        st.metric(
            "✅ Completed",
            completed_deadlines
        )

    with col4:
        st.metric(
            "🔴 Overdue",
            overdue_deadlines
        )

    with col5:
        st.metric(
            "🟠 Due Today",
            today_deadlines
        )


    # -----------------------------------------------------
    # PROGRESS
    # -----------------------------------------------------

    st.divider()

    st.subheader("📈 Completion Progress")

    if total_deadlines > 0:

        completion_percentage = (
            completed_deadlines /
            total_deadlines
        )

    else:

        completion_percentage = 0


    st.progress(
        completion_percentage
    )

    st.write(
        f"**{completed_deadlines} / "
        f"{total_deadlines} deadlines completed "
        f"({completion_percentage * 100:.0f}%)**"
    )


    # -----------------------------------------------------
    # QUICK VIEW
    # -----------------------------------------------------

    st.divider()

    st.subheader("📌 Quick View")

    quick_view = st.selectbox(
        "Show deadlines",
        [
            "Today",
            "This Week",
            "Upcoming"
        ]
    )

    today = datetime.now().date()

    if quick_view == "Today":

        start_date = today
        end_date = today

    elif quick_view == "This Week":

        start_date = today
        end_date = today + timedelta(days=7)

    else:

        start_date = today + timedelta(days=1)
        end_date = today + timedelta(days=30)


    quick_deadlines = []

    for deadline in deadlines:

        due_date = datetime.strptime(
            deadline[4],
            "%Y-%m-%d"
        ).date()

        if start_date <= due_date <= end_date:

            quick_deadlines.append(
                deadline
            )


    if not quick_deadlines:

        st.info(
            "No deadlines found for this period. 🎉"
        )

    else:

        for deadline in quick_deadlines:

            (
                deadline_id,
                title,
                subject,
                description,
                due_date,
                due_time,
                priority,
                status,
                created_at
            ) = deadline

            with st.container(border=True):

                st.subheader(
                    f"{get_priority_icon(priority)} {title}"
                )

                st.write(
                    f"📚 **Subject:** {subject}"
                )

                st.write(
                    f"📅 **Due:** {due_date}"
                )

                st.write(
                    f"⏰ **Time:** {due_time}"
                )

                status_text, status_icon = (
                    get_deadline_status(
                        due_date,
                        due_time,
                        status
                    )
                )

                st.write(
                    f"{status_icon} **{status_text}**"
                )


# =========================================================
# ADD DEADLINE
# =========================================================

elif page == "➕ Add Deadline":

    st.header("➕ Add New Deadline")

    st.write(
        "Create a new assignment, project, exam or task."
    )

    with st.form("add_deadline_form"):

        title = st.text_input(
            "Deadline Title",
            placeholder="Example: DBMS Assignment"
        )

        subject = st.text_input(
            "Subject",
            placeholder="Example: DBMS"
        )

        description = st.text_area(
            "Description",
            placeholder="Add additional details..."
        )

        col1, col2 = st.columns(2)

        with col1:

            due_date = st.date_input(
                "📅 Due Date"
            )

        with col2:

            due_time = st.time_input(
                "⏰ Due Time"
            )

        priority = st.selectbox(
            "🔥 Priority",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

        submit = st.form_submit_button(
            "➕ Add Deadline",
            use_container_width=True
        )


        if submit:

            if not title.strip():

                st.error(
                    "Please enter a deadline title."
                )

            elif not subject.strip():

                st.error(
                    "Please enter the subject."
                )

            else:

                add_deadline(
                    title.strip(),
                    subject.strip(),
                    description.strip(),
                    due_date.isoformat(),
                    due_time.strftime("%H:%M"),
                    priority
                )

                st.success(
                    "Deadline added successfully! 🎉"
                )

                st.rerun()


# =========================================================
# ALL DEADLINES
# =========================================================

elif page == "📋 All Deadlines":

    st.header("📋 All Deadlines")

    st.write(
        "Search, filter, sort and manage your deadlines."
    )


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search_text = st.text_input(
        "🔎 Search",
        placeholder="Search by title or subject..."
    )


    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        priority_filter = st.selectbox(
            "🔥 Priority",
            [
                "All",
                "High",
                "Medium",
                "Low"
            ]
        )

    with col2:

        status_filter = st.selectbox(
            "📌 Status",
            [
                "All",
                "Pending",
                "Completed"
            ]
        )

    with col3:

        sort_option = st.selectbox(
            "📅 Sort By",
            [
                "Nearest Deadline",
                "Farthest Deadline",
                "Highest Priority",
                "Lowest Priority"
            ]
        )


    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    filtered_deadlines = []

    for deadline in deadlines:

        (
            deadline_id,
            title,
            subject,
            description,
            due_date,
            due_time,
            priority,
            status,
            created_at
        ) = deadline


        if search_text:

            search_value = search_text.lower()

            if (
                search_value not in title.lower()
                and search_value not in subject.lower()
            ):

                continue


        if priority_filter != "All":

            if priority != priority_filter:

                continue


        if status_filter != "All":

            if status != status_filter:

                continue


        filtered_deadlines.append(
            deadline
        )


    # -----------------------------------------------------
    # SORT
    # -----------------------------------------------------

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }


    if sort_option == "Nearest Deadline":

        filtered_deadlines.sort(
            key=lambda x: (x[4], x[5])
        )


    elif sort_option == "Farthest Deadline":

        filtered_deadlines.sort(
            key=lambda x: (x[4], x[5]),
            reverse=True
        )


    elif sort_option == "Highest Priority":

        filtered_deadlines.sort(
            key=lambda x:
            priority_order.get(
                x[6],
                4
            )
        )


    elif sort_option == "Lowest Priority":

        filtered_deadlines.sort(
            key=lambda x:
            priority_order.get(
                x[6],
                4
            ),
            reverse=True
        )


    st.divider()


    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    if not deadlines:

        st.info(
            "No deadlines added yet. "
            "Go to ➕ Add Deadline."
        )


    elif not filtered_deadlines:

        st.warning(
            "No deadlines match your filters."
        )


    else:

        st.write(
            f"Showing **{len(filtered_deadlines)}** deadline(s)"
        )


        for deadline in filtered_deadlines:

            (
                deadline_id,
                title,
                subject,
                description,
                due_date,
                due_time,
                priority,
                status,
                created_at
            ) = deadline


            with st.container(border=True):

                st.subheader(
                    f"{get_priority_icon(priority)} "
                    f"{title}"
                )

                st.write(
                    f"📚 **Subject:** {subject}"
                )

                if description:

                    st.write(
                        f"📝 {description}"
                    )

                st.write(
                    f"📅 **Due:** {due_date}"
                )

                st.write(
                    f"⏰ **Time:** {due_time}"
                )

                st.write(
                    f"{get_priority_icon(priority)} "
                    f"**Priority:** {priority}"
                )


                deadline_status, status_icon = (
                    get_deadline_status(
                        due_date,
                        due_time,
                        status
                    )
                )

                st.write(
                    f"{status_icon} "
                    f"**{deadline_status}**"
                )


                reminder = get_reminder_message(
                    due_date,
                    due_time,
                    status
                )

                if reminder:

                    st.warning(
                        reminder
                    )


                # -------------------------------------------------
                # ACTION BUTTONS
                # -------------------------------------------------

                col1, col2, col3 = st.columns(3)


                with col1:

                    if status == "Pending":

                        if st.button(
                            "✅ Complete",
                            key=f"complete_{deadline_id}",
                            use_container_width=True
                        ):

                            mark_completed(
                                deadline_id
                            )

                            st.rerun()


                with col2:

                    if st.button(
                        "✏️ Edit",
                        key=f"edit_{deadline_id}",
                        use_container_width=True
                    ):

                        st.session_state[
                            f"edit_{deadline_id}"
                        ] = True


                with col3:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{deadline_id}",
                        use_container_width=True
                    ):

                        delete_deadline(
                            deadline_id
                        )

                        st.rerun()


                # -------------------------------------------------
                # EDIT FORM
                # -------------------------------------------------

                if st.session_state.get(
                    f"edit_{deadline_id}",
                    False
                ):

                    st.write(
                        "### ✏️ Edit Deadline"
                    )

                    with st.form(
                        f"edit_form_{deadline_id}"
                    ):

                        new_title = st.text_input(
                            "Deadline Title",
                            value=title
                        )

                        new_subject = st.text_input(
                            "Subject",
                            value=subject
                        )

                        new_description = st.text_area(
                            "Description",
                            value=description
                        )

                        new_due_date = st.date_input(
                            "Due Date",
                            value=datetime.strptime(
                                due_date,
                                "%Y-%m-%d"
                            ).date()
                        )

                        new_due_time = st.time_input(
                            "Due Time",
                            value=datetime.strptime(
                                due_time,
                                "%H:%M"
                            ).time()
                        )

                        new_priority = st.selectbox(
                            "Priority",
                            [
                                "Low",
                                "Medium",
                                "High"
                            ],
                            index=[
                                "Low",
                                "Medium",
                                "High"
                            ].index(priority)
                        )


                        save_changes = (
                            st.form_submit_button(
                                "💾 Save Changes"
                            )
                        )


                        if save_changes:

                            if not new_title.strip():

                                st.error(
                                    "Title cannot be empty."
                                )

                            elif not new_subject.strip():

                                st.error(
                                    "Subject cannot be empty."
                                )

                            else:

                                update_deadline(
                                    deadline_id,
                                    new_title.strip(),
                                    new_subject.strip(),
                                    new_description.strip(),
                                    new_due_date.isoformat(),
                                    new_due_time.strftime(
                                        "%H:%M"
                                    ),
                                    new_priority
                                )

                                st.session_state[
                                    f"edit_{deadline_id}"
                                ] = False

                                st.success(
                                    "Deadline updated successfully!"
                                )

                                st.rerun()


# =========================================================
# CALENDAR
# =========================================================

elif page == "🗓️ Calendar":

    st.header("🗓️ Calendar View")

    st.write(
        "Select a date to see the deadlines scheduled for that day."
    )

    selected_date = st.date_input(
        "📅 Select Date"
    )

    selected_date_string = (
        selected_date.isoformat()
    )


    calendar_deadlines = [
        deadline
        for deadline in deadlines
        if deadline[4] == selected_date_string
    ]


    if not calendar_deadlines:

        st.info(
            "No deadlines scheduled for this date. 🎉"
        )

    else:

        st.success(
            f"{len(calendar_deadlines)} "
            f"deadline(s) found."
        )


        for deadline in calendar_deadlines:

            (
                deadline_id,
                title,
                subject,
                description,
                due_date,
                due_time,
                priority,
                status,
                created_at
            ) = deadline


            with st.container(border=True):

                st.subheader(
                    f"{get_priority_icon(priority)} "
                    f"{title}"
                )

                st.write(
                    f"📚 **Subject:** {subject}"
                )

                if description:

                    st.write(
                        f"📝 {description}"
                    )

                st.write(
                    f"⏰ **Time:** {due_time}"
                )

                st.write(
                    f"🔥 **Priority:** {priority}"
                )

                st.write(
                    f"📌 **Status:** {status}"
                )


# =========================================================
# COMPLETED
# =========================================================

elif page == "✅ Completed":

    st.header("✅ Completed Deadlines")

    completed_list = [
        deadline
        for deadline in deadlines
        if deadline[7] == "Completed"
    ]


    if not completed_list:

        st.info(
            "No deadlines have been completed yet."
        )

    else:

        st.success(
            f"You have completed "
            f"{len(completed_list)} deadline(s)! 🎉"
        )


        for deadline in completed_list:

            (
                deadline_id,
                title,
                subject,
                description,
                due_date,
                due_time,
                priority,
                status,
                created_at
            ) = deadline


            with st.container(border=True):

                st.subheader(
                    f"✅ {title}"
                )

                st.write(
                    f"📚 **Subject:** {subject}"
                )

                st.write(
                    f"📅 **Due:** {due_date}"
                )

                st.write(
                    f"⏰ **Time:** {due_time}"
                )

                st.write(
                    f"🔥 **Priority:** {priority}"
                )

                st.write(
                    "📌 **Status:** Completed"
                )

                if description:

                    st.write(
                        f"📝 {description}"
                    )