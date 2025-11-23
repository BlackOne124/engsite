class CareerCosmos {
    constructor() {
        this.userData = null;
        this.currentSection = 'dashboard';
        this.aiState = null;
        this.aiAnswers = {};
        this.init();
    }

    async init() {
        await this.loadUserData();
        this.setupEventListeners();
        this.updateUI();
        this.setupAnimations();
    }

    async loadUserData() {
        try {
            const response = await fetch('/api/user');
            this.userData = await response.json();
        } catch (error) {
            console.error('Error loading cosmic data:', error);
            this.showNotification('Connection to mission control lost');
        }
    }

    setupEventListeners() {
        // Navigation stars
        document.querySelectorAll('.nav-star').forEach(star => {
            star.addEventListener('click', (e) => {
                const section = e.currentTarget.getAttribute('data-section');
                this.navigateToSection(section);
            });
        });

        // AI Chat
        document.getElementById('send-ai-message').addEventListener('click', () => this.sendAIMessage());
        document.getElementById('ai-chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendAIMessage();
        });

        // Quick questions
        document.querySelectorAll('.quick-question').forEach(button => {
            button.addEventListener('click', (e) => {
                const question = e.target.getAttribute('data-question');
                document.getElementById('ai-chat-input').value = question;
                this.sendAIMessage();
            });
        });

        // Cosmic background interactions
        document.addEventListener('mousemove', this.handleMouseMove.bind(this));
    }

    setupAnimations() {
        this.updateProgressRing();
        this.startCosmicAnimations();
    }

    navigateToSection(section) {
        // Update active navigation
        document.querySelectorAll('.nav-star').forEach(star => {
            star.classList.remove('active');
        });
        document.querySelector(`[data-section="${section}"]`).classList.add('active');

        // Update active section
        document.querySelectorAll('.cosmic-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(section).classList.add('active');

        // Update page title
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

        // Load section-specific data
        this.loadSectionData(section);
    }

    loadSectionData(section) {
        switch(section) {
            case 'profile':
                this.updateProfile();
                break;
            case 'galaxy':
                this.updateGalaxy();
                break;
            case 'quests':
                this.updateQuests();
                break;
            case 'goals':
                this.updateGoals();
                break;
            case 'achievements':
                this.updateAchievements();
                break;
        }
    }

    updateUI() {
        if (!this.userData) return;

        // Update user info
        document.getElementById('user-level').textContent = this.userData.level;
        document.getElementById('user-xp').textContent = this.userData.xp;
        document.getElementById('user-coins').textContent = this.userData.coins;

        // Update progress ring
        this.updateProgressRing();

        // Update career progress spacecraft
        this.updateCareerProgress();

        // Update date
        this.updateMissionTime();

        // Update dashboard content
        this.updateDashboard();
    }

    updateProgressRing() {
        if (!this.userData) return;

        const xpNeeded = this.userData.level * 100;
        const progressPercent = (this.userData.xp / xpNeeded) * 100;
        const circumference = 2 * Math.PI * 35;
        const offset = circumference - (progressPercent / 100) * circumference;

        const ring = document.getElementById('xp-ring');
        if (ring) {
            ring.style.strokeDasharray = `${circumference} ${circumference}`;
            ring.style.strokeDashoffset = offset;
        }
    }

    updateCareerProgress() {
        if (!this.userData) return;

        const xpNeeded = this.userData.level * 100;
        const progressPercent = (this.userData.xp / xpNeeded) * 100;
        const spacecraft = document.getElementById('career-progress');

        if (spacecraft) {
            spacecraft.style.left = `${progressPercent}%`;
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

    updateDashboard() {
        if (!this.userData) return;

        // Mission stats
        const missionStats = document.getElementById('mission-stats');
        if (missionStats) {
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

        // Active missions
        this.updateActiveMissions();

        // Objectives grid
        this.updateObjectives();
    }

    updateActiveMissions() {
        const activeMissions = document.getElementById('active-missions');
        if (!activeMissions) return;

        activeMissions.innerHTML = `
            <div class="mission-item">
                <div class="mission-icon">🎯</div>
                <div class="mission-info">
                    <div class="mission-name">Skill Development</div>
                    <div class="mission-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${(this.userData.skills_progress?.Python || 0)}%"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mission-item">
                <div class="mission-icon">🚀</div>
                <div class="mission-info">
                    <div class="mission-name">Career Advancement</div>
                    <div class="mission-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${(this.userData.xp / (this.userData.level * 100)) * 100}%"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mission-item">
                <div class="mission-icon">⭐</div>
                <div class="mission-info">
                    <div class="mission-name">Goal Completion</div>
                    <div class="mission-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${(this.userData.completed_goals?.length / 5) * 100 || 0}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    updateObjectives() {
        const objectivesGrid = document.getElementById('objectives-grid');
        if (!objectivesGrid) return;

        objectivesGrid.innerHTML = `
            <div class="objective-card">
                <div class="objective-icon">⭐</div>
                <div class="objective-text">Reach Level ${this.userData.level + 1}</div>
            </div>
            <div class="objective-card">
                <div class="objective-icon">🏆</div>
                <div class="objective-text">Earn 3 Badges</div>
            </div>
            <div class="objective-card">
                <div class="objective-icon">💫</div>
                <div class="objective-text">Complete 5 Missions</div>
            </div>
        `;
    }

    // Profile Section
    updateProfile() {
        if (!this.userData) return;

        // Update profile info
        const profileLevel = document.getElementById('profile-level');
        const profileStreak = document.getElementById('profile-streak');

        if (profileLevel) profileLevel.textContent = this.userData.level;
        if (profileStreak) profileStreak.textContent = `🔥 ${this.userData.daily_streak}-day streak`;

        // Update skills
        this.updateSkills();

        // Update profile stats
        this.updateProfileStats();
    }

    updateSkills() {
        const skillsUniverse = document.getElementById('skills-universe');
        if (!skillsUniverse || !this.userData.skills_progress) return;

        let skillsHTML = '';
        for (const [skill, progress] of Object.entries(this.userData.skills_progress)) {
            skillsHTML += `
                <div class="skill-planet">
                    <div class="planet-progress">
                        <div class="progress-ring small">
                            <svg width="60" height="60">
                                <circle class="ring-back" cx="30" cy="30" r="25"></circle>
                                <circle class="ring-front" cx="30" cy="30" r="25" style="stroke-dashoffset: ${157 - (progress / 100) * 157}"></circle>
                            </svg>
                        </div>
                        <div class="skill-name">${skill}</div>
                    </div>
                    <div class="skill-percent">${progress}%</div>
                </div>
            `;
        }
        skillsUniverse.innerHTML = skillsHTML;
    }

    updateProfileStats() {
        const profileStats = document.getElementById('profile-stats');
        if (!profileStats) return;

        profileStats.innerHTML = `
            <div class="profile-stat">
                <div class="stat-icon">🚀</div>
                <div class="stat-data">
                    <div class="stat-value">${this.userData.total_quests_completed || 0}</div>
                    <div class="stat-label">Missions Completed</div>
                </div>
            </div>
            <div class="profile-stat">
                <div class="stat-icon">⭐</div>
                <div class="stat-data">
                    <div class="stat-value">${this.userData.badges?.length || 0}</div>
                    <div class="stat-label">Badges Earned</div>
                </div>
            </div>
            <div class="profile-stat">
                <div class="stat-icon">💫</div>
                <div class="stat-data">
                    <div class="stat-value">${this.userData.total_xp_earned || 0}</div>
                    <div class="stat-label">Total XP</div>
                </div>
            </div>
            <div class="profile-stat">
                <div class="stat-icon">🪙</div>
                <div class="stat-data">
                    <div class="stat-value">${this.userData.total_coins_earned || 0}</div>
                    <div class="stat-label">Total Coins</div>
                </div>
            </div>
        `;
    }

    // Galaxy Section
    async updateGalaxy() {
        try {
            const response = await fetch('/api/career_paths');
            const careerPaths = await response.json();

            const galaxyMap = document.getElementById('galaxy-map');
            if (galaxyMap) {
                let galaxyHTML = '';
                for (const [path, data] of Object.entries(careerPaths)) {
                    const isSelected = this.userData.career_path === path;
                    galaxyHTML += `
                        <div class="career-galaxy ${isSelected ? 'selected' : ''}" data-path="${path}">
                            <div class="galaxy-core">
                                <div class="core-glow"></div>
                                <div class="galaxy-name">${path}</div>
                            </div>
                            <div class="galaxy-description">${data.description}</div>
                            <div class="galaxy-skills">
                                ${data.skills.map(skill => `<span class="skill-star">${skill}</span>`).join('')}
                            </div>
                            ${!isSelected ? `<button class="select-galaxy" data-path="${path}">Explore This Galaxy</button>` : ''}
                        </div>
                    `;
                }
                galaxyMap.innerHTML = galaxyHTML;

                // Add event listeners for galaxy selection
                document.querySelectorAll('.select-galaxy').forEach(button => {
                    button.addEventListener('click', async (e) => {
                        const path = e.target.getAttribute('data-path');
                        await this.selectCareerPath(path);
                    });
                });
            }

            // Update current galaxy
            this.updateCurrentGalaxy();
        } catch (error) {
            console.error('Error loading career paths:', error);
        }
    }

    async selectCareerPath(path) {
        try {
            const response = await fetch('/api/select_career', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ career_path: path })
            });

            if (response.ok) {
                await this.loadUserData();
                this.updateGalaxy();
                this.showNotification(`Now exploring the ${path} galaxy!`);
            }
        } catch (error) {
            console.error('Error selecting career path:', error);
        }
    }

    updateCurrentGalaxy() {
        const currentGalaxy = document.getElementById('current-galaxy');
        if (!currentGalaxy) return;

        if (this.userData.career_path) {
            currentGalaxy.innerHTML = `
                <div class="current-galaxy-info">
                    <div class="current-galaxy-name">${this.userData.career_path}</div>
                    <div class="exploration-progress">
                        <div class="progress-text">Exploration Progress</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: 30%"></div>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    // Quests Section
    async updateQuests() {
        try {
            const response = await fetch('/api/quests');
            const quests = await response.json();

            const missionsList = document.getElementById('missions-list');
            if (missionsList) {
                let missionsHTML = '';
                quests.forEach(quest => {
                    const isCompleted = this.userData.completed_quests?.includes(quest.id) || false;
                    missionsHTML += `
                        <div class="space-mission ${isCompleted ? 'completed' : ''}">
                            <div class="mission-icon">${this.getMissionIcon(quest.type)}</div>
                            <div class="mission-details">
                                <div class="mission-name">${quest.name}</div>
                                <div class="mission-rewards">
                                    <span class="reward-xp">⭐ ${quest.xp} XP</span>
                                    <span class="reward-coins">🪙 ${quest.coins} coins</span>
                                </div>
                                <div class="mission-skill">Skill: ${quest.skill}</div>
                            </div>
                            <button class="mission-action ${isCompleted ? 'completed-btn' : 'launch-btn'}" 
                                    data-id="${quest.id}" ${isCompleted ? 'disabled' : ''}>
                                ${isCompleted ? '✅ Completed' : '🚀 Launch Mission'}
                            </button>
                        </div>
                    `;
                });
                missionsList.innerHTML = missionsHTML;

                // Add event listeners for mission completion
                document.querySelectorAll('.launch-btn').forEach(button => {
                    button.addEventListener('click', async (e) => {
                        const questId = parseInt(e.target.getAttribute('data-id'));
                        await this.completeQuest(questId);
                    });
                });
            }

            // Update completed missions
            this.updateCompletedMissions();
        } catch (error) {
            console.error('Error loading quests:', error);
        }
    }

    getMissionIcon(type) {
        const icons = {
            'education': '📚',
            'reading': '📖',
            'social': '👥',
            'practice': '💻'
        };
        return icons[type] || '🎯';
    }

    updateCompletedMissions() {
        const completedMissions = document.getElementById('completed-missions');
        if (!completedMissions) return;

        const completedCount = this.userData.completed_quests?.length || 0;
        completedMissions.innerHTML = `
            <div class="completion-stats">
                <div class="completion-count">${completedCount} missions completed</div>
                <div class="completion-rate">${Math.round((completedCount / 6) * 100)}% completion rate</div>
            </div>
        `;
    }

    // Goals Section
    async updateGoals() {
        // This would typically fetch from API, but we'll use mock data for now
        const goalsUniverse = document.getElementById('goals-universe');
        if (goalsUniverse) {
            goalsUniverse.innerHTML = `
                <div class="stellar-goal active">
                    <div class="goal-orbit">
                        <div class="goal-core">
                            <div class="goal-icon">🚀</div>
                        </div>
                    </div>
                    <div class="goal-info">
                        <div class="goal-name">Reach Level 5</div>
                        <div class="goal-description">Advance to the next orbit in your career journey</div>
                        <div class="goal-reward">Reward: 200 XP + 100 coins</div>
                    </div>
                    <div class="goal-progress">
                        <div class="progress-text">${this.userData.level}/5</div>
                    </div>
                </div>
                <div class="stellar-goal">
                    <div class="goal-orbit">
                        <div class="goal-core">
                            <div class="goal-icon">⭐</div>
                        </div>
                    </div>
                    <div class="goal-info">
                        <div class="goal-name">Earn 3 Cosmic Badges</div>
                        <div class="goal-description">Collect badges by completing achievements</div>
                        <div class="goal-reward">Reward: 150 XP + 75 coins</div>
                    </div>
                    <div class="goal-progress">
                        <div class="progress-text">${this.userData.badges?.length || 0}/3</div>
                    </div>
                </div>
            `;
        }
    }

    // Achievements Section
    updateAchievements() {
        const badges = {
            "python_beginner": {"name": "Python Pioneer", "description": "Completed first Python mission", "icon": "🐍"},
            "active_learner": {"name": "Active Astronaut", "description": "Completed 5 space missions", "icon": "⭐"},
            "team_player": {"name": "Team Cosmonaut", "description": "Collaborated with fellow space explorers", "icon": "👥"},
            "goal_setter": {"name": "Goal Galaxy", "description": "Set your first stellar goal", "icon": "🎯"},
            "planner": {"name": "Master Planner", "description": "Created a cosmic career plan", "icon": "📋"}
        };

        const badgesConstellation = document.getElementById('badges-constellation');
        const availableBadges = document.getElementById('available-badges');

        if (badgesConstellation && availableBadges) {
            let earnedHTML = '';
            let availableHTML = '';

            for (const [badgeId, badge] of Object.entries(badges)) {
                const hasBadge = this.userData.badges?.includes(badgeId) || false;
                const badgeHTML = `
                    <div class="cosmic-badge ${hasBadge ? 'earned' : 'locked'}">
                        <div class="badge-icon">${badge.icon}</div>
                        <div class="badge-name">${badge.name}</div>
                        <div class="badge-description">${badge.description}</div>
                        <div class="badge-status">${hasBadge ? '✅ Earned' : '🔒 Locked'}</div>
                    </div>
                `;

                if (hasBadge) {
                    earnedHTML += badgeHTML;
                } else {
                    availableHTML += badgeHTML;
                }
            }

            badgesConstellation.innerHTML = earnedHTML || '<div class="no-badges">No badges earned yet</div>';
            availableBadges.innerHTML = availableHTML;
        }
    }

    // AI Navigator
    async sendAIMessage() {
        const input = document.getElementById('ai-chat-input');
        const message = input.value.trim();

        if (!message) return;

        this.addAIMessage(message, 'user');
        input.value = '';

        try {
            const response = await fetch('/api/ai_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            if (response.ok) {
                const data = await response.json();

                if (data.type === 'question') {
                    this.addAIQuestion(data.text, data.options);
                } else if (data.type === 'final_plan') {
                    this.addAIFinalPlan(data.text);
                    await this.loadUserData();
                } else {
                    this.addAIMessage(data.text, 'ai');
                }
            }
        } catch (error) {
            console.error('Error sending AI message:', error);
            this.addAIMessage('Sorry, I encountered a cosmic disturbance. Please try again.', 'ai');
        }
    }

    addAIMessage(message, sender) {
        const chatMessages = document.getElementById('ai-chat-messages');
        const messageElement = document.createElement('div');
        messageElement.className = `ai-message ${sender}-message`;
        messageElement.innerHTML = `
            <div class="message-avatar">${sender === 'user' ? '👨‍🚀' : '🤖'}</div>
            <div class="message-content">${message}</div>
        `;

        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    addAIQuestion(question, options) {
        const chatMessages = document.getElementById('ai-chat-messages');

        const questionElement = document.createElement('div');
        questionElement.className = 'ai-message ai-question';
        questionElement.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                ${question}
                <div class="ai-options">
                    ${options.map(option => 
                        `<button class="ai-option" data-option="${option}">${option}</button>`
                    ).join('')}
                </div>
            </div>
        `;

        chatMessages.appendChild(questionElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Add event listeners to options
        questionElement.querySelectorAll('.ai-option').forEach(button => {
            button.addEventListener('click', (e) => {
                const option = e.target.getAttribute('data-option');
                this.addAIMessage(option, 'user');
                this.sendAIOption(option);
            });
        });
    }

    addAIFinalPlan(plan) {
        const chatMessages = document.getElementById('ai-chat-messages');

        const planElement = document.createElement('div');
        planElement.className = 'ai-message ai-final-plan';
        planElement.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="final-plan">${plan.replace(/\n/g, '<br>')}</div>
            </div>
        `;

        chatMessages.appendChild(planElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        this.showNotification('Cosmic career plan generated! Check your mission control.');
    }

    async sendAIOption(option) {
        try {
            const response = await fetch('/api/ai_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: option })
            });

            if (response.ok) {
                const data = await response.json();

                if (data.type === 'question') {
                    this.addAIQuestion(data.text, data.options);
                } else if (data.type === 'final_plan') {
                    this.addAIFinalPlan(data.text);
                    await this.loadUserData();
                } else {
                    this.addAIMessage(data.text, 'ai');
                }
            }
        } catch (error) {
            console.error('Error sending AI option:', error);
            this.addAIMessage('Cosmic communication failed. Please retry.', 'ai');
        }
    }

    // Mission completion
    async completeQuest(questId) {
        try {
            const response = await fetch('/api/complete_quest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quest_id: questId })
            });

            if (response.ok) {
                const result = await response.json();
                if (result.success) {
                    this.userData = result.user_data;
                    this.updateUI();
                    this.showNotification('Mission accomplished! Stellar rewards received!');

                    // Refresh current section if it's quests
                    if (this.currentSection === 'quests') {
                        this.updateQuests();
                    }
                }
            }
        } catch (error) {
            console.error('Error completing mission:', error);
            this.showNotification('Mission failed to transmit');
        }
    }

    handleMouseMove(e) {
        const stars = document.querySelectorAll('.star');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;

        stars.forEach((star, index) => {
            const speed = (index + 1) * 0.0001;
            const x = (mouseX * speed * 100);
            const y = (mouseY * speed * 100);
            star.style.transform = `translate(${x}px, ${y}px)`;
        });
    }

    startCosmicAnimations() {
        const nodes = document.querySelectorAll('.constellation-node');
        nodes.forEach((node, index) => {
            node.style.animationDelay = `${index * 0.2}s`;
            node.classList.add('float-in');
        });
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

// Initialize the cosmic application
document.addEventListener('DOMContentLoaded', () => {
    new CareerCosmos();
});

// Add additional CSS for new components
const additionalStyles = `
    .float-in {
        animation: floatIn 0.6s ease-out forwards;
        opacity: 0;
        transform: translateY(30px);
    }

    @keyframes floatIn {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Profile Styles */
    .profile-display {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 20px 0;
    }

    .profile-avatar-large {
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, var(--cosmic-purple), var(--nebula-blue));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
    }

    .profile-info {
        flex: 1;
    }

    .profile-name {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .profile-level {
        color: var(--comet-cyan);
        margin-bottom: 10px;
    }

    .profile-streak {
        color: var(--supernova-orange);
        font-weight: 600;
    }

    .skills-universe {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }

    .skill-planet {
        text-align: center;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }

    .skill-name {
        font-size: 12px;
        margin-top: 8px;
        color: var(--orbit-silver);
    }

    .skill-percent {
        font-size: 14px;
        font-weight: 600;
        color: var(--comet-cyan);
        margin-top: 5px;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-top: 20px;
    }

    .profile-stat {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }

    .stat-icon {
        font-size: 24px;
    }

    .stat-value {
        font-size: 20px;
        font-weight: 700;
        color: var(--comet-cyan);
    }

    .stat-label {
        font-size: 12px;
        color: var(--orbit-silver);
    }

    /* Galaxy Styles */
    .galaxy-map {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }

    .career-galaxy {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }

    .career-galaxy:hover {
        border-color: var(--cosmic-purple);
        transform: translateY(-5px);
    }

    .career-galaxy.selected {
        border-color: var(--cosmic-purple);
        background: rgba(99, 102, 241, 0.1);
    }

    .galaxy-core {
        text-align: center;
        margin-bottom: 15px;
    }

    .core-glow {
        width: 60px;
        height: 60px;
        background: radial-gradient(circle, var(--cosmic-purple), transparent 70%);
        border-radius: 50%;
        margin: 0 auto 10px;
        animation: pulse 2s infinite;
    }

    .galaxy-name {
        font-size: 18px;
        font-weight: 600;
        color: var(--starlight-white);
    }

    .galaxy-description {
        font-size: 14px;
        color: var(--orbit-silver);
        margin-bottom: 15px;
        text-align: center;
    }

    .galaxy-skills {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin-bottom: 15px;
    }

    .skill-star {
        background: rgba(99, 102, 241, 0.2);
        color: var(--comet-cyan);
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
    }

    .select-galaxy {
        background: var(--cosmic-purple);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        width: 100%;
        transition: background 0.3s ease;
    }

    .select-galaxy:hover {
        background: var(--dark-purple);
    }

    .current-galaxy-info {
        text-align: center;
        padding: 30px;
    }

    .current-galaxy-name {
        font-size: 24px;
        font-weight: 700;
        color: var(--comet-cyan);
        margin-bottom: 20px;
    }

    /* Quests Styles */
    .missions-list {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-top: 20px;
    }

    .space-mission {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        transition: all 0.3s ease;
    }

    .space-mission:hover {
        border-color: var(--cosmic-purple);
    }

    .space-mission.completed {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.3);
    }

    .mission-icon {
        font-size: 24px;
    }

    .mission-details {
        flex: 1;
    }

    .mission-name {
        font-weight: 600;
        margin-bottom: 5px;
    }

    .mission-rewards {
        display: flex;
        gap: 15px;
        margin-bottom: 5px;
    }

    .reward-xp, .reward-coins {
        font-size: 12px;
        color: var(--orbit-silver);
    }

    .mission-skill {
        font-size: 12px;
        color: var(--comet-cyan);
    }

    .launch-btn, .completed-btn {
        background: var(--cosmic-purple);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.3s ease;
    }

    .launch-btn:hover {
        background: var(--dark-purple);
    }

    .completed-btn {
        background: var(--orbit-silver);
        cursor: not-allowed;
    }

    .completion-stats {
        text-align: center;
        padding: 30px;
    }

    .completion-count {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .completion-rate {
        color: var(--orbit-silver);
    }

    /* Goals Styles */
    .goals-universe {
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-top: 20px;
    }

    .stellar-goal {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        transition: all 0.3s ease;
    }

    .stellar-goal.active {
        border-color: var(--cosmic-purple);
        background: rgba(99, 102, 241, 0.1);
    }

    .goal-orbit {
        position: relative;
        width: 60px;
        height: 60px;
    }

    .goal-core {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--cosmic-purple), var(--nebula-blue));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }

    .goal-info {
        flex: 1;
    }

    .goal-name {
        font-weight: 600;
        margin-bottom: 5px;
    }

    .goal-description {
        font-size: 14px;
        color: var(--orbit-silver);
        margin-bottom: 5px;
    }

    .goal-reward {
        font-size: 12px;
        color: var(--comet-cyan);
    }

    .goal-progress {
        text-align: center;
    }

    .progress-text {
        font-weight: 600;
        color: var(--comet-cyan);
    }

    /* AI Chat Styles */
    .ai-chat-container {
        height: 500px;
        display: flex;
        flex-direction: column;
    }

    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .ai-message {
        display: flex;
        gap: 12px;
        max-width: 80%;
    }

    .user-message {
        align-self: flex-end;
        flex-direction: row-reverse;
    }

    .message-avatar {
        width: 40px;
        height: 40px;
        background: rgba(99, 102, 241, 0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
    }

    .user-message .message-avatar {
        background: rgba(6, 182, 212, 0.2);
    }

    .message-content {
        background: rgba(255, 255, 255, 0.05);
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }

    .user-message .message-content {
        background: rgba(6, 182, 212, 0.1);
        border-color: rgba(6, 182, 212, 0.3);
    }

    .ai-options {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 10px;
    }

    .ai-option {
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: var(--starlight-white);
        padding: 8px 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
    }

    .ai-option:hover {
        background: rgba(99, 102, 241, 0.3);
    }

    .ai-final-plan .message-content {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.3);
    }

    .final-plan {
        white-space: pre-line;
    }

    .chat-input-container {
        display: flex;
        gap: 10px;
        padding: 20px;
        border-top: 1px solid rgba(99, 102, 241, 0.2);
    }

    #ai-chat-input {
        flex: 1;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        padding: 12px;
        color: var(--starlight-white);
        font-family: inherit;
    }

    #ai-chat-input:focus {
        outline: none;
        border-color: var(--cosmic-purple);
    }

    #send-ai-message {
        background: var(--cosmic-purple);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        cursor: pointer;
        transition: background 0.3s ease;
    }

    #send-ai-message:hover {
        background: var(--dark-purple);
    }

    .quick-questions {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
        margin-top: 20px;
    }

    .quick-question {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: var(--starlight-white);
        padding: 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
    }

    .quick-question:hover {
        background: rgba(99, 102, 241, 0.2);
        transform: translateX(5px);
    }

    /* Achievements Styles */
    .badges-constellation, .available-badges {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }

    .cosmic-badge {
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        transition: all 0.3s ease;
    }

    .cosmic-badge.earned {
        border-color: var(--quantum-green);
        background: rgba(16, 185, 129, 0.1);
    }

    .cosmic-badge.locked {
        opacity: 0.6;
    }

    .badge-icon {
        font-size: 32px;
        margin-bottom: 10px;
    }

    .badge-name {
        font-weight: 600;
        margin-bottom: 5px;
    }

    .badge-description {
        font-size: 12px;
        color: var(--orbit-silver);
        margin-bottom: 10px;
    }

    .badge-status {
        font-size: 11px;
        font-weight: 600;
    }

    .earned .badge-status {
        color: var(--quantum-green);
    }

    .locked .badge-status {
        color: var(--orbit-silver);
    }

    .no-badges {
        text-align: center;
        color: var(--orbit-silver);
        font-style: italic;
        padding: 40px;
        grid-column: 1 / -1;
    }

    /* Progress bars */
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

    /* Mission stats in dashboard */
    .mission-stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
    }

    .mission-stat {
        text-align: center;
        padding: 15px;
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
    }

    .mission-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 12px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }

    .objectives-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
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
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);