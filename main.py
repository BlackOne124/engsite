from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional
import os

app = FastAPI(title="Career Autopilot", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class UserData(BaseModel):
    level: int = 1
    xp: int = 0
    coins: int = 0
    badges: List[str] = []
    completed_quests: List[int] = []
    career_path: Optional[str] = None
    skills_progress: Dict[str, int] = {}
    selected_goals: List[str] = []
    completed_goals: List[str] = []
    daily_streak: int = 1
    total_quests_completed: int = 0
    total_xp_earned: int = 0
    total_coins_earned: int = 0
    last_login: str = ""

class QuestCompletion(BaseModel):
    quest_id: int

class GoalUpdate(BaseModel):
    goal_id: str
    completed: bool

class AIChatMessage(BaseModel):
    message: str

class CareerPathSelect(BaseModel):
    career_path: str

# Demo data
CAREER_PATHS = {
    "Data Scientist": {
        "skills": ["Python", "SQL", "Machine Learning", "Statistics", "Data Visualization"],
        "description": "Specialist in data analysis and ML model building"
    },
    "Frontend Developer": {
        "skills": ["JavaScript", "React", "HTML/CSS", "TypeScript", "UI/UX"],
        "description": "User interface developer"
    },
    "Project Manager": {
        "skills": ["Project Management", "Communication", "Agile", "Presentations", "Leadership"],
        "description": "Project and team leader"
    },
    "Team Lead": {
        "skills": ["Technical Leadership", "Team Management", "Mentoring", "Architecture", "Code Review"],
        "description": "Technical team leader"
    }
}

QUESTS = [
    {"id": 1, "name": "Complete Python course", "xp": 100, "coins": 50, "skill": "Python", "type": "education"},
    {"id": 2, "name": "Watch Agile webinar", "xp": 80, "coins": 40, "skill": "Agile", "type": "education"},
    {"id": 3, "name": "Read React article", "xp": 60, "coins": 30, "skill": "React", "type": "reading"},
    {"id": 4, "name": "Get colleague feedback", "xp": 120, "coins": 60, "skill": "Communication", "type": "social"},
    {"id": 5, "name": "Solve algorithm task", "xp": 150, "coins": 75, "skill": "Python", "type": "practice"},
    {"id": 6, "name": "Prepare presentation", "xp": 90, "coins": 45, "skill": "Presentations", "type": "practice"}
]

GOALS = {
    "short_term": [
        {"id": "goal_1", "name": "Reach level 5", "xp_reward": 200, "coins_reward": 100, "category": "progress"},
        {"id": "goal_2", "name": "Complete 5 quests", "xp_reward": 150, "coins_reward": 75, "category": "quests"},
        {"id": "goal_3", "name": "Get 3 badges", "xp_reward": 180, "coins_reward": 90, "category": "achievements"},
        {"id": "goal_4", "name": "Earn 500 coins", "xp_reward": 120, "coins_reward": 60, "category": "economy"},
        {"id": "goal_5", "name": "Choose career path", "xp_reward": 100, "coins_reward": 50, "category": "career"}
    ],
    "medium_term": [
        {"id": "goal_6", "name": "Master 3 new skills", "xp_reward": 300, "coins_reward": 150, "category": "skills"},
        {"id": "goal_7", "name": "Reach level 10", "xp_reward": 400, "coins_reward": 200, "category": "progress"},
        {"id": "goal_8", "name": "Complete AI career plan", "xp_reward": 350, "coins_reward": 175, "category": "career"},
        {"id": "goal_9", "name": "Get all learning badges", "xp_reward": 280, "coins_reward": 140, "category": "achievements"}
    ]
}

# Global user data storage
user_data_store = {}

def get_user_data(session_id: str = "default") -> UserData:
    if session_id not in user_data_store:
        user_data_store[session_id] = UserData(
            skills_progress={
                'Python': 65,
                'SQL': 40,
                'Machine Learning': 25,
                'Communication': 70,
                'Project Management': 35
            },
            last_login=datetime.now().isoformat()
        )
    return user_data_store[session_id]

def update_daily_streak(user_data: UserData):
    now = datetime.now()
    if user_data.last_login:
        try:
            last_login = datetime.fromisoformat(user_data.last_login)
            if (now.date() - last_login.date()).days == 1:
                user_data.daily_streak += 1
            elif (now.date() - last_login.date()).days > 1:
                user_data.daily_streak = 1
        except:
            user_data.daily_streak = 1
    user_data.last_login = now.isoformat()

def ai_assistant_response(message: str, user_data: UserData) -> dict:
    message_lower = message.lower()

    if any(word in message_lower for word in ['hi', 'hello', 'hey']):
        return {
            "type": "question",
            "text": "Hello! I'm your AI career assistant. Let's create your personal development plan. What career goal do you want to achieve in the next year?",
            "options": [
                "I want to become a Team Lead",
                "I plan to switch to Data Science",
                "I want promotion to Senior Developer",
                "I'm interested in Product Management"
            ]
        }
    elif "team lead" in message_lower:
        return {
            "type": "question",
            "text": "Excellent! How many years of experience do you have in development?",
            "options": [
                "Less than 1 year",
                "1-3 years",
                "3-5 years",
                "More than 5 years"
            ]
        }
    elif "data science" in message_lower:
        return {
            "type": "question",
            "text": "Great choice! What's your current experience in data analysis?",
            "options": [
                "Beginner, just starting",
                "Have basic Python/SQL knowledge",
                "Already worked with data in current role",
                "Experienced in related field"
            ]
        }
    else:
        return {
            "type": "final_plan",
            "text": f"""
🎯 **Your Career Development Plan:**

Based on your interest in **{message}**, here's your personalized plan:

**First Month: Foundation**
• Complete core skill assessments
• Identify knowledge gaps
• Set specific milestones

**Months 2-3: Skill Building**
• Focused learning path
• Practical projects
• Mentor sessions

**Months 4-6: Real-world Application**
• Internal projects
• Cross-team collaboration
• Portfolio development

🏆 **You earned:**
• 150 career coins
• 75 XP
• Goal Setter badge 🎯

Ready to begin your journey?
            """
        }

# HTML frontend
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Career Cosmos - Career Autopilot</title>
    <style>
        :root {
            --space-black: #0A0A14;
            --cosmic-purple: #6366F1;
            --nebula-blue: #3B82F6;
            --starlight-white: #F8FAFC;
            --comet-cyan: #06B6D4;
            --galaxy-gray: #1E293B;
            --orbit-silver: #64748B;
            --supernova-orange: #F59E0B;
            --quantum-green: #10B981;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: var(--space-black);
            color: var(--starlight-white);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Cosmic Background */
        .cosmic-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background:
                radial-gradient(ellipse at 20% 50%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 40% 80%, rgba(6, 182, 212, 0.05) 0%, transparent 50%);
        }

        .star {
            position: absolute;
            background: white;
            border-radius: 50%;
            animation: twinkle 4s infinite;
        }

        .star:nth-child(1) { top: 20%; left: 10%; width: 2px; height: 2px; animation-delay: 0s; }
        .star:nth-child(2) { top: 60%; left: 80%; width: 3px; height: 3px; animation-delay: 1s; }
        .star:nth-child(3) { top: 80%; left: 30%; width: 1px; height: 1px; animation-delay: 2s; }

        @keyframes twinkle {
            0%, 100% { opacity: 0.3; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.2); }
        }

        /* App Container */
        .app-container {
            display: flex;
            min-height: 100vh;
        }

        /* Cosmic Navigation */
        .cosmic-nav {
            width: 280px;
            background: rgba(10, 10, 20, 0.8);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(99, 102, 241, 0.2);
            padding: 30px 20px;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }

        .cosmic-nav::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--cosmic-purple), transparent);
        }

        .nav-brand {
            text-align: center;
            margin-bottom: 40px;
        }

        .logo-orb {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--cosmic-purple), var(--nebula-blue));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 15px;
            font-size: 24px;
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.4);
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        .nav-brand h1 {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--starlight-white), var(--comet-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .tagline {
            font-size: 12px;
            color: var(--orbit-silver);
            font-weight: 300;
        }

        /* User Orb */
        .user-orb {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
        }

        .user-avatar {
            position: relative;
            width: 100px;
            height: 100px;
            margin: 0 auto 15px;
        }

        .orbit {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 50%;
            animation: spin 20s linear infinite;
        }

        .satellite {
            position: absolute;
            top: -5px;
            left: 50%;
            width: 10px;
            height: 10px;
            background: var(--comet-cyan);
            border-radius: 50%;
            transform: translateX(-50%);
        }

        .user-core {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--galaxy-gray), var(--space-black));
            border: 2px solid var(--cosmic-purple);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .level-badge {
            background: linear-gradient(135deg, var(--cosmic-purple), var(--nebula-blue));
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 8px;
        }

        .xp-display {
            font-size: 12px;
            color: var(--orbit-silver);
        }

        /* Navigation Constellation */
        .nav-constellation {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .nav-star {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            background: rgba(30, 41, 59, 0.3);
            border: 1px solid transparent;
        }

        .nav-star:hover {
            background: rgba(99, 102, 241, 0.1);
            border-color: rgba(99, 102, 241, 0.3);
            transform: translateX(5px);
        }

        .nav-star.active {
            background: rgba(99, 102, 241, 0.15);
            border-color: var(--cosmic-purple);
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
        }

        .star-icon {
            font-size: 20px;
            margin-right: 12px;
            width: 24px;
            text-align: center;
        }

        .nav-star span {
            font-weight: 500;
            font-size: 14px;
        }

        .star-trail {
            position: absolute;
            top: 50%;
            right: 20px;
            width: 6px;
            height: 6px;
            background: var(--cosmic-purple);
            border-radius: 50%;
            transform: translateY(-50%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .nav-star.active .star-trail {
            opacity: 1;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: translateY(-50%) scale(1); }
            50% { opacity: 0.5; transform: translateY(-50%) scale(1.5); }
        }

        /* Cosmic Stats */
        .cosmic-stats {
            margin-top: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .stat-comet {
            text-align: center;
            position: relative;
            padding: 15px;
            background: rgba(30, 41, 59, 0.5);
            border-radius: 12px;
            border: 1px solid rgba(99, 102, 241, 0.2);
        }

        .comet-head {
            width: 20px;
            height: 20px;
            background: linear-gradient(135deg, var(--supernova-orange), var(--comet-cyan));
            border-radius: 50%;
            margin: 0 auto 10px;
            position: relative;
        }

        .comet-head::after {
            content: '';
            position: absolute;
            top: 50%;
            right: -30px;
            width: 30px;
            height: 2px;
            background: linear-gradient(90deg, var(--supernova-orange), transparent);
            transform: translateY(-50%);
        }

        .comet-value {
            font-size: 24px;
            font-weight: 700;
            color: var(--starlight-white);
            margin-bottom: 5px;
        }

        .comet-label {
            font-size: 12px;
            color: var(--orbit-silver);
        }

        .progress-ring {
            position: relative;
            width: 80px;
            height: 80px;
            margin: 0 auto;
        }

        .ring-back {
            fill: none;
            stroke: var(--galaxy-gray);
            stroke-width: 3;
        }

        .ring-front {
            fill: none;
            stroke: var(--cosmic-purple);
            stroke-width: 3;
            stroke-linecap: round;
            transform: rotate(-90deg);
            transform-origin: 50% 50%;
            transition: stroke-dasharray 0.3s ease;
        }

        .ring-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 12px;
            font-weight: 600;
            color: var(--starlight-white);
        }

        /* Main Content */
        .cosmic-main {
            flex: 1;
            padding: 30px;
            overflow-y: auto;
        }

        .mission-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(99, 102, 241, 0.2);
        }

        .header-orbit h2 {
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--starlight-white), var(--comet-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .mission-time {
            font-size: 14px;
            color: var(--orbit-silver);
            margin-top: 5px;
        }

        .signal-bars {
            display: flex;
            align-items: end;
            gap: 3px;
            height: 20px;
        }

        .bar {
            width: 4px;
            background: var(--quantum-green);
            border-radius: 2px;
            animation: signal 2s infinite;
        }

        .bar:nth-child(1) { height: 6px; animation-delay: 0s; }
        .bar:nth-child(2) { height: 10px; animation-delay: 0.2s; }
        .bar:nth-child(3) { height: 14px; animation-delay: 0.4s; }
        .bar:nth-child(4) { height: 18px; animation-delay: 0.6s; }

        @keyframes signal {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }

        /* Cosmic Sections */
        .cosmic-section {
            display: none;
        }

        .cosmic-section.active {
            display: block;
        }

        /* Constellation Grid */
        .constellation-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }

        .constellation-node {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 20px;
            padding: 25px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .constellation-node:hover {
            border-color: var(--cosmic-purple);
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.1);
        }

        .node-glow {
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .constellation-node:hover .node-glow {
            opacity: 1;
        }

        .node-content h3 {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--starlight-white);
        }

        .main-node {
            grid-column: 1 / -1;
        }

        /* Cosmic Notification */
        .cosmic-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(30, 41, 59, 0.9);
            backdrop-filter: blur(10px);
            border: 1px solid var(--cosmic-purple);
            border-radius: 12px;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            transform: translateX(400px);
            transition: transform 0.3s ease;
            z-index: 1000;
        }

        .cosmic-notification.show {
            transform: translateX(0);
        }

        .notification-comet {
            position: relative;
            width: 30px;
            height: 30px;
        }

        .comet-core {
            width: 12px;
            height: 12px;
            background: var(--supernova-orange);
            border-radius: 50%;
            position: relative;
            z-index: 2;
        }

        .comet-tail {
            position: absolute;
            top: 50%;
            right: -20px;
            width: 20px;
            height: 2px;
            background: linear-gradient(90deg, var(--supernova-orange), transparent);
            transform: translateY(-50%);
        }

        .notification-message {
            font-size: 14px;
            font-weight: 500;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .app-container {
                flex-direction: column;
            }

            .cosmic-nav {
                width: 100%;
                height: auto;
            }

            .constellation-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Dashboard specific styles */
        .mission-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }

        .mission-stat {
            text-align: center;
            padding: 20px;
            background: rgba(30, 41, 59, 0.6);
            border-radius: 12px;
            border: 1px solid rgba(99, 102, 241, 0.2);
        }

        .mission-stat .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: var(--comet-cyan);
            margin-bottom: 5px;
        }

        .mission-stat .stat-label {
            font-size: 12px;
            color: var(--orbit-silver);
        }

        .mission-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 30px;
        }

        .mission-item {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }

        .mission-icon {
            font-size: 20px;
        }

        .mission-info {
            flex: 1;
        }

        .mission-name {
            font-weight: 500;
            margin-bottom: 5px;
        }

        .mission-progress {
            width: 100%;
        }

        .progress-bar {
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--comet-cyan), var(--cosmic-purple));
            border-radius: 3px;
            transition: width 0.3s ease;
        }

        .objectives-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .objective-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .objective-card:hover {
            border-color: var(--cosmic-purple);
            transform: translateY(-2px);
        }

        .objective-icon {
            font-size: 24px;
            margin-bottom: 10px;
        }

        .objective-text {
            font-size: 14px;
            font-weight: 500;
        }

        /* Loading states */
        .loading {
            text-align: center;
            padding: 40px;
            color: var(--orbit-silver);
            font-style: italic;
        }

        .loading::after {
            content: '';
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid var(--orbit-silver);
            border-top: 2px solid var(--cosmic-purple);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="cosmic-bg">
        <div class="star"></div>
        <div class="star"></div>
        <div class="star"></div>
    </div>

    <!-- Cosmic Notification -->
    <div id="notification" class="cosmic-notification">
        <div class="notification-comet">
            <div class="comet-core"></div>
            <div class="comet-tail"></div>
        </div>
        <div class="notification-message">Career Cosmos initialized!</div>
    </div>

    <div class="app-container">
        <!-- Cosmic Navigation -->
        <nav class="cosmic-nav">
            <div class="nav-brand">
                <div class="logo-orb">🚀</div>
                <h1>Career Cosmos</h1>
                <div class="tagline">Your Career Development Platform</div>
            </div>

            <div class="user-orb">
                <div class="user-avatar">
                    <div class="orbit">
                        <div class="satellite"></div>
                    </div>
                    <div class="user-core">👨‍🚀</div>
                </div>
                <div class="user-info">
                    <div class="level-badge">Level <span id="user-level">1</span></div>
                    <div class="xp-display"><span id="user-xp">0</span> XP • <span id="user-coins">0</span> 🪙</div>
                </div>
            </div>

            <div class="nav-constellation">
                <div class="nav-star active" data-section="dashboard">
                    <div class="star-icon">🌌</div>
                    <span>Mission Control</span>
                    <div class="star-trail"></div>
                </div>
                <div class="nav-star" data-section="profile">
                    <div class="star-icon">👨‍🚀</div>
                    <span>Astronaut Profile</span>
                    <div class="star-trail"></div>
                </div>
                <div class="nav-star" data-section="galaxy">
                    <div class="star-icon">🌠</div>
                    <span>Career Galaxy</span>
                    <div class="star-trail"></div>
                </div>
                <div class="nav-star" data-section="quests">
                    <div class="star-icon">🎯</div>
                    <span>Space Missions</span>
                    <div class="star-trail"></div>
                </div>
                <div class="nav-star" data-section="goals">
                    <div class="star-icon">⭐</div>
                    <span>Stellar Goals</span>
                    <div class="star-trail"></div>
                </div>
                <div class="nav-star" data-section="ai">
                    <div class="star-icon">🤖</div>
                    <span>AI Navigator</span>
                    <div class="star-trail"></div>
                </div>
                <div class="nav-star" data-section="achievements">
                    <div class="star-icon">🏆</div>
                    <span>Cosmic Badges</span>
                    <div class="star-trail"></div>
                </div>
            </div>

            <div class="cosmic-stats">
                <div class="stat-comet">
                    <div class="progress-ring">
                        <svg width="80" height="80">
                            <circle class="ring-back" cx="40" cy="40" r="35"></circle>
                            <circle id="xp-ring" class="ring-front" cx="40" cy="40" r="35"></circle>
                        </svg>
                        <div class="ring-text" id="xp-percent">0%</div>
                    </div>
                </div>
                <div class="stat-comet">
                    <div class="comet-head"></div>
                    <div class="comet-value" id="total-quests">0</div>
                    <div class="comet-label">Missions Completed</div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <main class="cosmic-main">
            <div class="mission-header">
                <div class="header-orbit">
                    <h2 id="page-title">Mission Control</h2>
                    <div class="mission-time" id="current-date">Loading mission time...</div>
                </div>
                <div class="signal-bars">
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                </div>
            </div>

            <!-- Dashboard Section -->
            <section id="dashboard" class="cosmic-section active">
                <div class="constellation-grid">
                    <div class="constellation-node main-node">
                        <div class="node-glow"></div>
                        <div class="node-content">
                            <h3>Mission Statistics</h3>
                            <div class="mission-stats" id="mission-stats">
                                <div class="mission-stat">
                                    <div class="stat-value">1</div>
                                    <div class="stat-label">Current Orbit</div>
                                </div>
                                <div class="mission-stat">
                                    <div class="stat-value">0</div>
                                    <div class="stat-label">Missions Completed</div>
                                </div>
                                <div class="mission-stat">
                                    <div class="stat-value">1</div>
                                    <div class="stat-label">Consecutive Days</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="constellation-node">
                        <div class="node-glow"></div>
                        <div class="node-content">
                            <h3>Active Missions</h3>
                            <div class="mission-list" id="active-missions">
                                <div class="mission-item">
                                    <div class="mission-icon">🎯</div>
                                    <div class="mission-info">
                                        <div class="mission-name">Skill Development</div>
                                        <div class="mission-progress">
                                            <div class="progress-bar">
                                                <div class="progress-fill" style="width: 65%"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="constellation-node">
                        <div class="node-glow"></div>
                        <div class="node-content">
                            <h3>Current Objectives</h3>
                            <div class="objectives-grid" id="objectives-grid">
                                <div class="objective-card">
                                    <div class="objective-icon">⭐</div>
                                    <div class="objective-text">Reach Level 2</div>
                                </div>
                                <div class="objective-card">
                                    <div class="objective-icon">🏆</div>
                                    <div class="objective-text">Earn 3 Badges</div>
                                </div>
                                <div class="objective-card">
                                    <div class="objective-icon">💫</div>
                                    <div class="objective-text">Complete 5 Missions</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Other Sections (simplified for demo) -->
            <section id="profile" class="cosmic-section">
                <div class="constellation-node main-node">
                    <div class="node-content">
                        <h3>Astronaut Profile</h3>
                        <div class="loading">Loading astronaut data...</div>
                    </div>
                </div>
            </section>

            <section id="galaxy" class="cosmic-section">
                <div class="constellation-node main-node">
                    <div class="node-content">
                        <h3>Career Galaxy</h3>
                        <div class="loading">Exploring career paths...</div>
                    </div>
                </div>
            </section>

            <section id="quests" class="cosmic-section">
                <div class="constellation-node main-node">
                    <div class="node-content">
                        <h3>Space Missions</h3>
                        <div class="loading">Scanning available missions...</div>
                    </div>
                </div>
            </section>

            <section id="goals" class="cosmic-section">
                <div class="constellation-node main-node">
                    <div class="node-content">
                        <h3>Stellar Goals</h3>
                        <div class="loading">Aligning cosmic objectives...</div>
                    </div>
                </div>
            </section>

            <section id="ai" class="cosmic-section">
                <div class="constellation-node main-node">
                    <div class="node-content">
                        <h3>AI Navigator</h3>
                        <div class="loading">Initializing AI assistant...</div>
                    </div>
                </div>
            </section>

            <section id="achievements" class="cosmic-section">
                <div class="constellation-node main-node">
                    <div class="node-content">
                        <h3>Cosmic Badges</h3>
                        <div class="loading">Loading achievements...</div>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <script>
        class CareerCosmos {
            constructor() {
                this.userData = null;
                this.currentSection = 'dashboard';
                this.init();
            }

            async init() {
                await this.loadUserData();
                this.setupEventListeners();
                this.updateUI();
                this.setupAnimations();
                this.showNotification('Career Cosmos initialized! Ready for launch! 🚀');
            }

            async loadUserData() {
                try {
                    const response = await fetch('/api/user');
                    if (!response.ok) throw new Error('API response not OK');
                    this.userData = await response.json();
                } catch (error) {
                    console.error('Error loading user data:', error);
                    // Fallback data
                    this.userData = {
                        level: 1,
                        xp: 0,
                        coins: 0,
                        badges: [],
                        completed_quests: [],
                        career_path: null,
                        skills_progress: {
                            'Python': 65,
                            'SQL': 40,
                            'Machine Learning': 25,
                            'Communication': 70,
                            'Project Management': 35
                        },
                        selected_goals: [],
                        completed_goals: [],
                        daily_streak: 1,
                        total_quests_completed: 0,
                        total_xp_earned: 0,
                        total_coins_earned: 0,
                        last_login: new Date().toISOString()
                    };
                    this.showNotification('Using demo data - some features limited');
                }
            }

            setupEventListeners() {
                // Navigation
                document.querySelectorAll('.nav-star').forEach(star => {
                    star.addEventListener('click', (e) => {
                        const section = e.currentTarget.getAttribute('data-section');
                        this.navigateToSection(section);
                    });
                });
            }

            navigateToSection(section) {
                // Update navigation
                document.querySelectorAll('.nav-star').forEach(star => {
                    star.classList.remove('active');
                });
                document.querySelector(`[data-section="${section}"]`).classList.add('active');

                // Update sections
                document.querySelectorAll('.cosmic-section').forEach(sec => {
                    sec.classList.remove('active');
                });
                document.getElementById(section).classList.add('active');

                // Update title
                const titles = {
                    'dashboard': 'Mission Control',
                    'profile': 'Astronaut Profile',
                    'galaxy': 'Career Galaxy',
                    'quests': 'Space Missions',
                    'goals': 'Stellar Goals',
                    'ai': 'AI Navigator',
                    'achievements': 'Cosmic Badges'
                };
                document.getElementById('page-title').textContent = titles[section] || 'Career Cosmos';

                this.currentSection = section;
            }

            updateUI() {
                if (!this.userData) return;

                // Update user info
                document.getElementById('user-level').textContent = this.userData.level;
                document.getElementById('user-xp').textContent = this.userData.xp;
                document.getElementById('user-coins').textContent = this.userData.coins;

                // Update progress ring
                this.updateProgressRing();

                // Update mission stats
                this.updateMissionStats();

                // Update date
                this.updateMissionTime();
            }

            updateProgressRing() {
                if (!this.userData) return;

                const xpNeeded = this.userData.level * 100;
                const progressPercent = (this.userData.xp / xpNeeded) * 100;
                const circumference = 2 * Math.PI * 35;
                const offset = circumference - (progressPercent / 100) * circumference;

                const ring = document.getElementById('xp-ring');
                const percentText = document.getElementById('xp-percent');

                if (ring && percentText) {
                    ring.style.strokeDasharray = `${circumference} ${circumference}`;
                    ring.style.strokeDashoffset = offset;
                    percentText.textContent = `${Math.round(progressPercent)}%`;
                }
            }

            updateMissionStats() {
                const missionStats = document.getElementById('mission-stats');
                if (missionStats && this.userData) {
                    missionStats.innerHTML = `
                        <div class="mission-stat">
                            <div class="stat-value">${this.userData.level}</div>
                            <div class="stat-label">Current Orbit</div>
                        </div>
                        <div class="mission-stat">
                            <div class="stat-value">${this.userData.total_quests_completed || 0}</div>
                            <div class="stat-label">Missions Completed</div>
                        </div>
                        <div class="mission-stat">
                            <div class="stat-value">${this.userData.daily_streak}</div>
                            <div class="stat-label">Consecutive Days</div>
                        </div>
                    `;
                }

                // Update total quests in sidebar
                const totalQuests = document.getElementById('total-quests');
                if (totalQuests) {
                    totalQuests.textContent = this.userData.total_quests_completed || 0;
                }
            }

            updateMissionTime() {
                const now = new Date();
                const options = {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                };
                document.getElementById('current-date').textContent = 
                    `Mission Time: ${now.toLocaleDateString('en-US', options)}`;
            }

            setupAnimations() {
                // Add stars to background
                this.createStars();
            }

            createStars() {
                const cosmicBg = document.querySelector('.cosmic-bg');
                for (let i = 0; i < 20; i++) {
                    const star = document.createElement('div');
                    star.className = 'star';
                    star.style.top = `${Math.random() * 100}%`;
                    star.style.left = `${Math.random() * 100}%`;
                    star.style.width = `${Math.random() * 3 + 1}px`;
                    star.style.height = star.style.width;
                    star.style.animationDelay = `${Math.random() * 4}s`;
                    cosmicBg.appendChild(star);
                }
            }

            showNotification(message) {
                const notification = document.getElementById('notification');
                const messageEl = notification.querySelector('.notification-message');

                messageEl.textContent = message;
                notification.classList.add('show');

                setTimeout(() => {
                    notification.classList.remove('show');
                }, 4000);
            }
        }

        // Initialize the application
        document.addEventListener('DOMContentLoaded', () => {
            new CareerCosmos();
        });
    </script>
</body>
</html>
"""

# Routes
@app.get("/")
async def read_root():
    return HTMLResponse(content=HTML_CONTENT)

@app.get("/api/user")
async def get_user(session_id: str = "default"):
    try:
        user_data = get_user_data(session_id)
        update_daily_streak(user_data)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user data: {str(e)}")

@app.get("/api/career_paths")
async def get_career_paths():
    try:
        return CAREER_PATHS
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching career paths: {str(e)}")

@app.get("/api/quests")
async def get_quests():
    try:
        return QUESTS
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quests: {str(e)}")

@app.get("/api/goals")
async def get_goals():
    try:
        return GOALS
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching goals: {str(e)}")

@app.post("/api/complete_quest")
async def complete_quest(quest: QuestCompletion, session_id: str = "default"):
    try:
        user_data = get_user_data(session_id)

        if quest.quest_id not in user_data.completed_quests:
            quest_data = next((q for q in QUESTS if q["id"] == quest.quest_id), None)
            if quest_data:
                user_data.xp += quest_data["xp"]
                user_data.coins += quest_data["coins"]
                user_data.completed_quests.append(quest.quest_id)
                user_data.total_quests_completed += 1
                user_data.total_xp_earned += quest_data["xp"]
                user_data.total_coins_earned += quest_data["coins"]

                # Level up check
                xp_needed = user_data.level * 100
                if user_data.xp >= xp_needed:
                    user_data.level += 1
                    user_data.xp = 0

                # Badge checks
                if quest_data["skill"] == "Python" and "python_beginner" not in user_data.badges:
                    user_data.badges.append("python_beginner")

                if len(user_data.completed_quests) >= 3 and "active_learner" not in user_data.badges:
                    user_data.badges.append("active_learner")

                return {"success": True, "user_data": user_data}

        return {"success": False, "message": "Quest already completed or not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error completing quest: {str(e)}")

@app.post("/api/select_career")
async def select_career(request: CareerPathSelect, session_id: str = "default"):
    try:
        user_data = get_user_data(session_id)
        user_data.career_path = request.career_path
        
        # Award badge for selecting career path
        if "goal_setter" not in user_data.badges:
            user_data.badges.append("goal_setter")
            user_data.coins += 50
            user_data.xp += 25
            
        return {"success": True, "user_data": user_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error selecting career path: {str(e)}")

@app.post("/api/select_goal")
async def select_goal(goal_id: str, session_id: str = "default"):
    try:
        user_data = get_user_data(session_id)
        if goal_id not in user_data.selected_goals:
            user_data.selected_goals.append(goal_id)
        return {"success": True, "user_data": user_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error selecting goal: {str(e)}")

@app.post("/api/toggle_goal")
async def toggle_goal(goal: GoalUpdate, session_id: str = "default"):
    try:
        user_data = get_user_data(session_id)

        if goal.completed and goal.goal_id not in user_data.completed_goals:
            user_data.completed_goals.append(goal.goal_id)

            # Find goal reward
            reward_given = False
            for category in GOALS.values():
                for g in category:
                    if g["id"] == goal.goal_id:
                        user_data.xp += g["xp_reward"]
                        user_data.coins += g["coins_reward"]
                        user_data.total_xp_earned += g["xp_reward"]
                        user_data.total_coins_earned += g["coins_reward"]
                        reward_given = True
                        
                        if "goal_setter" not in user_data.badges:
                            user_data.badges.append("goal_setter")
                        break
                if reward_given:
                    break

        elif not goal.completed and goal.goal_id in user_data.completed_goals:
            user_data.completed_goals.remove(goal.goal_id)

        return {"success": True, "user_data": user_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error toggling goal: {str(e)}")

@app.post("/api/ai_chat")
async def ai_chat(message: AIChatMessage, session_id: str = "default"):
    try:
        user_data = get_user_data(session_id)
        response = ai_assistant_response(message.message, user_data)

        # Award for first AI interaction
        if "goal_setter" not in user_data.badges:
            user_data.badges.append("goal_setter")
            user_data.coins += 100
            user_data.xp += 50

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in AI chat: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
