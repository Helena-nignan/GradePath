import joblib
import streamlit as st
import base64

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


st.set_page_config(page_title="Student Achievement Predictor", layout="wide")


def set_bg():
    bg_image = '1 (2).png' 
    with open(bg_image, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: url('data:image/jpg;base64,{encoded}') center center/cover no-repeat !important;
            min-height: 100vh;
        }}
        .centered {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 0;
            text-align: center;
            padding-top: 3rem;
        }}
        .feature-box {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(0,0,0,0.4);
            border-radius: 0.75rem;
            padding: 1rem 2rem;
            margin: 0.5rem;
            color: white;
            font-size: 1.1rem;
            font-weight: 500;
        }}
        .start-btn {{
            margin: 0.75rem 0.5rem;
            padding: 1rem 2rem; 
            border-radius: 1.5rem;
            background: linear-gradient(90deg, #6366f1 0%, #2563eb 100%);
            color: #fff;
            font-size: 1.2rem;
            font-weight: 600;
            box-shadow: 0 8px 32px 0 rgba(49,46,129,0.25), 0 1.5px 8px 0 rgba(49,46,129,0.10);
            border: none;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            outline: none;
            text-decoration: none;
            display: inline-block;
        }}
        .start-btn:hover {{
            background: linear-gradient(90deg, #4f46e5 0%, #1d4ed8 100%);
            box-shadow: 0 12px 36px 0 rgba(49,46,129,0.35), 0 2px 12px 0 rgba(49,46,129,0.15);
            transform: translateY(-2px) scale(1.03);
        }}
        .btn-secondary {{
            background: linear-gradient(90deg, #059669 0%, #047857 100%);
        }}
        .btn-secondary:hover {{
            background: linear-gradient(90deg, #047857 0%, #065f46 100%);
        }}
        .btn-warning {{
            background: linear-gradient(90deg, #d97706 0%, #b45309 100%);
        }}
        .btn-warning:hover {{
            background: linear-gradient(90deg, #b45309 0%, #92400e 100%);
        }}
        .buttons-container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin: 1.5rem 0;
            max-width: 800px;
        }}
        .recommendation-box {{
            background: rgba(255,255,255,0.95);
            border-radius: 1rem;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border-left: 4px solid #6366f1;
            max-width: 900px;
        }}
        .recommendation-title {{
            color: #2563eb;
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }}
        .recommendation-item {{
            background: rgba(99,102,241,0.05);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 0.75rem 0;
            border-left: 3px solid #6366f1;
        }}
        .recommendation-category {{
            font-weight: 600;
            color: #374151;
            margin-bottom: 0.5rem;
        }}
        .recommendation-text {{
            color: #4b5563;
            line-height: 1.6;
        }}
        </style>
    """, unsafe_allow_html=True)


def generate_recommendations(input_dict, prediction):
    """Generate personalized recommendations based on student inputs and predicted grade"""
    recommendations = []
    
    # Grade-based overall assessment
    if prediction < 10:
        grade_level = "At Risk"
        grade_color = "#ef4444"
    elif prediction < 14:
        grade_level = "Needs Improvement"
        grade_color = "#f59e0b"
    elif prediction < 16:
        grade_level = "Good Performance"
        grade_color = "#10b981"
    else:
        grade_level = "Excellent Performance"
        grade_color = "#6366f1"
    
    # Academic Performance Recommendations
    if input_dict['G1'] < 12 or input_dict['G2'] < 12:
        recommendations.append({
            'category': '📚 Academic Performance',
            'text': 'Your previous grades suggest you need to strengthen your study foundation. Consider reviewing past topics and seeking help from teachers or tutors to improve your understanding of core concepts.'
        })
    
    # Study Time Recommendations
    if input_dict['studytime'] <= 2:
        recommendations.append({
            'category': '⏰ Study Habits',
            'text': 'You\'re spending less than 5 hours per week studying. Research shows that increasing study time to 5-10 hours weekly can significantly improve academic performance. Try breaking study sessions into manageable chunks.'
        })
    
    # Attendance Issues
    if input_dict['absences'] > 10:
        recommendations.append({
            'category': '🎯 Attendance',
            'text': f'With {input_dict["absences"]} absences, you\'re missing valuable classroom instruction. Regular attendance is crucial for academic success. Try to minimize absences and catch up on missed material promptly.'
        })
    
    # Alcohol Consumption
    if input_dict['Dalc'] >= 3 or input_dict['Walc'] >= 4:
        recommendations.append({
            'category': '🚨 Health & Lifestyle',
            'text': 'High alcohol consumption can significantly impact academic performance, memory, and concentration. Consider reducing alcohol intake and exploring healthier stress-relief activities like sports or hobbies.'
        })
    
    # Health Issues
    if input_dict['health'] <= 2:
        recommendations.append({
            'category': '💪 Health & Wellness',
            'text': 'Poor health can affect your ability to learn and perform well. Consider consulting a healthcare professional, maintaining a balanced diet, getting regular exercise, and ensuring adequate sleep.'
        })
    
    # Family Support
    if input_dict['famsup'] == 'no':
        recommendations.append({
            'category': '👨‍👩‍👧‍👦 Support System',
            'text': 'Family support plays a crucial role in academic success. Consider having open conversations with family members about your educational goals and seek their encouragement and assistance.'
        })
    
    # Extracurricular Activities
    if input_dict['activities'] == 'no':
        recommendations.append({
            'category': '🎨 Personal Development',
            'text': 'Participating in extracurricular activities can improve social skills, time management, and overall well-being, which often translates to better academic performance. Consider joining clubs or sports teams.'
        })
    
    # Social Life Balance
    if input_dict['goout'] >= 4:
        recommendations.append({
            'category': '⚖️ Work-Life Balance',
            'text': 'While social activities are important, excessive going out might impact study time and academic focus. Try to find a healthy balance between social life and academic responsibilities.'
        })
    
    # Past Failures
    if input_dict['failures'] >= 2:
        recommendations.append({
            'category': '🎯 Academic Recovery',
            'text': 'Having multiple past failures indicates need for academic strategy change. Consider working with a counselor to identify learning challenges, develop better study methods, and create a structured academic plan.'
        })
    
    # Travel Time Impact
    if input_dict['traveltime'] >= 3:
        recommendations.append({
            'category': '🚌 Time Management',
            'text': 'Long commute times can reduce available study time and increase fatigue. Use travel time productively (reading, audio lessons) or consider finding study spaces closer to school.'
        })
    
    # Technology Access
    if input_dict['internet'] == 'no':
        recommendations.append({
            'category': '💻 Educational Resources',
            'text': 'Internet access provides valuable educational resources and research opportunities. Consider accessing internet at libraries, school, or community centers to supplement your learning.'
        })
    
    # Higher Education Aspiration
    if input_dict['higher'] == 'no' and prediction >= 12:
        recommendations.append({
            'category': '🎓 Future Planning',
            'text': 'Your academic potential suggests you could succeed in higher education. Consider exploring post-secondary options, as they can significantly expand career opportunities and earning potential.'
        })
    
    # Positive Reinforcements
    if prediction >= 14:
        recommendations.append({
            'category': '🌟 Keep Up the Great Work',
            'text': 'You\'re performing well academically! Continue your current study habits, maintain a balanced lifestyle, and consider helping peers who might be struggling - teaching others can reinforce your own learning.'
        })
    
    # If no specific issues, general advice
    if len(recommendations) == 0 or (len(recommendations) == 1 and recommendations[0]['category'] == '🌟 Keep Up the Great Work'):
        recommendations.append({
            'category': '📈 Continuous Improvement',
            'text': 'You\'re on a good path! Focus on maintaining consistent study habits, staying organized, and setting specific academic goals. Regular self-assessment and seeking feedback can help you continue improving.'
        })
    
    return recommendations, grade_level, grade_color


st.sidebar.title("GradePath")
if "page" not in st.session_state:
    st.session_state["page"] = "Welcome Page"
page = st.sidebar.radio(
    "Go to:",
    ["Welcome Page", "Predict Performance"],
    index=["Welcome Page", "Predict Performance"].index(st.session_state["page"]),
    key="sidebar_page_radio"
)
st.session_state["page"] = page

if page == "Welcome Page":
    set_bg()

    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.markdown('<h1 style="color:white;font-weight:900;font-size:3rem;text-shadow:2px 2px 8px #000;">Student Achievement Predictor</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:white;font-size:1.3rem;font-weight:300;max-width:600px;margin-bottom:2rem;">Predict your academic success in seconds!<br>Enter your details and discover your potentials.</p>', unsafe_allow_html=True)
    if st.button('🧮Predict final grade (G3)', key='predict_btn', help='Go to prediction page', use_container_width=False):
        st.session_state["page"] = "Predict Performance"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if page == "Predict Performance":
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#2563eb;font-weight:1100;">Enter Student Details for Prediction</h2>', unsafe_allow_html=True)
    st.markdown('''
        <div style="background:rgba(99,102,241,0.08);border-radius:1rem;padding:1.2rem 2rem;margin-bottom:1.5rem;max-width:900px;">
        <h4 style="color:#2563eb;margin-bottom:0.5rem;">Input Guide & Field Descriptions:</h4>
        <ul style="color:#222;font-size:1.05rem;line-height:1.7;">
            <li><b>Personal Information</b>:
                <ul>
                    <li><b>Age</b>: Student's age (15-22).</li>
                    <li><b>Sex</b>: F = Female, M = Male.</li>
                    <li><b>Address</b>: U = Urban, R = Rural.</li>
                    <li><b>Family Size</b>: LE3 = ≤3 members, GT3 = >3 members.</li>
                    <li><b>Parental Status</b>: T = Together, A = Apart.</li>
                </ul>
            </li>
            <li><b>Parental Education</b>:
                <ul>
                    <li><b>Mother's/Father's Education</b>: 0 = none, 1 = primary, 2 = 5th-9th grade, 3 = secondary, 4 = higher education.</li>
                    <li><b>Mother's/Father's Job</b>: teacher, health, services, at_home, other.</li>
                </ul>
            </li>
            <li><b>Motivation & Environment</b>:
                <ul>
                    <li><b>Reason for School Choice</b>: home, reputation, course, other.</li>
                    <li><b>Guardian</b>: mother, father, other.</li>
                    <li><b>Travel Time</b>: 1 = <15 min, 2 = 15-30 min, 3 = 30 min-1 hr, 4 = >1 hr.</li>
                    <li><b>Study Time</b>: 1 = <2 hrs, 2 = 2-5 hrs, 3 = 5-10 hrs, 4 = >10 hrs/week.</li>
                    <li><b>Past Class Failures</b>: 0 = none, 1 = one, 2 = two, 3 = three or more.</li>
                </ul>
            </li>
            <li><b>Support & Activities</b>:
                <ul>
                    <li><b>School/Family Support, Paid Classes, Activities, Nursery, Higher Education, Internet, Romantic</b>: yes or no.</li>
                </ul>
            </li>
            <li><b>Social Life & Habits</b>:
                <ul>
                    <li><b>Family Relationship Quality, Free Time, Going Out, Alcohol (Dalc/Walc), Health</b>: 1 = very low, 2 = low, 3 = average, 4 = high, 5 = very high.</li>
                    <li><b>Absences</b>: Number of school absences.</li>
                </ul>
            </li>
            <li><b>Academic Results</b>:
                <ul>
                    <li><b>G1, G2</b>: Grades for the first and second periods (0-20).</li>
                </ul>
            </li>
        </ul>
        <div style="color:#444;font-size:0.98rem;margin-top:0.7rem;">Please fill in each field carefully to get an accurate prediction of the final grade (G3).</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # --- FORM INPUTS ---
    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            school = st.selectbox("School", ["", "GP", "MS"], index=0)
            sex = st.selectbox("Sex", ["", "F", "M"], index=0)
            age = st.number_input("Age", min_value=15, max_value=22, value=None, placeholder="Select age")
            address = st.selectbox("Address", ["", "U", "R"], index=0)
            famsize = st.selectbox("Family Size", ["", "LE3", "GT3"], index=0)
            Pstatus = st.selectbox("Parent's Cohabitation Status", ["", "T", "A"], index=0)
            Medu = st.slider("Mother's Education (0-4)", 0, 4, value=None, format="%d")
            Fedu = st.slider("Father's Education (0-4)", 0, 4, value=None, format="%d")
            Mjob = st.selectbox("Mother's Job", ["", "teacher", "health", "services", "at_home", "other"], index=0)
            Fjob = st.selectbox("Father's Job", ["", "teacher", "health", "services", "at_home", "other"], index=0)
            reason = st.selectbox("Reason for School Choice", ["", "home", "reputation", "course", "other"], index=0)
        with col2:
            guardian = st.selectbox("Guardian", ["", "mother", "father", "other"], index=0)
            traveltime = st.slider("Travel Time (1-4)", 1, 4, value=None, format="%d")
            studytime = st.slider("Weekly Study Time (1-4)", 1, 4, value=None, format="%d")
            failures = st.slider("Past Class Failures", 0, 3, value=None, format="%d")
            schoolsup = st.selectbox("School Support", ["", "yes", "no"], index=0)
            famsup = st.selectbox("Family Support", ["", "yes", "no"], index=0)
            paid = st.selectbox("Extra Paid Classes", ["", "yes", "no"], index=0)
            activities = st.selectbox("Extracurricular Activities", ["", "yes", "no"], index=0)
            nursery = st.selectbox("Attended Nursery School", ["", "yes", "no"], index=0)
            higher = st.selectbox("Wants Higher Education", ["", "yes", "no"], index=0)
            internet = st.selectbox("Internet Access", ["", "yes", "no"], index=0)
        with col3:
            romantic = st.selectbox("In a Romantic Relationship", ["", "yes", "no"], index=0)
            famrel = st.slider("Family Relationship Quality (1-5)", 1, 5, value=None, format="%d")
            freetime = st.slider("Free Time After School (1-5)", 1, 5, value=None, format="%d")
            goout = st.slider("Going Out with Friends (1-5)", 1, 5, value=None, format="%d")
            Dalc = st.slider("Workday Alcohol Consumption (1-5)", 1, 5, value=None, format="%d")
            Walc = st.slider("Weekend Alcohol Consumption (1-5)", 1, 5, value=None, format="%d")
            health = st.slider("Current Health Status (1-5)", 1, 5, value=None, format="%d")
            absences = st.number_input("Number of Absences", min_value=0, max_value=100, value=None, placeholder="Enter absences")
            G1 = st.number_input("First Period Grade (G1, 0-20)", min_value=0, max_value=20, value=None, placeholder="Enter G1")
            G2 = st.number_input("Second Period Grade (G2, 0-20)", min_value=0, max_value=20, value=None, placeholder="Enter G2")
        
        submitted = st.form_submit_button("🔮 Predict Final Grade (G3)", use_container_width=True)

    # --- PREDICTION & OUTPUT ---
    if submitted:
        required_fields = [
            school, sex, age, address, famsize, Pstatus, Medu, Fedu, Mjob, Fjob, reason,
            guardian, traveltime, studytime, failures, schoolsup, famsup, paid, activities, nursery, higher, internet,
            romantic, famrel, freetime, goout, Dalc, Walc, health, absences, G1, G2
        ]
        
        if any(
            (isinstance(f, str) and (f == "" or f is None)) or
            (isinstance(f, (int, float)) and f is None)
            for f in required_fields
        ):
            st.warning("⚠️ Please fill in all fields before predicting the final grade.")
        else:
            # Prepare input for prediction
            input_dict = {
                'school': school, 'sex': sex, 'age': age, 'address': address, 'famsize': famsize, 'Pstatus': Pstatus,
                'Medu': Medu, 'Fedu': Fedu, 'Mjob': Mjob, 'Fjob': Fjob, 'reason': reason, 'guardian': guardian,
                'traveltime': traveltime, 'studytime': studytime, 'failures': failures, 'schoolsup': schoolsup,
                'famsup': famsup, 'paid': paid, 'activities': activities, 'nursery': nursery, 'higher': higher,
                'internet': internet, 'romantic': romantic, 'famrel': famrel, 'freetime': freetime, 'goout': goout,
                'Dalc': Dalc, 'Walc': Walc, 'health': health, 'absences': absences, 'G1': G1, 'G2': G2
            }
            
            input_df = pd.DataFrame([input_dict])
            
            try:
                model = joblib.load('model_sk.joblib')
                prediction = model.predict(input_df)[0]
                
                # Store results in session state
                st.session_state['prediction'] = prediction
                st.session_state['input_dict'] = input_dict
                st.session_state['prediction_made'] = True
                
                # Generate recommendations
                recommendations, grade_level, grade_color = generate_recommendations(input_dict, prediction)
                st.session_state['recommendations'] = recommendations
                st.session_state['grade_level'] = grade_level
                st.session_state['grade_color'] = grade_color
                
                # Display prediction result with enhanced styling
                st.markdown(f"""
                    <div class="prediction-result">
                        <div style="color: #374151; font-size: 1.8rem; font-weight: 600; margin-bottom: 0.5rem;">
                            🎯 Academic Performance Prediction
                        </div>
                        <div class="grade-subtitle">Your predicted final grade is:</div>
                        <div class="grade-display" style="color: {grade_color};">
                            {prediction:.1f}<span style="font-size: 2rem; color: #9ca3af;">/20</span>
                        </div>
                        <div class="performance-badge" style="background: linear-gradient(135deg, {grade_color} 0%, {grade_color}dd 100%);">
                            {grade_level}
                        </div>
                        <div style="margin-top: 1.5rem; color: #6b7280; font-size: 1rem; line-height: 1.6;">
                            This prediction is based on your academic history, study habits, and personal factors.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Prediction failed: {e}. Please ensure the model file exists and is compatible.")

    # Show action buttons only after successful prediction
    if st.session_state.get('prediction_made', False):
        prediction = st.session_state['prediction']
        input_dict = st.session_state['input_dict']
        
        # Prepare result text for download/email
        result_text = f"""Student Achievement Prediction Report
=====================================

PREDICTION RESULT:
Final Grade (G3): {prediction:.2f}/20
Performance Level: {st.session_state.get('grade_level', 'N/A')}

STUDENT PROFILE:
"""
        for k, v in input_dict.items():
            result_text += f"{k}: {v}\n"
        
        result_text += f"\nGenerated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result_text += "Report generated by GradePath - Student Achievement Predictor"
        
        # Action buttons container
        st.markdown('<div class="buttons-container">', unsafe_allow_html=True)
        
        # Create columns for inline buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            # Download button
            st.download_button(
                label="📄 Download Report",
                data=result_text,
                file_name=f"student_prediction_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True,
                help="Download detailed prediction report"
            )
        
        with col2:
            # Email button (using HTML for styling consistency)
            import urllib.parse
            subject = urllib.parse.quote("Student Achievement Prediction Report")
            body = urllib.parse.quote(result_text)
            mailto_link = f"mailto:?subject={subject}&body={body}"
            
            
            st.markdown(f"""
                <a href="{mailto_link}" target="_blank" style="text-decoration: none; width: 100%; display: block;">
                    <button class="start-btn btn-secondary" style="width: 100%;">📧 Share by Email</button>
                </a>
            """, unsafe_allow_html=True)
        
        with col3:
            # Recommendations toggle
            if st.session_state.get('recommendations_visible', False):
                hide_recs = st.button("🔼 Hide Tips", key="hide_recommendations_btn", use_container_width=True)
                if hide_recs:
                    st.session_state['recommendations_visible'] = False
                    st.rerun()
            else:
                show_recs = st.button("💡 View Tips", key="show_recommendations_btn", use_container_width=True)
                if show_recs:
                    st.session_state['recommendations_visible'] = True
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display recommendations if visible
        if st.session_state.get('recommendations_visible', False):
            recommendations = st.session_state.get('recommendations', [])
            
            st.markdown(f"""
                <div class="recommendation-box">
                    <div class="recommendation-title">🤖 AI-Powered Personal Recommendations</div>
                    <p style="color: #6b7280; margin-bottom: 1.5rem;">Based on your inputs and predicted performance, here are tailored suggestions to help improve your academic success:</p>
                </div>
            """, unsafe_allow_html=True)
            
            for rec in recommendations:
                st.markdown(f"""
                    <div class="recommendation-item">
                        <div class="recommendation-category">{rec['category']}</div>
                        <div class="recommendation-text">{rec['text']}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Ensure page state persistence
if "page" in st.session_state:
    page = st.session_state["page"]