from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

# Demo data - simplified for reliability
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

# Global user data storage (in production, use database)
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

# Routes with error handling
@app.get("/")
async def root():
    return {"message": "Career Autopilot API is running", "status": "healthy"}

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
