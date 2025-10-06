import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from collections import Counter
import json

st.set_page_config(
    page_title="SkillSync Pro - Workforce Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Blue-Green Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F0F9FF 0%, #F0FDF4 100%);
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(135deg, #0EA5E9 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.08);
        border: 1px solid #E0F2FE;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #0EA5E9 0%, #10B981 100%);
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 30px rgba(14, 165, 233, 0.15);
        transform: translateY(-4px);
    }
    
    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #E0F2FE 0%, #D1FAE5 100%);
        color: #0369A1;
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 13px;
        font-weight: 600;
        margin: 6px 4px;
        border: 1px solid #BAE6FD;
        transition: all 0.2s;
    }
    
    .skill-tag:hover {
        background: linear-gradient(135deg, #0EA5E9 0%, #10B981 100%);
        color: white;
        border-color: transparent;
        transform: scale(1.05);
    }
    
    .skill-advanced {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border-color: transparent;
    }
    
    .skill-intermediate {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        border-color: transparent;
    }
    
    .skill-beginner {
        background: linear-gradient(135deg, #94A3B8 0%, #64748B 100%);
        color: white;
        border-color: transparent;
    }
    
    .skill-missing {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        color: #991B1B;
        border: 1px solid #FCA5A5;
    }
    
    .skill-learning {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        color: #92400E;
        border: 1px solid #FCD34D;
    }
    
    /* Cards */
    .course-card {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        border-left: 5px solid #10B981;
        box-shadow: 0 2px 12px rgba(16, 185, 129, 0.1);
        transition: all 0.3s;
    }
    
    .course-card:hover {
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.2);
        transform: translateX(4px);
    }
    
    .opportunity-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        border-left: 5px solid #0EA5E9;
        box-shadow: 0 2px 12px rgba(14, 165, 233, 0.1);
        transition: all 0.3s;
    }
    
    .opportunity-card:hover {
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.2);
        transform: translateX(4px);
    }
    
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #0EA5E9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin: 12px 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #F59E0B;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.1);
        margin: 12px 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #10B981;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
        margin: 12px 0;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #0EA5E9 0%, #10B981 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3) !important;
        transition: all 0.3s !important;
    }
    
    .stButton button:hover {
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0C4A6E 0%, #065F46 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #F0F9FF !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: #BAE6FD !important;
        font-weight: 600 !important;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #0EA5E9 0%, #10B981 100%);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0EA5E9 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Tables */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        border: 1px solid #E0F2FE;
    }
    
    /* Forms */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
        border: 2px solid #BAE6FD !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 15px !important;
        transition: all 0.2s !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0EA5E9 !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: white;
        padding: 8px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #64748B;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #F0F9FF;
        color: #0EA5E9;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0EA5E9 0%, #10B981 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 10px !important;
        border-left: 4px solid #0EA5E9 !important;
        font-weight: 600 !important;
        padding: 16px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F0F9FF !important;
    }
    
    /* Priority badges */
    .priority-critical {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .priority-high {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .priority-medium {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .priority-low {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #0EA5E9 0%, #10B981 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #0284C7 0%, #059669 100%);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Skills taxonomy
SKILL_CATEGORIES = {
    'Technical': {
        'Current High Demand': ['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'Kubernetes', 'SQL', 'Git', 'TypeScript', 'Node.js'],
        'Emerging': ['Rust', 'Go', 'GraphQL', 'Terraform', 'WebAssembly', 'Edge Computing', 'Microservices', 'gRPC'],
        'Future Critical (2026+)': ['AI/ML Integration', 'Quantum Computing', 'Web3', 'AR/VR Development', 'Blockchain', 'IoT']
    },
    'Data & AI': {
        'Current High Demand': ['Machine Learning', 'Data Analysis', 'SQL', 'Python', 'Tableau', 'Power BI', 'Statistics', 'R'],
        'Emerging': ['LLMs', 'Prompt Engineering', 'MLOps', 'Feature Stores', 'Vector Databases', 'Data Mesh', 'Streaming Analytics'],
        'Future Critical (2026+)': ['Responsible AI', 'AI Governance', 'Synthetic Data', 'Federated Learning', 'AutoML', 'AI Ethics']
    },
    'Product': {
        'Current High Demand': ['Product Strategy', 'User Research', 'Analytics', 'Roadmapping', 'Agile', 'Stakeholder Management'],
        'Emerging': ['AI Product Management', 'Growth Hacking', 'Platform Thinking', 'API Product Management', 'PLG Strategy'],
        'Future Critical (2026+)': ['AI-Native Products', 'Ecosystem Design', 'Web3 Products', 'Metaverse Strategy']
    },
    'Leadership': {
        'Current High Demand': ['People Management', 'Strategic Thinking', 'Communication', 'Decision Making', 'Team Building'],
        'Emerging': ['Remote Leadership', 'Data-Driven Leadership', 'Change Management', 'Cross-Cultural Management', 'OKRs'],
        'Future Critical (2026+)': ['AI-Assisted Leadership', 'Distributed Team Building', 'Crisis Management', 'Hybrid Work Management']
    },
    'Business': {
        'Current High Demand': ['Financial Analysis', 'Market Research', 'Business Strategy', 'Project Management', 'Negotiation'],
        'Emerging': ['Digital Transformation', 'Business Intelligence', 'Process Automation', 'Vendor Management'],
        'Future Critical (2026+)': ['AI-Driven Business Strategy', 'Sustainability Strategy', 'ESG Reporting']
    }
}

# Comprehensive learning paths
LEARNING_PATHS = {
    'Python': {
        'beginner': [
            {'name': 'Python for Everybody (Coursera)', 'duration': '8 weeks', 'cost': 'Free', 'provider': 'Coursera', 'rating': 4.8},
            {'name': 'Codecademy Learn Python 3', 'duration': '25 hours', 'cost': '$19.99/mo', 'provider': 'Codecademy', 'rating': 4.6}
        ],
        'intermediate': [
            {'name': 'Python Beyond the Basics', 'duration': '4 weeks', 'cost': '$49', 'provider': 'Udemy', 'rating': 4.7},
            {'name': 'Real Python Membership', 'duration': 'Self-paced', 'cost': '$60/year', 'provider': 'Real Python', 'rating': 4.9}
        ],
        'advanced': [
            {'name': 'Advanced Python Programming', 'duration': '6 weeks', 'cost': '$199', 'provider': 'Pluralsight', 'rating': 4.5},
            {'name': 'Python Design Patterns', 'duration': '40 hours', 'cost': '$89', 'provider': 'LinkedIn Learning', 'rating': 4.6}
        ]
    },
    'Machine Learning': {
        'beginner': [
            {'name': 'Machine Learning by Andrew Ng', 'duration': '11 weeks', 'cost': 'Free', 'provider': 'Coursera', 'rating': 4.9},
            {'name': 'Intro to ML with Python', 'duration': '6 weeks', 'cost': '$199', 'provider': 'DataCamp', 'rating': 4.7}
        ],
        'intermediate': [
            {'name': 'Applied ML in Production', 'duration': '8 weeks', 'cost': '$49/mo', 'provider': 'Coursera', 'rating': 4.6},
            {'name': 'Deep Learning Specialization', 'duration': '5 months', 'cost': '$49/mo', 'provider': 'Coursera', 'rating': 4.8}
        ],
        'advanced': [
            {'name': 'Advanced ML on Google Cloud', 'duration': '12 weeks', 'cost': '$49/mo', 'provider': 'Coursera', 'rating': 4.7},
            {'name': 'MLOps Specialization', 'duration': '4 months', 'cost': '$49/mo', 'provider': 'Coursera', 'rating': 4.6}
        ]
    },
    'AWS': {
        'beginner': [
            {'name': 'AWS Cloud Practitioner Essentials', 'duration': '6 hours', 'cost': 'Free', 'provider': 'AWS Training', 'rating': 4.7},
            {'name': 'AWS Fundamentals Specialization', 'duration': '4 weeks', 'cost': '$49/mo', 'provider': 'Coursera', 'rating': 4.6}
        ],
        'intermediate': [
            {'name': 'AWS Solutions Architect Associate', 'duration': '12 weeks', 'cost': '$299', 'provider': 'A Cloud Guru', 'rating': 4.8},
            {'name': 'Architecting on AWS', 'duration': '3 days', 'cost': '$2,100', 'provider': 'AWS Training', 'rating': 4.7}
        ],
        'advanced': [
            {'name': 'AWS Solutions Architect Professional', 'duration': '16 weeks', 'cost': '$399', 'provider': 'A Cloud Guru', 'rating': 4.8},
            {'name': 'Advanced Architecting on AWS', 'duration': '3 days', 'cost': '$2,100', 'provider': 'AWS Training', 'rating': 4.9}
        ]
    }
}

# Training costs and ROI
TRAINING_COSTS = {
    'Online Course': {'avg_cost': 150, 'time_hours': 40, 'completion_rate': 0.7},
    'Certification': {'avg_cost': 500, 'time_hours': 100, 'completion_rate': 0.6},
    'Bootcamp': {'avg_cost': 2000, 'time_hours': 200, 'completion_rate': 0.8},
    'Conference': {'avg_cost': 1500, 'time_hours': 24, 'completion_rate': 0.9},
    'Workshop': {'avg_cost': 800, 'time_hours': 16, 'completion_rate': 0.85},
    'Mentorship Program': {'avg_cost': 1200, 'time_hours': 80, 'completion_rate': 0.75}
}

# Initialize session state
if 'employees' not in st.session_state:
    st.session_state.employees = [
        {
            'name': 'Alex Johnson',
            'role': 'Software Engineer',
            'department': 'Engineering',
            'current_skills': ['Python', 'JavaScript', 'SQL', 'Git', 'Docker', 'React'],
            'proficiency': {'Python': 'Advanced', 'JavaScript': 'Intermediate', 'SQL': 'Advanced', 'Git': 'Advanced', 'Docker': 'Intermediate', 'React': 'Intermediate'},
            'learning_goals': ['Machine Learning', 'AWS', 'System Design', 'Kubernetes'],
            'career_goal': 'Senior Software Engineer',
            'salary': 95000,
            'years_experience': 4,
            'certifications': ['AWS Cloud Practitioner'],
            'completed_courses': ['Python Advanced'],
            'target_salary': 125000
        },
        {
            'name': 'Maria Garcia',
            'role': 'Data Analyst',
            'department': 'Data',
            'current_skills': ['SQL', 'Python', 'Tableau', 'Excel', 'Statistics', 'Power BI'],
            'proficiency': {'SQL': 'Advanced', 'Python': 'Intermediate', 'Tableau': 'Advanced', 'Excel': 'Advanced', 'Statistics': 'Intermediate', 'Power BI': 'Advanced'},
            'learning_goals': ['Machine Learning', 'MLOps', 'Big Data', 'Deep Learning'],
            'career_goal': 'Data Scientist',
            'salary': 82000,
            'years_experience': 3,
            'certifications': ['Tableau Desktop Specialist'],
            'completed_courses': ['SQL Mastery', 'Python for Data Science'],
            'target_salary': 110000
        },
        {
            'name': 'David Chen',
            'role': 'Product Manager',
            'department': 'Product',
            'current_skills': ['Product Strategy', 'Analytics', 'User Research', 'Agile', 'Roadmapping', 'Stakeholder Management'],
            'proficiency': {'Product Strategy': 'Intermediate', 'Analytics': 'Advanced', 'User Research': 'Intermediate', 'Agile': 'Advanced', 'Roadmapping': 'Intermediate', 'Stakeholder Management': 'Advanced'},
            'learning_goals': ['AI Product Management', 'Growth Hacking', 'Platform Strategy', 'Data-Driven PM'],
            'career_goal': 'Senior Product Manager',
            'salary': 110000,
            'years_experience': 5,
            'certifications': ['Certified Scrum Product Owner'],
            'completed_courses': ['Product Management Fundamentals'],
            'target_salary': 145000
        },
        {
            'name': 'Sarah Williams',
            'role': 'Engineering Manager',
            'department': 'Engineering',
            'current_skills': ['People Management', 'System Design', 'Python', 'AWS', 'Strategic Thinking', 'Team Building'],
            'proficiency': {'People Management': 'Advanced', 'System Design': 'Advanced', 'Python': 'Advanced', 'AWS': 'Intermediate', 'Strategic Thinking': 'Advanced', 'Team Building': 'Advanced'},
            'learning_goals': ['Remote Leadership', 'OKRs', 'Cloud Architecture', 'Budget Management'],
            'career_goal': 'Director of Engineering',
            'salary': 145000,
            'years_experience': 8,
            'certifications': ['AWS Solutions Architect Associate'],
            'completed_courses': ['Leadership Fundamentals', 'Engineering Management'],
            'target_salary': 185000
        }
    ]

if 'company_initiatives' not in st.session_state:
    st.session_state.company_initiatives = [
        {
            'name': 'AI Integration Project', 
            'required_skills': ['Machine Learning', 'Python', 'MLOps', 'AI Product Management', 'LLMs'], 
            'timeline': 'Q2 2025', 
            'priority': 'Critical',
            'description': 'Integrate AI capabilities across product suite',
            'budget': 500000,
            'team_size': 12
        },
        {
            'name': 'Cloud Migration', 
            'required_skills': ['AWS', 'Kubernetes', 'Terraform', 'Docker', 'Microservices'], 
            'timeline': 'Q3 2025', 
            'priority': 'High',
            'description': 'Migrate all services to AWS cloud infrastructure',
            'budget': 350000,
            'team_size': 8
        },
        {
            'name': 'Mobile App Launch', 
            'required_skills': ['React Native', 'Mobile Development', 'API Design', 'User Research'], 
            'timeline': 'Q4 2025', 
            'priority': 'Medium',
            'description': 'Launch native mobile applications for iOS and Android',
            'budget': 250000,
            'team_size': 6
        },
        {
            'name': 'Data Platform Modernization',
            'required_skills': ['Big Data', 'Data Engineering', 'Python', 'SQL', 'Streaming Analytics'],
            'timeline': 'Q1 2026',
            'priority': 'High',
            'description': 'Build real-time data processing platform',
            'budget': 400000,
            'team_size': 10
        }
    ]

if 'training_records' not in st.session_state:
    st.session_state.training_records = []

if 'skill_assessments' not in st.session_state:
    st.session_state.skill_assessments = []

# Helper functions
def predict_future_skills(employee, company_initiatives):
    """Predict skills needed based on company direction"""
    future_skills = set()
    
    for initiative in company_initiatives:
        if initiative['priority'] in ['Critical', 'High']:
            future_skills.update(initiative['required_skills'])
    
    for category, skills_data in SKILL_CATEGORIES.items():
        if any(skill in employee['current_skills'] for skill in skills_data['Current High Demand']):
            future_skills.update(skills_data['Emerging'][:3])
    
    future_skills = future_skills - set(employee['current_skills'])
    
    return list(future_skills)

def calculate_skill_gap(employee, target_skills):
    """Calculate gap between current and target skills"""
    current = set(employee['current_skills'])
    target = set(target_skills)
    
    gap = target - current
    overlap = target & current
    
    return {
        'missing': list(gap),
        'have': list(overlap),
        'gap_percentage': (len(gap) / len(target) * 100) if target else 0,
        'readiness_score': (len(overlap) / len(target) * 100) if target else 0
    }

def generate_learning_path(skill, current_level='beginner'):
    """Generate personalized learning path"""
    if skill in LEARNING_PATHS:
        return LEARNING_PATHS[skill]
    
    return {
        'beginner': [{'name': f'{skill} Fundamentals', 'duration': '6 weeks', 'cost': '$99', 'provider': 'Various', 'rating': 4.5}],
        'intermediate': [{'name': f'Advanced {skill}', 'duration': '8 weeks', 'cost': '$199', 'provider': 'Various', 'rating': 4.5}],
        'advanced': [{'name': f'{skill} Expert Level', 'duration': '12 weeks', 'cost': '$399', 'provider': 'Various', 'rating': 4.5}]
    }

def find_internal_opportunities(employee, all_employees):
    """Find internal mobility opportunities"""
    role_transitions = {
        'Software Engineer': ['Senior Software Engineer', 'Tech Lead', 'Data Engineer', 'DevOps Engineer'],
        'Data Analyst': ['Data Scientist', 'Senior Data Analyst', 'Analytics Manager', 'Business Intelligence Lead'],
        'Product Manager': ['Senior Product Manager', 'Group Product Manager', 'Technical Product Manager', 'Product Director'],
        'Engineering Manager': ['Director of Engineering', 'VP Engineering', 'CTO']
    }
    
    potential_roles = role_transitions.get(employee['role'], [])
    
    opportunities = []
    for role in potential_roles:
        role_skills = {
            'Senior Software Engineer': ['System Design', 'Microservices', 'Leadership', 'Cloud Architecture', 'Performance Optimization'],
            'Tech Lead': ['Team Leadership', 'Architecture', 'Mentoring', 'Project Management', 'Technical Strategy'],
            'Data Scientist': ['Machine Learning', 'Statistics', 'Python', 'Deep Learning', 'Feature Engineering'],
            'Senior Product Manager': ['Product Strategy', 'Leadership', 'Market Analysis', 'Stakeholder Management', 'Business Intelligence'],
            'Director of Engineering': ['Strategic Planning', 'Budget Management', 'People Management', 'Organizational Design', 'Technical Vision']
        }
        
        required = role_skills.get(role, [])
        gap_analysis = calculate_skill_gap(employee, required)
        
        # Calculate estimated timeline
        missing_skills = len(gap_analysis['missing'])
        estimated_months = missing_skills * 2  # 2 months per skill
        
        # Calculate salary increase potential
        current_salary = employee.get('salary', 0)
        target_salary = employee.get('target_salary', 0)
        salary_increase = target_salary - current_salary
        
        opportunities.append({
            'role': role,
            'required_skills': required,
            'gap_analysis': gap_analysis,
            'estimated_timeline': f"{estimated_months} months",
            'readiness': gap_analysis['readiness_score'],
            'salary_range': f"${current_salary:,} → ${target_salary:,}",
            'salary_increase': salary_increase
        })
    
    return sorted(opportunities, key=lambda x: x['readiness'], reverse=True)

def calculate_training_roi(skill, employee_salary, business_impact='Medium'):
    """Calculate ROI for training investment"""
    training_type = 'Online Course'  # Default
    
    if skill in ['AWS', 'Machine Learning', 'Cloud Architecture']:
        training_type = 'Certification'
    elif skill in ['Leadership', 'Product Strategy']:
        training_type = 'Workshop'
    
    cost_data = TRAINING_COSTS[training_type]
    
    # Calculate productivity gains
    impact_multipliers = {'Low': 0.05, 'Medium': 0.10, 'High': 0.15, 'Critical': 0.20}
    productivity_gain = employee_salary * impact_multipliers.get(business_impact, 0.10)
    
    # Calculate time to proficiency
    weeks_to_proficiency = cost_data['time_hours'] / 10  # Assuming 10 hours/week
    
    # First year ROI
    annual_value = productivity_gain
    total_cost = cost_data['avg_cost'] + (employee_salary / 2080 * cost_data['time_hours'])  # Include time cost
    
    roi_percentage = ((annual_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
    payback_months = (total_cost / (productivity_gain / 12)) if productivity_gain > 0 else 0
    
    return {
        'training_cost': cost_data['avg_cost'],
        'time_cost': employee_salary / 2080 * cost_data['time_hours'],
        'total_cost': total_cost,
        'annual_value': annual_value,
        'roi_percentage': roi_percentage,
        'payback_months': payback_months,
        'completion_rate': cost_data['completion_rate'],
        'training_type': training_type,
        'hours_required': cost_data['time_hours']
    }

def generate_team_insights(employees, initiatives):
    """Generate team-level insights"""
    all_skills = []
    for emp in employees:
        all_skills.extend(emp['current_skills'])
    
    skill_counts = Counter(all_skills)
    
    # Calculate coverage for each initiative
    initiative_coverage = []
    for init in initiatives:
        required = set(init['required_skills'])
        team_skills = set(all_skills)
        coverage = len(required & team_skills) / len(required) * 100 if required else 0
        
        initiative_coverage.append({
            'initiative': init['name'],
            'coverage': coverage,
            'priority': init['priority'],
            'timeline': init['timeline'],
            'missing_skills': list(required - team_skills)
        })
    
    return {
        'total_unique_skills': len(skill_counts),
        'most_common_skills': skill_counts.most_common(10),
        'initiative_coverage': sorted(initiative_coverage, key=lambda x: x['coverage'])
    }

# ==================== MAIN APP ====================

st.title("🎓 SkillSync Pro - Workforce Intelligence Platform")
st.markdown("*AI-Powered Skills Management & Career Development*")

# Sidebar Navigation
with st.sidebar:
    st.image("assets/sga0.jpg", use_container_width=True)
    st.markdown("---")
    
    page = st.selectbox(
        "📍 Navigate",
        ["🏠 Dashboard", "👥 Employee Profiles", "🎯 Skills Analysis", "📚 Learning Paths", 
         "🚀 Career Planning", "📊 Analytics & ROI", "➕ Add Employee", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    st.metric("Total Employees", len(st.session_state.employees))
    st.metric("Active Initiatives", len(st.session_state.company_initiatives))
    
    total_skills = len(set([skill for emp in st.session_state.employees for skill in emp['current_skills']]))
    st.metric("Unique Skills", total_skills)

# ==================== DASHBOARD PAGE ====================
if page == "🏠 Dashboard":
    st.header("Executive Dashboard")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #64748B; font-size: 14px; margin: 0;">Team Size</h3>
            <h1 style="color: #0EA5E9; font-size: 42px; margin: 10px 0;">{}</h1>
            <p style="color: #10B981; font-size: 13px; margin: 0;">↑ 12% from last quarter</p>
        </div>
        """.format(len(st.session_state.employees)), unsafe_allow_html=True)
    
    with col2:
        avg_skills = sum(len(emp['current_skills']) for emp in st.session_state.employees) / len(st.session_state.employees)
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #64748B; font-size: 14px; margin: 0;">Avg Skills per Employee</h3>
            <h1 style="color: #10B981; font-size: 42px; margin: 10px 0;">{:.1f}</h1>
            <p style="color: #0EA5E9; font-size: 13px; margin: 0;">↑ 8% skill growth rate</p>
        </div>
        """.format(avg_skills), unsafe_allow_html=True)
    
    with col3:
        team_insights = generate_team_insights(st.session_state.employees, st.session_state.company_initiatives)
        avg_coverage = sum(i['coverage'] for i in team_insights['initiative_coverage']) / len(team_insights['initiative_coverage'])
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #64748B; font-size: 14px; margin: 0;">Initiative Readiness</h3>
            <h1 style="color: #F59E0B; font-size: 42px; margin: 10px 0;">{:.0f}%</h1>
            <p style="color: #EF4444; font-size: 13px; margin: 0;">↓ Needs attention</p>
        </div>
        """.format(avg_coverage), unsafe_allow_html=True)
    
    with col4:
        total_learning_goals = sum(len(emp['learning_goals']) for emp in st.session_state.employees)
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #64748B; font-size: 14px; margin: 0;">Active Learning Goals</h3>
            <h1 style="color: #8B5CF6; font-size: 42px; margin: 10px 0;">{}</h1>
            <p style="color: #10B981; font-size: 13px; margin: 0;">↑ 23% engagement</p>
        </div>
        """.format(total_learning_goals), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Dashboard Content
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Skills Overview", "🎯 Initiative Readiness", "⚠️ Critical Gaps", "🏆 Top Performers"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Skills in Organization")
            all_skills = [skill for emp in st.session_state.employees for skill in emp['current_skills']]
            skill_counts = Counter(all_skills)
            top_skills = skill_counts.most_common(10)
            
            if top_skills:
                fig = go.Figure(data=[
                    go.Bar(
                        x=[count for _, count in top_skills],
                        y=[skill for skill, _ in top_skills],
                        orientation='h',
                        marker=dict(
                            color=[count for _, count in top_skills],
                            colorscale='Tealgrn',
                            showscale=False
                        ),
                        text=[count for _, count in top_skills],
                        textposition='auto',
                    )
                ])
                fig.update_layout(
                    height=400,
                    xaxis_title="Number of Employees",
                    yaxis_title="",
                    yaxis=dict(autorange="reversed"),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                )
                st.plotly_chart(fig, use_container_width=True, key="dashboard_top_skills")
        
        with col2:
            st.subheader("Skills by Category")
            category_counts = {}
            for category in SKILL_CATEGORIES.keys():
                count = 0
                for emp in st.session_state.employees:
                    for skill in emp['current_skills']:
                        for skill_type in SKILL_CATEGORIES[category].values():
                            if skill in skill_type:
                                count += 1
                category_counts[category] = count
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=list(category_counts.keys()),
                    values=list(category_counts.values()),
                    hole=0.4,
                    marker=dict(colors=['#0EA5E9', '#10B981', '#F59E0B', '#8B5CF6', '#EF4444'])
                )
            ])
            fig.update_layout(
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True, key="dashboard_skills_category")
    
    with tab2:
        st.subheader("Initiative Readiness Analysis")
        
        for initiative in team_insights['initiative_coverage']:
            priority_class = f"priority-{initiative['priority'].lower()}"
            
            st.markdown(f"""
            <div class="opportunity-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: #0F172A;">{initiative['initiative']}</h3>
                        <p style="color: #64748B; margin: 5px 0;">Timeline: {initiative['timeline']}</p>
                    </div>
                    <span class="{priority_class}">{initiative['priority']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.progress(initiative['coverage'] / 100)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**Readiness: {initiative['coverage']:.0f}%**")
            with col2:
                if initiative['coverage'] < 50:
                    st.error("⚠️ High Risk")
                elif initiative['coverage'] < 75:
                    st.warning("⚡ Needs Attention")
                else:
                    st.success("✅ On Track")
            
            if initiative['missing_skills']:
                with st.expander("View Missing Skills"):
                    for skill in initiative['missing_skills']:
                        st.markdown(f'<span class="skill-tag skill-missing">{skill}</span>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Critical Skill Gaps")
        
        # Identify critical gaps across all initiatives
        all_required_skills = []
        for init in st.session_state.company_initiatives:
            if init['priority'] in ['Critical', 'High']:
                all_required_skills.extend(init['required_skills'])
        
        all_current_skills = [skill for emp in st.session_state.employees for skill in emp['current_skills']]
        
        critical_gaps = set(all_required_skills) - set(all_current_skills)
        gap_counts = Counter([skill for skill in all_required_skills if skill in critical_gaps])
        
        if critical_gaps:
            st.warning(f"⚠️ **{len(critical_gaps)} critical skills** are completely missing from the team")
            
            for skill, count in gap_counts.most_common(10):
                st.markdown(f"""
                <div class="warning-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0; color: #92400E;">{skill}</h4>
                            <p style="color: #78350F; margin: 5px 0; font-size: 13px;">
                                Required for {count} high-priority initiative(s)
                            </p>
                        </div>
                        <div>
                            <span class="priority-high">URGENT</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show recommended actions
                with st.expander("Recommended Actions"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**🎯 Hire Externally**")
                        st.write("- Time to hire: 2-3 months")
                        st.write("- Cost: $15,000 - $25,000")
                        st.write("- Risk: Medium")
                    
                    with col2:
                        st.write("**📚 Train Internally**")
                        learning_path = generate_learning_path(skill)
                        if 'intermediate' in learning_path:
                            course = learning_path['intermediate'][0]
                            st.write(f"- Duration: {course['duration']}")
                            st.write(f"- Cost: {course['cost']}")
                            st.write("- Risk: Low")
        else:
            st.success("✅ No critical gaps identified! Team is well-positioned for upcoming initiatives.")
    
    with tab4:
        st.subheader("Top Performers & Rising Stars")
        
        # Calculate performance scores
        employee_scores = []
        for emp in st.session_state.employees:
            score = len(emp['current_skills']) * 2
            score += len(emp.get('certifications', [])) * 5
            score += len(emp.get('completed_courses', [])) * 3
            score += len(emp['learning_goals']) * 1
            
            employee_scores.append({
                'name': emp['name'],
                'role': emp['role'],
                'score': score,
                'skills_count': len(emp['current_skills']),
                'learning_goals': len(emp['learning_goals'])
            })
        
        top_performers = sorted(employee_scores, key=lambda x: x['score'], reverse=True)
        
        for i, performer in enumerate(top_performers[:5], 1):
            medal = ["🥇", "🥈", "🥉", "🏅", "🏅"][i-1]
            
            st.markdown(f"""
            <div class="success-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="font-size: 32px;">{medal}</div>
                        <div>
                            <h3 style="margin: 0; color: #0F172A;">{performer['name']}</h3>
                            <p style="color: #64748B; margin: 5px 0;">{performer['role']}</p>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <h2 style="margin: 0; color: #10B981;">{performer['score']}</h2>
                        <p style="color: #64748B; margin: 0; font-size: 12px;">Performance Score</p>
                    </div>
                </div>
                <div style="margin-top: 15px; display: flex; gap: 20px; font-size: 13px; color: #475569;">
                    <span>💼 {performer['skills_count']} Skills</span>
                    <span>🎯 {performer['learning_goals']} Learning Goals</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================== EMPLOYEE PROFILES PAGE ====================
elif page == "👥 Employee Profiles":
    st.header("Employee Profiles")
    
    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search employees", placeholder="Search by name, role, or skill...")
    with col2:
        dept_filter = st.selectbox("Department", ["All"] + list(set([emp['department'] for emp in st.session_state.employees])))
    with col3:
        role_filter = st.selectbox("Role", ["All"] + list(set([emp['role'] for emp in st.session_state.employees])))
    
    # Filter employees
    filtered_employees = st.session_state.employees
    if search:
        filtered_employees = [emp for emp in filtered_employees if 
                            search.lower() in emp['name'].lower() or 
                            search.lower() in emp['role'].lower() or
                            any(search.lower() in skill.lower() for skill in emp['current_skills'])]
    if dept_filter != "All":
        filtered_employees = [emp for emp in filtered_employees if emp['department'] == dept_filter]
    if role_filter != "All":
        filtered_employees = [emp for emp in filtered_employees if emp['role'] == role_filter]
    
    st.markdown(f"*Showing {len(filtered_employees)} employee(s)*")
    st.markdown("---")
    
    # Display employee cards
    for emp_idx, emp in enumerate(filtered_employees):
        with st.expander(f"**{emp['name']}** - {emp['role']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Department:** {emp['department']}")
                st.markdown(f"**Experience:** {emp.get('years_experience', 'N/A')} years")
                st.markdown(f"**Career Goal:** {emp.get('career_goal', 'Not specified')}")
                
                st.markdown("**Current Skills:**")
                for skill in emp['current_skills']:
                    proficiency = emp.get('proficiency', {}).get(skill, 'Unknown')
                    prof_class = f"skill-{proficiency.lower()}" if proficiency != 'Unknown' else 'skill-tag'
                    st.markdown(f'<span class="{prof_class}">{skill} • {proficiency}</span>', unsafe_allow_html=True)
                
                st.markdown("<br>**Learning Goals:**", unsafe_allow_html=True)
                for goal in emp['learning_goals']:
                    st.markdown(f'<span class="skill-tag skill-learning">{goal}</span>', unsafe_allow_html=True)
                
                if emp.get('certifications'):
                    st.markdown(f"<br>**Certifications:** {', '.join(emp['certifications'])}", unsafe_allow_html=True)
            
            with col2:
                # Skills radar chart
                proficiency_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
                skills_data = [(skill, proficiency_map.get(emp.get('proficiency', {}).get(skill, 'Beginner'), 1)) 
                              for skill in emp['current_skills'][:6]]
                
                if skills_data:
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=[level for _, level in skills_data],
                        theta=[skill for skill, _ in skills_data],
                        fill='toself',
                        marker=dict(color='#0EA5E9')
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 3])),
                        showlegend=False,
                        height=250,
                        margin=dict(l=40, r=40, t=40, b=40)
                    )
                    st.plotly_chart(fig, use_container_width=True, key=f"radar_{emp_idx}")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📚 Learning Path", key=f"learn_{emp_idx}"):
                    st.session_state.selected_employee_learning = emp['name']
            with col2:
                if st.button(f"🚀 Career Plan", key=f"career_{emp_idx}"):
                    st.session_state.selected_employee_career = emp['name']
            with col3:
                if st.button(f"📊 Full Analysis", key=f"analyze_{emp_idx}"):
                    st.session_state.selected_employee_analysis = emp['name']

# ==================== SKILLS ANALYSIS PAGE ====================
elif page == "🎯 Skills Analysis":
    st.header("Skills Gap Analysis")
    
    selected_employee = st.selectbox("Select Employee", [emp['name'] for emp in st.session_state.employees])
    employee = next(emp for emp in st.session_state.employees if emp['name'] == selected_employee)
    
    tab1, tab2, tab3 = st.tabs(["🎯 Initiative Readiness", "🔮 Future Skills", "📈 Skill Matrix"])
    
    with tab1:
        st.subheader("Initiative Readiness Assessment")
        
        for idx, initiative in enumerate(st.session_state.company_initiatives):
            gap_analysis = calculate_skill_gap(employee, initiative['required_skills'])
            
            priority_class = f"priority-{initiative['priority'].lower()}"
            description = initiative.get('description', 'No description available')
            
            st.markdown(f"""
            <div class="opportunity-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3 style="margin: 0;">{initiative['name']}</h3>
                    <span class="{priority_class}">{initiative['priority']}</span>
                </div>
                <p style="color: #64748B; margin-bottom: 10px;">{description}</p>
                <p style="color: #64748B; font-size: 13px;">Timeline: {initiative['timeline']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Readiness Score", f"{gap_analysis['readiness_score']:.0f}%")
            with col2:
                st.metric("Skills Match", f"{len(gap_analysis['have'])}/{len(initiative['required_skills'])}")
            with col3:
                st.metric("Skills Gap", len(gap_analysis['missing']))
            
            st.progress(gap_analysis['readiness_score'] / 100)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Current Skills Match:**")
                for skill in gap_analysis['have']:
                    st.markdown(f'<span class="skill-tag skill-advanced">{skill}</span>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("**❌ Missing Skills:**")
                for skill_idx, skill in enumerate(gap_analysis['missing']):
                    st.markdown(f'<span class="skill-tag skill-missing">{skill}</span>', unsafe_allow_html=True)
                    
                    # Calculate ROI for training
                    roi = calculate_training_roi(skill, employee.get('salary', 80000), initiative['priority'])
                    
                    with st.expander(f"📊 Training ROI for {skill}"):
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Investment", f"${roi['total_cost']:,.0f}")
                        with col_b:
                            st.metric("Annual Value", f"${roi['annual_value']:,.0f}")
                        with col_c:
                            st.metric("ROI", f"{roi['roi_percentage']:.0f}%")
                        
                        st.write(f"**Payback Period:** {roi['payback_months']:.1f} months")
                        st.write(f"**Training Type:** {roi['training_type']}")
                        st.write(f"**Time Required:** {roi['hours_required']} hours")
            
            st.markdown("---")
    
    with tab2:
        st.subheader("Future Skills Prediction")
        
        future_skills = predict_future_skills(employee, st.session_state.company_initiatives)
        
        st.markdown("""
        <div class="info-card">
            <h4 style="margin-top: 0;">🔮 Recommended Skills for 2025-2026</h4>
            <p>Based on company initiatives, industry trends, and career trajectory</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Categorize future skills
        for category, skills_data in SKILL_CATEGORIES.items():
            category_future = [s for s in future_skills if any(s in skill_list for skill_list in skills_data.values())]
            
            if category_future:
                st.markdown(f"### {category}")
                
                for skill in category_future[:5]:
                    # Determine if emerging or future critical
                    is_emerging = skill in skills_data.get('Emerging', [])
                    is_future = skill in skills_data.get('Future Critical (2026+)', [])
                    
                    skill_type = "🚀 Emerging" if is_emerging else "🔮 Future Critical"
                    tag_class = "skill-learning" if is_emerging else "skill-missing"
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f'<span class="skill-tag {tag_class}">{skill} • {skill_type}</span>', unsafe_allow_html=True)
                    with col2:
                        roi = calculate_training_roi(skill, employee.get('salary', 80000), 'High')
                        st.write(f"ROI: {roi['roi_percentage']:.0f}%")
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Comprehensive Skill Matrix")
        
        # Create skill matrix
        all_relevant_skills = set()
        for init in st.session_state.company_initiatives:
            all_relevant_skills.update(init['required_skills'])
        
        matrix_data = []
        for skill in sorted(all_relevant_skills):
            has_skill = skill in employee['current_skills']
            proficiency = employee.get('proficiency', {}).get(skill, 'N/A') if has_skill else 'N/A'
            is_learning = skill in employee['learning_goals']
            
            # Find which initiatives need this skill
            required_for = [init['name'] for init in st.session_state.company_initiatives if skill in init['required_skills']]
            
            matrix_data.append({
                'Skill': skill,
                'Current Status': '✅ Have' if has_skill else ('🎯 Learning' if is_learning else '❌ Missing'),
                'Proficiency': proficiency,
                'Required For': ', '.join(required_for[:2]) + ('...' if len(required_for) > 2 else ''),
                'Priority': 'High' if len(required_for) >= 2 else 'Medium' if len(required_for) == 1 else 'Low'
            })
        
        df = pd.DataFrame(matrix_data)
        st.dataframe(df, use_container_width=True, height=400)
        
        # Export option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Skills Matrix",
            data=csv,
            file_name=f"skills_matrix_{selected_employee.replace(' ', '_')}.csv",
            mime="text/csv"
        )

# ==================== LEARNING PATHS PAGE ====================
elif page == "📚 Learning Paths":
    st.header("Personalized Learning Paths")
    
    selected_employee = st.selectbox("Select Employee", [emp['name'] for emp in st.session_state.employees])
    employee = next(emp for emp in st.session_state.employees if emp['name'] == selected_employee)
    
    st.markdown(f"### Learning Journey for {employee['name']}")
    st.markdown(f"*Current Role: {employee['role']} • Target: {employee.get('career_goal', 'Not specified')}*")
    
    # Priority skills based on gaps
    st.subheader("🎯 Priority Skills")
    
    all_required = set()
    for init in st.session_state.company_initiatives:
        if init['priority'] in ['Critical', 'High']:
            all_required.update(init['required_skills'])
    
    priority_gaps = all_required - set(employee['current_skills'])
    
    for idx, skill in enumerate(list(priority_gaps)[:5]):
        with st.container():
            st.markdown(f"""
            <div class="course-card">
                <h3 style="margin-top: 0; color: #0F172A;">{skill}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Get learning path
            current_level = employee.get('proficiency', {}).get(skill, 'beginner')
            if current_level not in ['beginner', 'intermediate', 'advanced']:
                current_level = 'beginner'
            
            learning_path = generate_learning_path(skill, current_level)
            
            # ROI calculation
            roi = calculate_training_roi(skill, employee.get('salary', 80000), 'High')
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Recommended Level:** {current_level.title()}")
                
                if current_level in learning_path:
                    for course in learning_path[current_level]:
                        st.markdown(f"""
                        <div class="info-card">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div>
                                    <h4 style="margin: 0 0 5px 0;">{course['name']}</h4>
                                    <p style="margin: 0; color: #64748B; font-size: 13px;">
                                        {course['provider']} • {course['duration']} • ⭐ {course['rating']}
                                    </p>
                                </div>
                                <div style="text-align: right;">
                                    <span style="font-size: 18px; font-weight: 700; color: #0EA5E9;">{course['cost']}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("**📊 Training ROI**")
                st.metric("Investment", f"${roi['total_cost']:,.0f}")
                st.metric("Annual Value", f"${roi['annual_value']:,.0f}")
                st.metric("ROI", f"{roi['roi_percentage']:.0f}%", 
                         delta=f"{roi['payback_months']:.1f} mo payback")
                
                if st.button(f"➕ Add to Plan", key=f"add_{skill}_{idx}"):
                    st.success(f"✅ {skill} added to learning plan!")
            
            st.markdown("---")
    
    # Learning goals
    st.subheader("🎯 Current Learning Goals")
    if employee['learning_goals']:
        for idx, goal in enumerate(employee['learning_goals']):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f'<span class="skill-tag skill-learning">{goal}</span>', unsafe_allow_html=True)
            with col2:
                progress = st.slider("Progress", 0, 100, 0, key=f"progress_{goal}_{idx}", label_visibility="collapsed")
            with col3:
                if st.button("✅ Complete", key=f"complete_{goal}_{idx}"):
                    st.success(f"{goal} completed!")
    else:
        st.info("No active learning goals. Add skills from the priority list above!")

# ==================== CAREER PLANNING PAGE ====================
elif page == "🚀 Career Planning":
    st.header("Career Development & Internal Mobility")
    
    selected_employee = st.selectbox("Select Employee", [emp['name'] for emp in st.session_state.employees])
    employee = next(emp for emp in st.session_state.employees if emp['name'] == selected_employee)
    
    # Career overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Role", employee['role'])
    with col2:
        st.metric("Experience", f"{employee.get('years_experience', 0)} years")
    with col3:
        st.metric("Career Goal", employee.get('career_goal', 'Not Set'))
    
    st.markdown("---")
    
    # Internal opportunities
    opportunities = find_internal_opportunities(employee, st.session_state.employees)
    
    st.subheader("🎯 Potential Career Paths")
    
    for opp_idx, opp in enumerate(opportunities):
        readiness_color = "#10B981" if opp['readiness'] >= 75 else "#F59E0B" if opp['readiness'] >= 50 else "#EF4444"
        
        st.markdown(f"""
        <div class="opportunity-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h3 style="margin: 0;">{opp['role']}</h3>
                <div style="text-align: right;">
                    <div style="font-size: 32px; font-weight: 800; color: {readiness_color};">
                        {opp['readiness']:.0f}%
                    </div>
                    <div style="font-size: 12px; color: #64748B;">Readiness</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Timeline", opp['estimated_timeline'])
        with col2:
            st.metric("Skills Gap", len(opp['gap_analysis']['missing']))
        with col3:
            st.metric("Salary Impact", f"+${opp['salary_increase']:,}")
        
        # Detailed breakdown
        with st.expander("📋 Detailed Career Path"):
            tab1, tab2, tab3 = st.tabs(["Required Skills", "Development Plan", "Financial Impact"])
            
            with tab1:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**✅ Skills You Have:**")
                    for skill in opp['gap_analysis']['have']:
                        st.markdown(f'<span class="skill-tag skill-advanced">{skill}</span>', unsafe_allow_html=True)
                
                with col_b:
                    st.markdown("**📚 Skills to Develop:**")
                    for skill in opp['gap_analysis']['missing']:
                        st.markdown(f'<span class="skill-tag skill-missing">{skill}</span>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown("**🗺️ Recommended Development Path:**")
                
                total_cost = 0
                total_time = 0
                
                for i, skill in enumerate(opp['gap_analysis']['missing'], 1):
                    roi = calculate_training_roi(skill, employee.get('salary', 80000))
                    total_cost += roi['total_cost']
                    total_time += roi['hours_required']
                    
                    st.markdown(f"""
                    **Step {i}: Master {skill}**
                    - Training: {roi['training_type']}
                    - Duration: {roi['hours_required']} hours
                    - Investment: ${roi['total_cost']:,.0f}
                    - Expected ROI: {roi['roi_percentage']:.0f}%
                    """)
                
                st.markdown("---")
                st.markdown(f"""
                **📊 Total Investment Summary:**
                - **Total Cost:** ${total_cost:,.0f}
                - **Total Time:** {total_time} hours ({total_time/40:.1f} weeks at 40hrs/week)
                - **Expected Timeline:** {opp['estimated_timeline']}
                """)
            
            with tab3:
                current_salary = employee.get('salary', 0)
                target_salary = employee.get('target_salary', 0)
                
                # Create salary progression chart
                years = list(range(5))
                current_projection = [current_salary * (1.03 ** year) for year in years]
                with_promotion = [current_salary * (1.03 ** year) if year < 2 else target_salary * (1.03 ** (year-2)) for year in years]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=years, y=current_projection,
                    name='Current Path',
                    line=dict(color='#94A3B8', dash='dash')
                ))
                fig.add_trace(go.Scatter(
                    x=years, y=with_promotion,
                    name='With Promotion',
                    line=dict(color='#10B981', width=3),
                    fill='tonexty'
                ))
                fig.update_layout(
                    title="5-Year Salary Projection",
                    xaxis_title="Years",
                    yaxis_title="Salary ($)",
                    height=300,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True, key=f"salary_chart_{opp_idx}")
                
                # Financial summary
                lifetime_gain = sum(with_promotion) - sum(current_projection)
                
                # Calculate ROI safely
                if total_cost > 0:
                    roi_value = ((lifetime_gain - total_cost) / total_cost * 100)
                else:
                    roi_value = 0
                
                st.markdown(f"""
                **💰 Financial Impact (5 Years):**
                - **Immediate Increase:** ${target_salary - current_salary:,}
                - **Lifetime Earnings Gain:** ${lifetime_gain:,.0f}
                - **Total Investment:** ${total_cost:,.0f}
                - **Net Benefit:** ${lifetime_gain - total_cost:,.0f}
                - **ROI:** {roi_value:.0f}%
                """)
        
        st.markdown("<br>", unsafe_allow_html=True)

# ==================== ANALYTICS & ROI PAGE ====================
elif page == "📊 Analytics & ROI":
    st.header("Training Analytics & ROI Dashboard")
    
    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_employees = len(st.session_state.employees)
    total_skills = sum(len(emp['current_skills']) for emp in st.session_state.employees)
    total_learning_goals = sum(len(emp['learning_goals']) for emp in st.session_state.employees)
    avg_skills_per_employee = total_skills / total_employees if total_employees > 0 else 0
    
    with col1:
        st.metric("Total Training ROI", "+$1.2M", delta="↑ 18% YoY")
    with col2:
        st.metric("Avg Skills/Employee", f"{avg_skills_per_employee:.1f}", delta="+0.8")
    with col3:
        st.metric("Active Learning Paths", total_learning_goals, delta="+12")
    with col4:
        st.metric("Internal Mobility Rate", "23%", delta="+5%")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💰 ROI Analysis", "📈 Skills Trends", "🎯 Program Effectiveness", "🔮 Predictions"])
    
    with tab1:
        st.subheader("Training Investment ROI")
        
        # Calculate ROI for all priority skills
        roi_data = []
        for emp in st.session_state.employees:
            for goal in emp['learning_goals']:
                roi = calculate_training_roi(goal, emp.get('salary', 80000), 'High')
                roi_data.append({
                    'Employee': emp['name'],
                    'Skill': goal,
                    'Investment': roi['total_cost'],
                    'Annual Value': roi['annual_value'],
                    'ROI %': roi['roi_percentage'],
                    'Payback (months)': roi['payback_months'],
                    'Training Type': roi['training_type']
                })
        
        if roi_data:
            df_roi = pd.DataFrame(roi_data)
            
            # ROI scatter plot
            fig = px.scatter(df_roi, 
                           x='Investment', 
                           y='ROI %',
                           size='Annual Value',
                           color='Training Type',
                           hover_data=['Employee', 'Skill'],
                           title='Training Investment vs ROI')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key="roi_scatter")
            
            # Top ROI opportunities
            st.subheader("🏆 Top ROI Training Opportunities")
            top_roi = df_roi.nlargest(10, 'ROI %')
            st.dataframe(top_roi, use_container_width=True)
            
            # Summary stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Investment", f"${df_roi['Investment'].sum():,.0f}")
            with col2:
                st.metric("Total Annual Value", f"${df_roi['Annual Value'].sum():,.0f}")
            with col3:
                avg_roi = df_roi['ROI %'].mean()
                st.metric("Average ROI", f"{avg_roi:.0f}%")
        else:
            st.info("No active learning goals to analyze. Add learning goals to see ROI projections.")
    
    with tab2:
        st.subheader("Skills Acquisition Trends")
        
        # Simulated monthly skills growth
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        skills_acquired = [15, 22, 28, 35, 42, 48]
        certifications = [2, 3, 3, 5, 6, 8]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=skills_acquired, name='Skills Acquired',
                                line=dict(color='#0EA5E9', width=3)))
        fig.add_trace(go.Scatter(x=months, y=certifications, name='Certifications',
                                line=dict(color='#10B981', width=3)))
        fig.update_layout(
            title="Skills & Certifications Growth (2024)",
            xaxis_title="Month",
            yaxis_title="Count",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True, key="skills_trends")
        
        # Skills by category over time
        st.subheader("Skills Distribution by Category")
        categories = list(SKILL_CATEGORIES.keys())
        category_counts = []
        for category in categories:
            count = 0
            for emp in st.session_state.employees:
                for skill in emp['current_skills']:
                    for skill_type in SKILL_CATEGORIES[category].values():
                        if skill in skill_type:
                            count += 1
            category_counts.append(count)
        
        fig = go.Figure(data=[
            go.Bar(x=categories, y=category_counts,
                  marker=dict(color=['#0EA5E9', '#10B981', '#F59E0B', '#8B5CF6', '#EF4444']))
        ])
        fig.update_layout(
            title="Current Skills by Category",
            xaxis_title="Category",
            yaxis_title="Number of Skills",
            height=350
        )
        st